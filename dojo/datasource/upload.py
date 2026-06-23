from __future__ import annotations

import os
from pathlib import Path
from huggingface_hub import HfApi


def upload_dataset(dataset_name: str, local_folder: str | Path, token: str | None = None) -> None:
    """Uploads a local folder as a dataset to HuggingFace Hub.

    Parameters
    ----------
    dataset_name : str
        The name of the dataset to upload (e.g. 'dojo_sector_precomputed').
        It will be mapped to the AlphaDojo organization automatically.
    local_folder : str | Path
        The path to the local folder containing the dataset files.
    token : str | None
        HuggingFace token. If None, it attempts to use the HF_TOKEN environment variable.
    """
    token = token or os.environ.get("HF_TOKEN")
    if not token:
        raise ValueError("Missing HF_TOKEN for upload. Set HF_TOKEN environment variable or pass it to upload_dataset().")

    api = HfApi(token=token)
    repo_id = f"AlphaDojo/{dataset_name}"

    # Ensure the repo exists; create if it doesn't.
    try:
        api.create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True)
    except Exception as e:  # noqa
        # If it fails, maybe we don't have permission to create it or it exists and exist_ok failed.
        # Proceed to upload anyway.
        pass

    api.upload_folder(folder_path=str(local_folder), repo_id=repo_id, repo_type="dataset")


def download_dataset(dataset_name: str, local_folder: str | Path, token: str | None = None) -> None:
    """Downloads a dataset from HuggingFace Hub to a local folder.

    Parameters
    ----------
    dataset_name : str
        The name of the dataset to download (e.g. 'dojo_sector_precomputed').
        It will be mapped to the AlphaDojo organization automatically.
    local_folder : str | Path
        The path to the local folder where the dataset should be downloaded.
    token : str | None
        HuggingFace token. If None, it attempts to use the HF_TOKEN environment variable.
    """
    token = token or os.environ.get("HF_TOKEN")
    from huggingface_hub import snapshot_download

    repo_id = f"AlphaDojo/{dataset_name}"
    os.makedirs(local_folder, exist_ok=True)

    snapshot_download(
        repo_id=repo_id,
        repo_type="dataset",
        local_dir=str(local_folder),
        token=token,
    )
