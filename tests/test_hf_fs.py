from huggingface_hub import HfFileSystem
import os


def test_read_hf():
    token = os.environ.get("DOJO_HF_TOKEN")
    fs = HfFileSystem(token=token)
    repo = "datasets/AlphaDojo/dojo_benchmark_kline"
    try:
        print(fs.ls(repo))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_read_hf()
