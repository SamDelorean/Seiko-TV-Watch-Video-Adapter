# Game Boy / RP2C02 sync completion — V0.1

Status: **architecture decision / bench validation pending**

Related source project:

- https://github.com/SamDelorean/gameboy-rp2c02-crt-adapter

## Existing signals already available

The Game Boy / RP2C02 project already exposes all timing domains needed to construct a Seiko-compatible interface.

### Game Boy source side

The RP2350 captures:

- `LD0`
- `LD1`
- `CP`
- `CPL`
- `ST`
- `S`

These signals describe the Game Boy LCD source raster and are useful for capture/debugging. They are **not** used directly as the Seiko composite-sync output because the downstream RP2C02 raster is the final video timing domain.

### RP2C02/output side

Available:

- `PPU_CLK_IN` — NTSC PPU master clock
- `PPU_nINT` — RP2C02 VBlank reference
- `PPU_VIDEO_RAW` — RP2C02 pin 21 analog NTSC composite output
- common GND

The RP2C02 composite output is the authoritative source for the Seiko sync branch because it contains the horizontal and vertical timing actually associated with the final video waveform.

## Decision

Derive Seiko pin 5 **Composite Sync** from `PPU_VIDEO_RAW`.

Do not use:

- Game Boy `S` alone — frame timing only and in the source LCD domain;
- Game Boy `CPL`/`ST` alone — source-line timing, not the final NTSC raster;
- RP2C02 `/INT` alone — VBlank/frame reference only, no horizontal sync;
- an independently free-running GPIO sync generator — unnecessary phase-risk.

## V0.1 signal split

```text
RP2C02 pin 21
PPU_VIDEO_RAW
      |
 high-Z / video buffer
      |
      +---------------------------+
      |                           |
      v                           v
 VIDEO branch                SYNC branch
      |                           |
 luma/video conditioning     composite sync separator
 DC bias / gain                   |
      |                      output protection
      v                           v
 Seiko pin 6                  Seiko pin 5
```

Both outputs therefore originate from the same raster and remain phase-coherent.

## Candidate sync separator

An LM1881-class video sync separator is the current low-complexity candidate.

Candidate connection concept:

```text
buffered composite
       |
     AC coupling / optional sync LPF
       |
    LM1881 CVIN
       |
    LM1881 CSOUT
       |
 level/protection stage
       |
   SEIKO pin 5
```

The LM1881 is **not yet frozen as the final component**. It is selected for bench evaluation because it directly extracts composite sync from an NTSC-like composite waveform.

## Why not synthesize sync digitally?

A digital RP2350/PIO generator is technically possible because the project controls the PPU timing environment and already sees `PPU_nINT`.

However it would add:

- horizontal-phase alignment logic;
- reset/startup phase assumptions;
- additional timing validation;
- another failure mode if digital sync and analog video shift relative to each other.

Extracting sync from the actual analog video avoids these problems and is preferred for V0.1.

A PIO-generated sync remains a later optional diagnostic path.

## Protection rule

The sync separator must **not** drive the Seiko directly until the original receiver's pin-5 waveform and input loading are measured.

Initial output stage shall provide:

- defined 5 V-class logic domain only after measurement confirms it;
- series current limiting;
- optional buffer/open-collector stage if required by measured loading;
- a test point before the Seiko connector.

## Bench validation

Measure simultaneously:

1. `PPU_VIDEO_RAW`
2. extracted `CSYNC`
3. original Seiko receiver pin 5 reference waveform

Acceptance criteria:

- horizontal period matches;
- vertical interval structure is preserved;
- polarity matches the original receiver;
- high/low levels remain inside measured Seiko limits;
- added sync-path delay is stable and small relative to the video path;
- no loading-induced distortion appears on `PPU_VIDEO_RAW`.

## Result of this increment

The Game Boy path does **not** require an additional synchronization source.

It requires only a **sync extraction and level/protection block** downstream of the already available RP2C02 composite output.
