#!/usr/bin/env python3
import os
import sys
import re
import json
import ast
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Compare QData OpenAPI schema against DojoSDK codebase implementations.")
    parser.add_argument(
        "--openapi",
        default="docs/qdata_openapi.json",
        help="Path to the OpenAPI JSON file (default: docs/qdata_openapi.json)",
    )
    parser.add_argument(
        "--codebase",
        default="dojo/resources",
        help="Path to the client resources directory (default: dojo/resources)",
    )
    return parser.parse_args()


def load_openapi(filepath):
    if not os.path.exists(filepath):
        print(f"Error: OpenAPI file not found at {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    endpoints = {}
    for path, methods in data.get("paths", {}).items():
        for method, info in methods.items():
            if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                continue
            key = (path, method.upper())

            query_params = {}
            path_params = {}
            for p in info.get("parameters", []):
                p_name = p.get("name")
                p_in = p.get("in")
                p_req = p.get("required", False)
                schema = p.get("schema", {})
                p_type = schema.get("type", "any") if "schema" in p else "any"

                if p_in == "query":
                    query_params[p_name] = {"required": p_req, "type": p_type}
                elif p_in == "path":
                    path_params[p_name] = {"required": p_req, "type": p_type}

            endpoints[key] = {
                "query_params": query_params,
                "path_params": path_params,
                "has_body": "requestBody" in info,
                "summary": info.get("summary", ""),
                "operationId": info.get("operationId", ""),
                "tags": info.get("tags", []),
            }
    return endpoints


def scan_codebase(resources_dir):
    if not os.path.exists(resources_dir):
        print(f"Error: Codebase directory not found at {resources_dir}", file=sys.stderr)
        sys.exit(1)

    code_endpoints = {}

    for filename in os.listdir(resources_dir):
        if not filename.endswith(".py") or filename == "base.py":
            continue
        filepath = os.path.join(resources_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=filename)
            except SyntaxError as e:
                print(f"Warning: Syntax error parsing {filename}: {e}", file=sys.stderr)
                continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for body_node in node.body:
                    if isinstance(body_node, ast.FunctionDef):
                        # Find calls to self._get, self._post, etc.
                        for sub_node in ast.walk(body_node):
                            if isinstance(sub_node, ast.Call) and isinstance(sub_node.func, ast.Attribute) and sub_node.func.attr in ["_get", "_post", "_put", "_delete"]:
                                if sub_node.args:
                                    path_node = sub_node.args[0]
                                    path = None
                                    if isinstance(path_node, ast.Constant):
                                        path = path_node.value
                                    elif isinstance(path_node, ast.JoinedStr):
                                        path_parts = []
                                        for val in path_node.values:
                                            if isinstance(val, ast.Constant):
                                                path_parts.append(val.value)
                                            elif isinstance(val, ast.FormattedValue):
                                                path_parts.append(f"{{{val.value.id}}}")
                                        path = "".join(path_parts)

                                    if path:
                                        http_method = sub_node.func.attr[1:].upper()
                                        # Extract method arguments
                                        method_args = {arg.arg for arg in body_node.args.kwonlyargs}
                                        for arg in body_node.args.args:
                                            if arg.arg != "self":
                                                method_args.add(arg.arg)

                                        code_endpoints[(path, http_method)] = {
                                            "file": filename,
                                            "method_name": body_node.name,
                                            "args": method_args,
                                        }
    return code_endpoints


def norm_path(p):
    return re.sub(r"\{[^}]+\}", "{}", p)


def main():
    args = parse_args()
    openapi = load_openapi(args.openapi)
    codebase = scan_codebase(args.codebase)

    # Normalize keys for path variable matches
    openapi_norm = {norm_path(k[0]) + "_" + k[1]: k for k in openapi.keys()}
    codebase_norm = {norm_path(k[0]) + "_" + k[1]: k for k in codebase.keys()}

    # 1. New/Missing Endpoints
    print("=== Endpoints in OpenAPI but NOT in codebase (New/Missing) ===")
    missing_count = 0
    for norm_key, orig_openapi_key in sorted(openapi_norm.items()):
        if norm_key not in codebase_norm:
            info = openapi[orig_openapi_key]
            print(f"- {orig_openapi_key[1]} {orig_openapi_key[0]} (Tags: {info['tags']}, Summary: {info['summary']})")
            missing_count += 1
    if missing_count == 0:
        print("  None")
    print(f"Total: {missing_count}\n")

    # 2. Removed Endpoints
    print("=== Endpoints in codebase but NOT in OpenAPI (Deleted/Removed) ===")
    removed_count = 0
    for norm_key, orig_codebase_key in sorted(codebase_norm.items()):
        if norm_key not in openapi_norm:
            info = codebase[orig_codebase_key]
            print(f"- {orig_codebase_key[1]} {orig_codebase_key[0]} (Implemented as '{info['method_name']}' in {info['file']})")
            removed_count += 1
    if removed_count == 0:
        print("  None")
    print(f"Total: {removed_count}\n")

    # 3. Discrepancies on common endpoints
    print("=== Parameter Mismatches on Common Endpoints ===")
    mismatch_count = 0
    for norm_key in sorted(openapi_norm.keys() & codebase_norm.keys()):
        orig_openapi_key = openapi_norm[norm_key]
        orig_codebase_key = codebase_norm[norm_key]

        openapi_info = openapi[orig_openapi_key]
        code_info = codebase[orig_codebase_key]

        # Get parameter sets
        openapi_params = set(openapi_info["query_params"].keys()) | set(openapi_info["path_params"].keys())
        code_params = set(code_info["args"])
        code_params.discard("body")
        code_params.discard("headers")

        # Exclude path params because some OpenAPI specs don't list path params explicitly in PUT/POST requests
        path_params = set(openapi_info["path_params"].keys())
        openapi_params -= path_params
        code_params -= path_params

        added_params = openapi_params - code_params
        removed_params = code_params - openapi_params

        if added_params or removed_params:
            print(f"- {orig_openapi_key[1]} {orig_openapi_key[0]} (method '{code_info['method_name']}' in {code_info['file']}):")
            if added_params:
                print(f"  Added in OpenAPI: {sorted(added_params)}")
            if removed_params:
                print(f"  Missing in OpenAPI / Extra in Code: {sorted(removed_params)}")
            mismatch_count += 1
    if mismatch_count == 0:
        print("  None")
    print(f"Total mismatches: {mismatch_count}\n")


if __name__ == "__main__":
    main()
