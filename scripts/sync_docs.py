from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from common import dump_json, docs_root, root_docs_json, skill_root, state_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync OpenClaw docs into the local skill snapshot.")
    parser.add_argument("--source-path", help="Path to a local OpenClaw checkout.")
    parser.add_argument("--repo-url", help="Git repo URL for OpenClaw.")
    parser.add_argument("--ref", default="main", help="Git ref to sync when using --repo-url.")
    parser.add_argument("--subdir", default="docs", help="Docs directory inside the upstream repo.")
    parser.add_argument("--mode", choices=["pinned", "tracking"], default="pinned")
    parser.add_argument("--keep-assets", action="store_true", help="Keep non-markdown assets instead of text-first sync.")
    return parser.parse_args()


def run_git_clone(repo_url: str, ref: str, destination: Path) -> Path:
    cmd = ["git", "clone", "--depth", "1", "--branch", ref, repo_url, str(destination)]
    subprocess.run(cmd, check=True)
    return destination


def copy_docs(source_docs: Path, destination: Path, keep_assets: bool) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    for item in source_docs.iterdir():
        if item.name == "docs.json":
            continue
        target = destination / item.name
        if item.is_dir():
            if keep_assets:
                shutil.copytree(item, target)
                continue
            markdown_like = [path for path in item.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".mdx", ".json"}]
            if not markdown_like:
                continue
            for path in markdown_like:
                rel = path.relative_to(item)
                out = target / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, out)
            continue
        if keep_assets or item.suffix.lower() in {".md", ".mdx", ".json"}:
            shutil.copy2(item, target)


def detect_commit(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def main() -> int:
    args = parse_args()
    if not args.source_path and not args.repo_url:
        print("ERROR: Provide --source-path or --repo-url.")
        return 1

    root = skill_root()
    state = state_root()
    state.mkdir(parents=True, exist_ok=True)
    current_manifest = state / "docs-manifest.json"
    previous_manifest = state / "docs-manifest.previous.json"
    if current_manifest.exists():
        shutil.copy2(current_manifest, previous_manifest)

    with tempfile.TemporaryDirectory(prefix="openclaw-sync-") as tmp:
        tmp_path = Path(tmp)
        if args.source_path:
            repo_root = Path(args.source_path).resolve()
            source_type = "local_repo"
        else:
            repo_root = run_git_clone(args.repo_url, args.ref, tmp_path / "repo")
            source_type = "git_clone"

        source_docs = repo_root / args.subdir
        source_docs_json = source_docs / "docs.json"
        if not source_docs.exists():
            print(f"ERROR: Docs directory not found: {source_docs}")
            return 1
        if not source_docs_json.exists():
            print(f"ERROR: docs.json not found: {source_docs_json}")
            return 1

        staged_docs = tmp_path / "staged_docs"
        copy_docs(source_docs, staged_docs, keep_assets=args.keep_assets)

        live_docs = docs_root()
        backup_docs = root / "openclaw_docs.previous"
        if backup_docs.exists():
            shutil.rmtree(backup_docs)
        if live_docs.exists():
            shutil.move(str(live_docs), str(backup_docs))
        shutil.move(str(staged_docs), str(live_docs))
        shutil.copy2(source_docs_json, root_docs_json())

        source_lock = {
            "repo_url": args.repo_url or "https://github.com/openclaw/openclaw",
            "source_type": source_type,
            "source_path": str(Path(args.source_path).resolve()) if args.source_path else None,
            "tracked_ref": args.ref,
            "resolved_commit": detect_commit(repo_root),
            "docs_subdir": args.subdir,
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "mode": args.mode,
            "keep_assets": bool(args.keep_assets),
            "previous_manifest_present": previous_manifest.exists(),
        }
        dump_json(state / "source-lock.json", source_lock)
    print("Docs sync completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
