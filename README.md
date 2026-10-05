# Seiko TV Watch Video Adapter

Reverse-engineering and hardware/software project to replace the original Seiko TV Watch pocket receiver with a modern video source while keeping the wristwatch itself unmodified.

## Goal

Play modern video files (MP4/H.264 as the first target) on the original Seiko TV Watch LCD through its original external video connector.

The preferred architecture is:

```text
MP4 file
   |
Raspberry Pi / video source
   |
NTSC composite generation
   |
+-----------------------+
| interface electronics |
| - video conditioning  |
| - sync conditioning   |
| - power rails         |
+-----------------------+
   |
original Seiko cable
   |
Seiko TV Watch
```

## Current status

**Phase: v0.1 — interface reconstruction**

Available documentation is sufficient to establish that the original pocket receiver does not appear to send a proprietary digital pixel bus. The watch receives separate analog video and synchronization signals, together with several supply rails.

Current working interface:

| Pin | Function | Current evidence status |
|---|---|---|
| 1 | ~+8.9 V supply | CONFIRMED in independent measurements; verify on original unit |
| 2 | ~+13.2 V supply | CONFIRMED in independent measurements; verify on original unit |
| 3 | ~+4.1 V supply | CONFIRMED in independent measurements; verify on original unit |
| 4 | Electrical ground | CONFIRMED |
| 5 | Composite synchronization | CONFIRMED function; exact waveform to measure |
| 6 | Analog video / DC bias | CONFIRMED function; exact polarity, impedance and levels to measure |
| chassis contact | chassis ground | DOCUMENTED; verify connector implementation |

See [docs/interface.md](docs/interface.md) for the evidence model and electrical details.

Candidate source paths are documented in [docs/input-paths.md](docs/input-paths.md). The Game Boy/RP2C02 route is cross-linked in [docs/gameboy-rp2c02-integration.md](docs/gameboy-rp2c02-integration.md), and the Seiko's analog LVD sampling model is summarized in [docs/lvd-sampling.md](docs/lvd-sampling.md).

## Important rule

No signal is to be applied to an original watch until the corresponding voltage, polarity, impedance and waveform have been verified against an original receiver with an oscilloscope.

## Repository structure

- `docs/` — research, signal reconstruction and sources
- `hardware/` — adapter schematics and PCB work
- `raspberry/` — playback and composite-video generation
- `tests/` — oscilloscope captures, test patterns and validation procedures
- `media/` — original diagrams and assets for documentation/video production

## Planned milestones

1. **v0.1 — Interface reconstruction**
2. **v0.2 — Bench electrical emulator**
3. **v0.3 — Raspberry Pi composite-video prototype**
4. **v0.4 — First image on the original watch**
5. **v0.5 — MP4 playback**
6. **v1.0 — Reproducible hardware/software build**

See [ROADMAP.md](ROADMAP.md).

## Preservation principle

The project is intended to be non-destructive: the watch should remain original and the adapter should emulate the external receiver through the factory connector.

## Documentation status labels

- **CONFIRMED** — directly supported by primary documentation or consistent independent measurements.
- **INFERRED** — technically supported but not yet directly measured on the target hardware.
- **TO MEASURE** — must be characterized on the original receiver before implementation.
