from concurrent.futures import ThreadPoolExecutor
from huggingface_hub import hf_hub_download


def download_file(repo_id, filename):
    print(f"Starting {filename}")
    try:
        hf_hub_download(repo_id=repo_id, filename=filename, repo_type="dataset", force_download=True)
    except Exception as e:
        print(e)
    print(f"Done {filename}")


repos = [("squad", "plain_text/train-00000-of-00001.parquet"), ("squad", "plain_text/validation-00000-of-00001.parquet")]

with ThreadPoolExecutor(max_workers=2) as pool:
    for r, f in repos:
        pool.submit(download_file, r, f)
