# Seiko calibration station — A00..A07 implementation

This directory contains the first executable implementation of the Raspberry Pi calibration station.

## What is implemented

Canonical monochrome patterns:

- A00 — full black
- A01 — full white
- A02 — 50% gray
- A03 — 11-step 0–100% grayscale
- A04 — horizontal grayscale ramp
- A05 — vertical grayscale ramp
- A06 — near-black 0/2/4/6/8/10%
- A07 — near-white 90/92/94/96/98/100%

The generator writes **binary PGM (P5)** images using only the Python standard library. PGM is intentional: the canonical source is lossless, grayscale-native, trivial to audit, and independent of the display frontend.

Default raster: **720 × 480**. This is the source raster presented to the Raspberry Pi display pipeline; it must not be confused with the physical ~152 × 210 LVD cell matrix.

## Files

- `patterns.py` — canonical pattern generator and SHA-256 manifest writer.
- `station.py` — manual/automatic controller.
- `sequence-a00-a07.json` — deterministic automatic sequence.
- `test_patterns.py` — standard-library regression tests.
- `generated_patterns/` — generated at runtime; do not treat generated files as source of truth.
- `logs/diagnostic.jsonl` — optional run log.

## Generate

From this directory:

```sh
python3 patterns.py --output generated_patterns
```

or:

```sh
python3 station.py --generate --list
```

## Regression test

```sh
python3 test_patterns.py
```

The tests verify exact luma values, ramp endpoints, pattern IDs and manifest/hash generation.

## Display frontend

The canonical generator has no GUI dependency. `station.py` currently uses `ffplay` by default as a replaceable full-screen frontend.

Example:

```sh
python3 station.py --generate
```

Select A00..A07 from the menu.

Show one pattern:

```sh
python3 station.py --show A03
```

Run the timed sequence:

```sh
python3 station.py --auto
```

A custom viewer may be supplied:

```sh
python3 station.py --show A00 --viewer 'myviewer --fullscreen {image}'
```

The viewer is deliberately separate from pattern generation so a later DRM/KMS-native renderer can replace `ffplay` without changing the canonical diagnostic assets.

## Automatic sequence

`sequence-a00-a07.json` is versioned separately from the program. Durations can therefore be changed without changing pattern generation.

Current sequence:

| ID | Duration |
|---|---:|
| A00 | 5 s |
| A01 | 5 s |
| A02 | 5 s |
| A03 | 8 s |
| A04 | 8 s |
| A05 | 8 s |
| A06 | 8 s |
| A07 | 8 s |

The AUTO runner writes JSONL events containing run ID, UTC timestamps, pattern ID, requested duration and viewer return code.

## Important measurement rule

These are **digital source levels**, not yet calibrated Seiko pin-6 voltages.

The analog bench remains responsible for:

- CVBS termination/buffering;
- sync extraction;
- video gain;
- DC bias;
- protection;
- 4.1/8.9/13.2 V rails.

A pattern's 0–255 digital level must not be interpreted directly as a voltage at the watch connector.
