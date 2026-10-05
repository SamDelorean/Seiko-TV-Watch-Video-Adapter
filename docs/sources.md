# Sources and evidence register

This file records the principal research sources used for the interface reconstruction.

## Primary technical sources

### Development of TV-WATCH
M. Toyoda, M. Murata, Y. Wakai — Suwa Seikosha, 1983.

Value:
- system architecture;
- wrist-TV internal blocks;
- VID1 synchronization path;
- VID2 video path;
- PLL/display timing;
- LVD construction and drive method.

Research copy currently retained in the project research archive as:
`107_KJ00001680139.pdf`

### Watch Television Receiver
George Shimakawa, Toshio Kano, Masami Murata — Suwa Seikosha, 1983.

Value:
- receiver architecture;
- synchronization circuitry;
- display timing;
- receiver power conversion context.

Research copy:
`37_112.pdf`

## Supporting technical source

### Matrix Panel With an Active Driving System
US Patent 4,591,848 — Seiko Epson / Suwa Seikosha technology family.

Value:
- video polarity inversion concepts;
- active-matrix drive principles;
- video scaling/bias concepts;
- field-related drive behavior.

Important: this patent is a technology-family source. It must not be treated as proof that every illustrated circuit appears unchanged in the production T001.

Research copy:
`US4591848.pdf`

## Independent reverse engineering

### DG1SFJ / Jochen Huebl — Seiko TV Watch
Value:
- partial power-supply reconstruction;
- measured supply rails;
- connector/interface observations;
- identification of composite sync and analog video.

Reported approximate rails:
- 4.1 V
- 8.9 V
- 13.2 V

Reported interface:
- pin 5: composite sync
- pin 6: analog video / associated DC bias

Caution:
the author explicitly notes that the reconstructed power schematic is not guaranteed to be exact.

## Historical/technical secondary source

### James A. Mahaffey — Suwa Seikosha's Television Watch
NAWCC Bulletin, 2001.

Value:
- connector description;
- system-level interface discussion;
- additional electrical observations.

Use as corroborating evidence, not as a substitute for measurement on the target receiver.

## Original user documentation

### SEIKO T001 instruction manual
Research copy:
`doku-seikotvwatch.pdf`

Useful for:
- system usage;
- original accessories;
- operational constraints;
- model identification.

It is not a service manual.

## Evidence policy

For repository documentation:

- **CONFIRMED** = primary documentation or mutually consistent independent evidence.
- **INFERRED** = technically plausible conclusion supported by architecture.
- **TO MEASURE** = must be measured on original hardware before it becomes a design parameter.

No patent-family circuit is to be labeled as an exact T001 production circuit unless physical or service-document evidence confirms it.
