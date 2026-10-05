# Seiko TV Watch Video Adapter

Reverse-engineering and hardware/software project for a **modern display, diagnostic and integration station** for the Seiko TV Watch. The project is not intended to permanently replace the original pocket receiver or alter a collectible watch. Instead, it documents the original interface and provides reversible ways to power, test, diagnose, demonstrate and integrate the wrist unit with modern or experimental video sources.

## Goal

Build a reversible bench/display station around the original Seiko TV Watch connector. The station should support several use cases: preservation-friendly exhibition, electrical diagnosis and repair, interface characterization, test-pattern injection, and experimental connection to modern video sources such as Raspberry Pi or the Game Boy/RP2C02 project. MP4/H.264 playback is one demonstration path, not the sole purpose of the project.

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

Candidate source paths are documented in [docs/input-paths.md](docs/input-paths.md). The Game Boy/RP2C02 route is cross-linked in [docs/gameboy-rp2c02-integration.md](docs/gameboy-rp2c02-integration.md); its first sync-completion hardware decision is in [hardware/gameboy-rp2c02-sync-v0.1.md](hardware/gameboy-rp2c02-sync-v0.1.md). The Seiko's analog LVD sampling model is summarized in [docs/lvd-sampling.md](docs/lvd-sampling.md).

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

## Preservation and scope principle

The original Seiko receiver remains historically significant and is **not treated as obsolete hardware to be permanently replaced**. This project is a companion test/display platform.

The preferred implementation is external, reversible and non-destructive: the watch remains original, the factory connector is used wherever practical, and any modern interface should be removable without altering the collectible unit.

Publishing the reconstructed interface is also intended to make the work useful beyond exhibition. The same electrical information and example interface blocks may support:

- diagnosis of a watch or receiver;
- repair and restoration work;
- bench testing without depending on RF broadcast reception;
- museum or collector display setups;
- development of reversible modern video-source adapters;
- experimentation with other compatible NTSC-derived sources.

The repository documents interfaces and implementation ideas rather than prescribing one permanent conversion.

## Documentation status labels

- **CONFIRMED** — directly supported by primary documentation or consistent independent measurements.
- **INFERRED** — technically supported but not yet directly measured on the target hardware.
- **TO MEASURE** — must be characterized on the original receiver before implementation.
