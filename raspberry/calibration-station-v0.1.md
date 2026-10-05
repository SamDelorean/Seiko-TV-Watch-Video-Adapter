# Raspberry Pi Seiko Calibration & Diagnostic Station — V0.1

Status: **functional architecture / implementation pending**

## Mission

Treat the Raspberry Pi Zero 2 W not primarily as a media player, but as a dedicated **calibration, diagnostic, restoration and exhibition instrument** for the Seiko TV Watch wrist unit.

The Raspberry Pi feeds standard NTSC CVBS into the universal bench. The bench remains responsible for Seiko-specific power, video bias, sync extraction and protection.

```text
                RASPBERRY PI ZERO 2 W
                         |
          calibration / diagnostic software
                         |
                   hardware CVBS
                         |
                UNIVERSAL CVBS BENCH
                         |
              Seiko power + video + sync
                         |
                  SEIKO WRIST UNIT
```

## Operating modes

### 1. AUTO DIAGNOSTIC

Runs a deterministic sequence of identified patterns for a fixed duration.

Purpose:
- quick functional assessment;
- before/after repair comparison;
- repeatable video documentation;
- oscilloscope correlation.

Each pattern has:
- stable ID;
- pattern name;
- nominal luma range;
- duration;
- optional spoken/logged description;
- timestamp in the station log.

### 2. MANUAL PATTERN

Operator selects one pattern and leaves it on screen indefinitely.

Useful for:
- contrast/brightness adjustment;
- oscilloscope work;
- photography;
- tracing a fault.

### 3. DYNAMIC / RESPONSE TEST

Patterns specifically intended to reveal:
- LCD response time;
- persistence;
- smearing;
- ghosting;
- field/interlace problems;
- horizontal/vertical lock instability.

### 4. SERVICE / MEASUREMENT

Displays patterns with optional ID, frame counter and timing markers.

This mode is intended for:
- receiver comparison;
- sync validation;
- waveform capture;
- repair documentation.

### 5. MEDIA / EXHIBITION

Last-priority diagnostic mode, but high-value demonstration mode.

Supports:
- still image;
- image slideshow;
- MP4/H.264 playback;
- automatic looping;
- later grayscale/gamma preprocessing optimized for the Seiko LVD.

## Rendering architecture

Use two complementary generators.

### A. Project-owned canonical patterns

Generate exact lossless test images and dynamic rasters under project control.

Recommended implementation:
- Python for pattern definition/build tooling;
- Pillow and/or NumPy for static assets;
- later SDL2/KMS direct renderer for appliance-style full-screen output.

Canonical patterns should be generated reproducibly from source rather than stored only as hand-edited bitmap files.

### B. FFmpeg/LAVFI patterns

FFmpeg already provides useful deterministic sources including:
- `color`;
- `testsrc`;
- `testsrc2`;
- `smptebars`;
- `smptehdbars`;
- `rgbtestsrc`;
- `yuvtestsrc`.

Use these as:
- external reference patterns;
- quick smoke tests;
- standard source validation;
- media/tone generation.

Do not make Seiko-specific diagnostics depend exclusively on FFmpeg.

## Why not adopt an existing calibration suite directly?

Projects such as PGenerator+ demonstrate that Raspberry Pi is a strong platform for display calibration and network-controlled pattern generation. However, PGenerator+ targets precision HDMI SDR/HDR/Dolby Vision workflows and is substantially broader than required here.

The Seiko station needs different priorities:
- monochrome analog video;
- very low physical resolution;
- vintage LCD sample-and-hold behavior;
- CVBS / NTSC;
- sync stability;
- restoration diagnosis;
- dead/stuck-cell observation;
- ghosting/persistence;
- reversible museum/collector use.

Therefore external projects are references, not a core runtime dependency.

## Control interface

V0.1 should support at minimum:
- local keyboard;
- simple numbered menu;
- next/previous pattern;
- AUTO sequence start/stop;
- media mode.

Later:
- three or four physical buttons;
- rotary encoder;
- lightweight local web UI;
- remote control from phone/tablet over Wi-Fi.

No web interface is required for first light.

## Logging

Every automatic diagnostic run should optionally record:

```text
date/time
station software version
output norm (NTSC/NTSC-J)
pattern sequence version
pattern ID and start time
user notes
measured Seiko rail values if entered
video gain / bias settings if entered
```

This makes before/after repair results comparable.

## V0.1 implementation principle

The first implementation should remain small and auditable:

```text
pattern definitions
      |
static generator + dynamic renderer
      |
simple menu/sequencer
      |
full-screen KMS/SDL output
      |
Pi hardware composite output
```

Media playback is a separate callable mode and must not complicate the diagnostic renderer.
