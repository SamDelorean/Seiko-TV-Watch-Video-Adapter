# Seiko TV Watch Video Adapter

Reverse-engineering and hardware/software project for a **modern display, diagnostic and integration station** for the Seiko TV Watch. The project is not intended to permanently replace the original pocket receiver or alter a collectible watch. Instead, it documents the original interface and provides reversible ways to power, test, diagnose, demonstrate and integrate the wrist unit with modern or experimental video sources.

## Goal

Build a reversible bench/display station around the original Seiko TV Watch connector. The station should support preservation-friendly exhibition, electrical diagnosis and repair, interface characterization, test-pattern injection, and experimental connection to modern video sources.

The preferred architecture is now source-independent:

```text
Game Boy / RP2C02 --\
Raspberry Pi --------+--> standard CVBS input
DVD / camera --------/          |
pattern generator ---/          v
                         UNIVERSAL TEST STATION
                         - 75-ohm / Hi-Z input
                         - sync separation
                         - video conditioning
                         - 4.1 / 8.9 / 13.2 V rails
                         - independent audio path
                                  |
                                  v
                        original Seiko connector
                                  |
                                  v
                           Seiko TV Watch
```

MP4/H.264 playback through Raspberry Pi is one demonstration path, not the sole purpose of the project.

## Current status

**Phase: v0.1 — interface reconstruction / universal bench definition**

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

The source-independent station is defined in [hardware/universal-cvbs-bench-v0.1.md](hardware/universal-cvbs-bench-v0.1.md).

Candidate source paths are documented in [docs/input-paths.md](docs/input-paths.md). The Game Boy/RP2C02 route is cross-linked in [docs/gameboy-rp2c02-integration.md](docs/gameboy-rp2c02-integration.md), with its sync-completion decision in [hardware/gameboy-rp2c02-sync-v0.1.md](hardware/gameboy-rp2c02-sync-v0.1.md). The first Raspberry Pi source implementation is [raspberry/zero2w-cvbs-source-v0.1.md](raspberry/zero2w-cvbs-source-v0.1.md). The Raspberry is further defined as a dedicated calibration/diagnostic appliance in [raspberry/calibration-station-v0.1.md](raspberry/calibration-station-v0.1.md), with the first Seiko-specific pattern suite in [tests/pattern-catalog-v0.1.md](tests/pattern-catalog-v0.1.md). The executable A00–A07 implementation is in [raspberry/calibration_station/](raspberry/calibration_station/).

The Seiko's analog LVD sampling model is summarized in [docs/lvd-sampling.md](docs/lvd-sampling.md).

## Important rule

No signal is to be applied to an original watch until the corresponding voltage, polarity, impedance and waveform have been verified against an original receiver with an oscilloscope.

## Repository structure

- `docs/` — research, signal reconstruction and sources
- `hardware/` — universal test station, adapter schematics and PCB work
- `raspberry/` — Raspberry Pi playback and composite-video generation
- `tests/` — oscilloscope captures, test patterns and validation procedures
- `media/` — original diagrams and assets for documentation/video production

## Planned milestones

1. **v0.1 — Interface reconstruction**
2. **v0.2 — Universal CVBS/AV bench**
3. **v0.3 — Raspberry Pi Zero 2 W source**
4. **v0.4 — First protected image on the original watch**
5. **v0.5 — MP4 playback / exhibition mode**
6. **v1.0 — Reproducible display, diagnostic and integration station**

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
