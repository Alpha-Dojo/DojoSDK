from __future__ import annotations

import os
from pathlib import Path
from huggingface_hub import HfApi


def upload_dataset(dataset_name: str, local_folder: str | Path, token: str | None = None, ms_token: str | None = None) -> None:
    """Uploads a local folder as a dataset to HuggingFace Hub and ModelScope.

    Parameters
    ----------
    dataset_name : str
        The name of the dataset to upload (e.g. 'dojo_sector_precomputed').
        It will be mapped to the AlphaDojo/alphadojo organization automatically.
    local_folder : str | Path
        The path to the local folder containing the dataset files.
    token : str | None
        HuggingFace token. If None, it attempts to use the HF_TOKEN environment variable.
    ms_token : str | None
        ModelScope token. If None, it attempts to use MODELSCOPE_TOKEN or DOJO_MODELSCOPE_TOKEN.
    """
    hf_token = token or os.environ.get("HF_TOKEN")
    ms_token = ms_token or os.environ.get("MODELSCOPE_TOKEN") or os.environ.get("DOJO_MODELSCOPE_TOKEN")

    if not hf_token and not ms_token:
        raise ValueError("Missing both HF_TOKEN and MODELSCOPE_TOKEN for upload.")

    if hf_token:
        api = HfApi(token=hf_token)
        repo_id = f"AlphaDojo/{dataset_name}"

        # Ensure the repo exists; create if it doesn't.
        try:
            api.create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True)
        except Exception as e:  # noqa
            pass

        api.upload_folder(folder_path=str(local_folder), repo_id=repo_id, repo_type="dataset")

    if ms_token:
        from modelscope.hub.api import HubApi
        from dojo.logging import logger

        ms_api = HubApi()
        ms_api.login(ms_token)
        ms_repo_id = f"alphadojo/{dataset_name}"

        try:
            ms_api.create_dataset(dataset_name=dataset_name, namespace="alphadojo", visibility=5)
        except Exception as e:
            logger.debug(f"ModelScope repo might already exist: {e}")
            pass

        ms_api.upload_folder(folder_path=str(local_folder), repo_id=ms_repo_id, repo_type="dataset")


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
