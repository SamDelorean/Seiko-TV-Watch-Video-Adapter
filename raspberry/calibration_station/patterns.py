#!/usr/bin/env python3
"""Canonical monochrome diagnostic patterns for the Seiko TV Watch station.

The generator deliberately uses only the Python standard library and writes
binary PGM (P5) files. PGM keeps the canonical diagnostic assets lossless,
simple, grayscale-native, and independent of any rendering toolkit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


DEFAULT_WIDTH = 720
DEFAULT_HEIGHT = 480


@dataclass(frozen=True)
class PatternSpec:
    pattern_id: str
    name: str
    description: str
    generator: Callable[[int, int], bytes]


def _solid(width: int, height: int, value: int) -> bytes:
    if not 0 <= value <= 255:
        raise ValueError("grayscale value must be in [0,255]")
    return bytes([value]) * (width * height)


def _vertical_bars(width: int, height: int, values: Iterable[int]) -> bytes:
    vals = tuple(values)
    if not vals:
        raise ValueError("at least one bar is required")
    row = bytearray(width)
    n = len(vals)
    for x in range(width):
        idx = min((x * n) // width, n - 1)
        row[x] = vals[idx]
    return bytes(row) * height


def _horizontal_ramp(width: int, height: int) -> bytes:
    if width == 1:
        row = bytes([0])
    else:
        row = bytes(round(255 * x / (width - 1)) for x in range(width))
    return row * height


def _vertical_ramp(width: int, height: int) -> bytes:
    out = bytearray(width * height)
    if height == 1:
        return bytes(out)
    for y in range(height):
        value = round(255 * y / (height - 1))
        start = y * width
        out[start:start + width] = bytes([value]) * width
    return bytes(out)


def _percent_values(values: Iterable[int]) -> tuple[int, ...]:
    return tuple(round(255 * p / 100) for p in values)


def gen_a00(width: int, height: int) -> bytes:
    return _solid(width, height, 0)


def gen_a01(width: int, height: int) -> bytes:
    return _solid(width, height, 255)


def gen_a02(width: int, height: int) -> bytes:
    return _solid(width, height, 128)


def gen_a03(width: int, height: int) -> bytes:
    return _vertical_bars(width, height, (round(255 * i / 10) for i in range(11)))


def gen_a04(width: int, height: int) -> bytes:
    return _horizontal_ramp(width, height)


def gen_a05(width: int, height: int) -> bytes:
    return _vertical_ramp(width, height)


def gen_a06(width: int, height: int) -> bytes:
    return _vertical_bars(width, height, _percent_values((0, 2, 4, 6, 8, 10)))


def gen_a07(width: int, height: int) -> bytes:
    return _vertical_bars(width, height, _percent_values((90, 92, 94, 96, 98, 100)))


PATTERNS: tuple[PatternSpec, ...] = (
    PatternSpec("A00", "BLACK", "Full-field black / black-level reference.", gen_a00),
    PatternSpec("A01", "WHITE", "Full-field white / maximum-drive reference.", gen_a01),
    PatternSpec("A02", "MIDGRAY", "Full-field 50% nominal gray.", gen_a02),
    PatternSpec("A03", "GRAY_STEPS_0_100", "11 vertical steps from 0% to 100%.", gen_a03),
    PatternSpec("A04", "GRAY_RAMP_H", "Continuous left-to-right grayscale ramp.", gen_a04),
    PatternSpec("A05", "GRAY_RAMP_V", "Continuous top-to-bottom grayscale ramp.", gen_a05),
    PatternSpec("A06", "NEAR_BLACK", "0/2/4/6/8/10% nominal luma bars.", gen_a06),
    PatternSpec("A07", "NEAR_WHITE", "90/92/94/96/98/100% nominal luma bars.", gen_a07),
)
PATTERN_MAP = {p.pattern_id: p for p in PATTERNS}


def pgm_bytes(width: int, height: int, pixels: bytes) -> bytes:
    expected = width * height
    if len(pixels) != expected:
        raise ValueError(f"expected {expected} pixels, got {len(pixels)}")
    header = f"P5\n# Seiko TV Watch calibration station\n{width} {height}\n255\n".encode("ascii")
    return header + pixels


def generate_pattern(pattern_id: str, width: int, height: int) -> bytes:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    try:
        spec = PATTERN_MAP[pattern_id.upper()]
    except KeyError as exc:
        raise ValueError(f"unknown pattern: {pattern_id}") from exc
    pixels = spec.generator(width, height)
    return pgm_bytes(width, height, pixels)


def generate_all(output_dir: Path, width: int, height: int) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": 1,
        "width": width,
        "height": height,
        "format": "PGM/P5 8-bit grayscale",
        "patterns": [],
    }

    for spec in PATTERNS:
        content = generate_pattern(spec.pattern_id, width, height)
        filename = f"{spec.pattern_id}_{spec.name.lower()}.pgm"
        path = output_dir / filename
        path.write_bytes(content)
        manifest["patterns"].append(
            {
                "id": spec.pattern_id,
                "name": spec.name,
                "description": spec.description,
                "file": filename,
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate canonical Seiko TV Watch grayscale patterns.")
    parser.add_argument("--output", type=Path, default=Path("generated_patterns"))
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--pattern", choices=[p.pattern_id for p in PATTERNS])
    args = parser.parse_args()

    if args.pattern:
        args.output.mkdir(parents=True, exist_ok=True)
        spec = PATTERN_MAP[args.pattern]
        filename = f"{spec.pattern_id}_{spec.name.lower()}.pgm"
        content = generate_pattern(spec.pattern_id, args.width, args.height)
        (args.output / filename).write_bytes(content)
        print(args.output / filename)
    else:
        manifest = generate_all(args.output, args.width, args.height)
        print(f"generated {len(manifest['patterns'])} patterns in {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
