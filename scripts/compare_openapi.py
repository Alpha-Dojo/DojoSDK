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
    parser.add_argument(
        "--scope-prefix",
        action="append",
        default=[],
        help="Only compare paths with this prefix; may be repeated.",
    )
    parser.add_argument(
        "--scope-path",
        action="append",
        default=[],
        help="Only compare this exact path; may be repeated.",
    )
    parser.add_argument(
        "--method",
        action="append",
        default=[],
        help="Only compare this HTTP method; may be repeated.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when the selected scope contains a drift.",
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

            has_body = "requestBody" in info
            body_required = info.get("requestBody", {}).get("required", False)

            endpoints[key] = {
                "query_params": query_params,
                "path_params": path_params,
                "has_body": has_body,
                "body_required": body_required,
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
                class_name = node.name
                for body_node in node.body:
                    if isinstance(body_node, ast.FunctionDef) or getattr(ast, "AsyncFunctionDef", type(None)) and isinstance(body_node, ast.AsyncFunctionDef):
                        assigned_paths = {}
                        for statement in body_node.body:
                            if (
                                isinstance(statement, ast.Assign)
                                and len(statement.targets) == 1
                                and isinstance(statement.targets[0], ast.Name)
                                and isinstance(statement.value, ast.IfExp)
                            ):
                                choices = (statement.value.body, statement.value.orelse)
                                if all(isinstance(choice, ast.Constant) and isinstance(choice.value, str) for choice in choices):
                                    assigned_paths[statement.targets[0].id] = [choice.value for choice in choices]
                        for sub_node in ast.walk(body_node):
                            if isinstance(sub_node, ast.Call) and isinstance(sub_node.func, ast.Attribute) and sub_node.func.attr in ["_get", "_post", "_put", "_delete", "_patch"]:
                                if sub_node.args:
                                    path_node = sub_node.args[0]
                                    paths = []
                                    path_vars = set()
                                    if isinstance(path_node, ast.Constant):
                                        paths = [path_node.value]
                                        # Also look for format strings using .format()
                                        matches = re.findall(r"\{([A-Za-z0-9_]+)\}", str(path_node.value))
                                        for m in matches:
                                            path_vars.add(m)
                                    elif isinstance(path_node, ast.JoinedStr):
                                        path_parts = []
                                        for val in path_node.values:
                                            if isinstance(val, ast.Constant):
                                                path_parts.append(val.value)
                                            elif isinstance(val, ast.FormattedValue):
                                                var_name = val.value.id if isinstance(val.value, ast.Name) else "unknown"
                                                path_vars.add(var_name)
                                                path_parts.append(f"{{{var_name}}}")
                                        paths = ["".join(path_parts)]
                                    elif isinstance(path_node, ast.Name):
                                        paths = assigned_paths.get(path_node.id, [])

                                    for path in paths:
                                        http_method = sub_node.func.attr[1:].upper()

                                        method_args = {}

                                        num_args = len(body_node.args.args)
                                        num_defaults = len(body_node.args.defaults)
                                        for i, arg in enumerate(body_node.args.args):
                                            if arg.arg == "self":
                                                continue
                                            has_default = i >= num_args - num_defaults
                                            method_args[arg.arg] = {"required": not has_default}

                                        for i, arg in enumerate(body_node.args.kwonlyargs):
                                            default_node = body_node.args.kw_defaults[i]
                                            has_default = default_node is not None
                                            method_args[arg.arg] = {"required": not has_default}

                                        code_endpoints[(path, http_method, class_name)] = {
                                            "file": filename,
                                            "method_name": body_node.name,
                                            "args": method_args,
                                            "path_vars": path_vars,
                                        }
    return code_endpoints


def norm_path(p):
    return re.sub(r"\{[^}]+\}", "{}", p)


def main():
    args = parse_args()
    openapi = load_openapi(args.openapi)
    codebase = scan_codebase(args.codebase)
    if args.scope_prefix:
        prefixes = tuple(args.scope_prefix)
        openapi = {key: value for key, value in openapi.items() if key[0].startswith(prefixes)}
        codebase = {key: value for key, value in codebase.items() if key[0].startswith(prefixes)}
    if args.scope_path:
        paths = set(args.scope_path)
        openapi = {key: value for key, value in openapi.items() if key[0] in paths}
        codebase = {key: value for key, value in codebase.items() if key[0] in paths}
    if args.method:
        methods = {method.upper() for method in args.method}
        openapi = {key: value for key, value in openapi.items() if key[1] in methods}
        codebase = {key: value for key, value in codebase.items() if key[1] in methods}

    openapi_norm = {norm_path(k[0]) + "_" + k[1]: k for k in openapi.keys()}

    codebase_norm = {}
    for (path, method, class_name), code_info in codebase.items():
        n_path = norm_path(path) + "_" + method
        if n_path not in codebase_norm:
            codebase_norm[n_path] = []
        codebase_norm[n_path].append(((path, method, class_name), code_info))

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

    print("=== Endpoints in codebase but NOT in OpenAPI (Deleted/Removed) ===")
    removed_count = 0
    for norm_key, class_implementations in sorted(codebase_norm.items()):
        if norm_key not in openapi_norm:
            for orig_codebase_key, info in class_implementations:
                print(f"- {orig_codebase_key[1]} {orig_codebase_key[0]} (Implemented as '{info['method_name']}' in {info['file']}:{orig_codebase_key[2]})")
                removed_count += 1
    if removed_count == 0:
        print("  None")
    print(f"Total: {removed_count}\n")

    print("=== Parameter Mismatches on Common Endpoints ===")
    mismatch_count = 0
    for norm_key in sorted(openapi_norm.keys() & codebase_norm.keys()):
        orig_openapi_key = openapi_norm[norm_key]
        openapi_info = openapi[orig_openapi_key]

        class_implementations = codebase_norm[norm_key]

        for orig_codebase_key, code_info in class_implementations:
            openapi_path_params = set(openapi_info["path_params"].keys())
            code_path_vars = code_info["path_vars"]

            openapi_query_params = set(openapi_info["query_params"].keys())
            code_args = set(code_info["args"].keys())
            code_args.discard("headers")

            has_body_arg = "body" in code_args
            code_args.discard("body")

            code_args -= code_path_vars

            mismatches = []

            if openapi_info["body_required"] and not has_body_arg:
                mismatches.append("Missing 'body' parameter in code, but OpenAPI requires requestBody")
            elif not openapi_info["has_body"] and has_body_arg:
                mismatches.append("Extra 'body' parameter in code, but OpenAPI has no requestBody")

            added_path_vars = openapi_path_params - code_path_vars
            removed_path_vars = code_path_vars - openapi_path_params
            if added_path_vars:
                mismatches.append(f"Missing Path Variables in Code: {sorted(added_path_vars)}")
            if removed_path_vars:
                mismatches.append(f"Extra Path Variables in Code: {sorted(removed_path_vars)}")

            added_query_params = openapi_query_params - code_args
            removed_query_params = code_args - openapi_query_params

            if added_query_params:
                mismatches.append(f"Added Query Params in OpenAPI: {sorted(added_query_params)}")
            if removed_query_params:
                real_extra = removed_query_params - openapi_path_params
                if real_extra:
                    mismatches.append(f"Missing in OpenAPI / Extra Query Params in Code: {sorted(real_extra)}")

            common_query_params = openapi_query_params & code_args
            for p in common_query_params:
                o_req = openapi_info["query_params"][p]["required"]
                c_req = code_info["args"][p]["required"]
                if o_req != c_req:
                    mismatches.append(f"Parameter '{p}' required status mismatch: OpenAPI ({o_req}) vs Code ({c_req})")

            if mismatches:
                print(f"- {orig_codebase_key[1]} {orig_openapi_key[0]} (method '{code_info['method_name']}' in {code_info['file']}:{orig_codebase_key[2]}):")
                for m in mismatches:
                    print(f"  {m}")
                mismatch_count += 1

    if mismatch_count == 0:
        print("  None")
    print(f"Total mismatches: {mismatch_count}\n")
    if args.strict and (missing_count or removed_count or mismatch_count):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
