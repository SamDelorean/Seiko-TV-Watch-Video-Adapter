#!/usr/bin/env python3
"""Manual/automatic front-end for the Seiko TV Watch calibration patterns."""

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

try:
    from .patterns import PATTERN_MAP, PATTERNS, generate_all
except ImportError:
    from patterns import PATTERN_MAP, PATTERNS, generate_all


ROOT = Path(__file__).resolve().parent
DEFAULT_GENERATED = ROOT / "generated_patterns"
DEFAULT_SEQUENCE = ROOT / "sequence-a00-a07.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_manifest(pattern_dir: Path) -> dict:
    manifest = pattern_dir / "manifest.json"
    if not manifest.exists():
        raise FileNotFoundError(f"missing {manifest}; run with --generate first")
    return json.loads(manifest.read_text(encoding="utf-8"))


def _pattern_file(manifest: dict, pattern_dir: Path, pattern_id: str) -> Path:
    for item in manifest["patterns"]:
        if item["id"] == pattern_id:
            return pattern_dir / item["file"]
    raise KeyError(pattern_id)


def _viewer_command(viewer: str, image: Path, duration: float | None) -> list[str]:
    if viewer == "ffplay":
        cmd = [
            "ffplay",
            "-hide_banner",
            "-loglevel", "error",
            "-fs",
            "-autoexit",
            "-loop", "1",
            "-framerate", "30",
        ]
        if duration is not None:
            cmd += ["-t", f"{duration:.3f}"]
        cmd += [str(image)]
        return cmd

    parts = shlex.split(viewer)
    return [
        part.format(image=str(image), duration="" if duration is None else f"{duration:.3f}")
        for part in parts
    ]


def _ensure_viewer(viewer: str) -> None:
    exe = "ffplay" if viewer == "ffplay" else shlex.split(viewer)[0]
    if shutil.which(exe) is None:
        raise RuntimeError(
            f"viewer executable '{exe}' not found. "
            "Install it or pass --viewer with a suitable command template."
        )


def _show(viewer: str, image: Path, duration: float | None) -> int:
    cmd = _viewer_command(viewer, image, duration)
    proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL)
    if duration is not None:
        return proc.wait()

    print("Pattern is on screen. Press ENTER to return.")
    try:
        input()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
    return proc.returncode or 0


def _append_log(log_path: Path, event: dict) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, sort_keys=True) + "\n")


def run_auto(manifest: dict, pattern_dir: Path, sequence_path: Path, viewer: str, log_path: Path) -> int:
    sequence = json.loads(sequence_path.read_text(encoding="utf-8"))
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    _append_log(log_path, {
        "event": "run_start",
        "run_id": run_id,
        "timestamp_utc": _utc_now(),
        "sequence": sequence.get("id"),
    })

    try:
        for step in sequence["steps"]:
            pattern_id = step["id"]
            duration = float(step["duration_s"])
            image = _pattern_file(manifest, pattern_dir, pattern_id)
            print(f"{pattern_id}: {PATTERN_MAP[pattern_id].name} ({duration:g} s)")
            _append_log(log_path, {
                "event": "pattern_start",
                "run_id": run_id,
                "timestamp_utc": _utc_now(),
                "pattern_id": pattern_id,
                "duration_s": duration,
            })
            rc = _show(viewer, image, duration)
            _append_log(log_path, {
                "event": "pattern_end",
                "run_id": run_id,
                "timestamp_utc": _utc_now(),
                "pattern_id": pattern_id,
                "viewer_rc": rc,
            })
            if rc not in (0, 255):
                return rc
    finally:
        _append_log(log_path, {
            "event": "run_end",
            "run_id": run_id,
            "timestamp_utc": _utc_now(),
        })
    return 0


def manual_menu(manifest: dict, pattern_dir: Path, viewer: str) -> int:
    while True:
        print("\nSeiko TV Watch calibration station — A00..A07")
        for spec in PATTERNS:
            print(f"  {spec.pattern_id}  {spec.name:18s}  {spec.description}")
        print("  Q    quit")
        selection = input("> ").strip().upper()
        if selection in {"Q", "QUIT", "EXIT"}:
            return 0
        if selection not in PATTERN_MAP:
            print("Unknown selection.")
            continue
        image = _pattern_file(manifest, pattern_dir, selection)
        _show(viewer, image, None)


def main() -> int:
    parser = argparse.ArgumentParser(description="Seiko TV Watch calibration-station controller.")
    parser.add_argument("--pattern-dir", type=Path, default=DEFAULT_GENERATED)
    parser.add_argument("--width", type=int, default=720)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--viewer", default="ffplay",
                        help="ffplay or a custom command template containing {image}")
    parser.add_argument("--generate", action="store_true", help="(re)generate A00..A07 assets")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--list", action="store_true")
    mode.add_argument("--show", choices=[p.pattern_id for p in PATTERNS])
    mode.add_argument("--auto", action="store_true")
    parser.add_argument("--sequence", type=Path, default=DEFAULT_SEQUENCE)
    parser.add_argument("--log", type=Path, default=ROOT / "logs" / "diagnostic.jsonl")
    args = parser.parse_args()

    if args.generate or not (args.pattern_dir / "manifest.json").exists():
        generate_all(args.pattern_dir, args.width, args.height)

    manifest = _load_manifest(args.pattern_dir)

    if args.list:
        for item in manifest["patterns"]:
            print(f"{item['id']} {item['name']} {item['file']} {item['sha256']}")
        return 0

    _ensure_viewer(args.viewer)

    if args.show:
        return _show(args.viewer, _pattern_file(manifest, args.pattern_dir, args.show), None)
    if args.auto:
        return run_auto(manifest, args.pattern_dir, args.sequence, args.viewer, args.log)
    return manual_menu(manifest, args.pattern_dir, args.viewer)


if __name__ == "__main__":
    raise SystemExit(main())
