import os
import shutil


def cleanup_ms_snapshots(snapshots_dir, current_commit):
    if not os.path.exists(snapshots_dir):
        return
    snapshots = [d for d in os.listdir(snapshots_dir) if os.path.isdir(os.path.join(snapshots_dir, d))]
    other_commits = [s for s in snapshots if s != current_commit]
    if other_commits:
        for c in other_commits:
            path_to_delete = os.path.join(snapshots_dir, c)
            shutil.rmtree(path_to_delete, ignore_errors=True)
            print(f"Cleaned up old modelscope revision: {c}")


# Create dummy dirs
os.makedirs("dummy_repo/snapshots/commit1")
os.makedirs("dummy_repo/snapshots/commit2")
cleanup_ms_snapshots("dummy_repo/snapshots", "commit2")
print("Remaining:", os.listdir("dummy_repo/snapshots"))
