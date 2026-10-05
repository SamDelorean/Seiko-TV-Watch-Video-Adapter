# Game Boy RP2C02 integration note

Related project: **SamDelorean/gameboy-rp2c02-crt-adapter**

The Game Boy project currently models the path:

```text
Game Boy 160x144 / four logical shades
  -> project scaler/bridge
  -> RP2C02-class video stage
  -> NTSC composite
```

For the Seiko TV Watch, the useful interface is the NTSC composite stage.

## Why

The original DMG LCD-side signals (LD0/LD1 and timing signals such as CP/CPL/ST/S) are digital LCD-driving information, not the analog video level expected at the Seiko receiver connector.

By contrast, an RP2C02-class PPU generates an analog NTSC composite signal. That signal contains the common timing reference needed for both the Seiko video and sync branches.

## Proposed reuse

No change is required to the Game Boy image-generation model solely for the Seiko.

The Seiko-specific adapter is downstream:

```text
RP2C02 VOUT
   |
   +--> sync separator --> level/protection --> Seiko pin 5
   |
   +--> video/luma path --> gain + DC shift + protection --> Seiko pin 6
```

A sync separator such as an LM1881-class circuit is a candidate, but no component is frozen until the original pin-5 waveform is measured.

## Repository relationship

Keep both repositories independent.

This Seiko repository references the Game Boy project as an optional source implementation. A Git submodule is unnecessary until code or hardware files must actually be consumed at build time.

This avoids coupling the Seiko adapter to one video source: the same interface can later accept Raspberry Pi or other NTSC sources.
