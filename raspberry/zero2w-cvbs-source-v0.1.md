# Raspberry Pi Zero 2 W CVBS Source — V0.1

Status: **first modern-source implementation**

## Why Zero 2 W

The Raspberry Pi Zero 2 W is a compact source capable of decoding ordinary media files while still exposing a hardware composite-video output.

Current Raspberry Pi documentation identifies a `TV` composite-video test pad on the underside of the Zero 2 W together with nearby ground pads.

This makes it a natural source for the universal Seiko CVBS bench.

## Functional chain

```text
MP4 / still image / test pattern
          |
 Raspberry Pi Zero 2 W
          |
 hardware composite TV output
          |
       TV pad
          |
     CVBS cable
          |
 UNIVERSAL CVBS TEST STATION
          |
   +------+------+
   |             |
 Seiko VIDEO   Seiko CSYNC
 pin 6         pin 5
          |
      Seiko watch
```

The Raspberry Pi does **not** need to generate a separate GPIO sync signal in the baseline design.

The station extracts sync from the same composite waveform, guaranteeing source-level video/sync coherence.

## Physical video output

Zero 2 W test pads documented by Raspberry Pi include:

- `TV` — composite video output;
- `GND` — nearby ground.

The first hardware prototype should solder a short coaxial or twisted/shielded pigtail from the TV/GND pads to an RCA connector or directly to the bench CVBS input.

Keep the lead short and preserve a solid ground reference.

## Current Raspberry Pi OS configuration

With the current DRM/KMS Raspberry Pi display stack, composite video is enabled through the KMS composite output configuration.

Working baseline to validate on the actual software image:

`/boot/firmware/config.txt`

```text
enable_tvout=1
dtoverlay=vc4-kms-v3d,composite
```

For a normal NTSC target, the default composite mode is NTSC. The video norm can be set explicitly from the kernel command line where desired:

```text
vc4.tv_norm=NTSC
```

The exact existing `dtoverlay` line should be edited rather than duplicated.

## NTSC vs NTSC-J

The station should eventually test both:

- NTSC;
- NTSC-J.

For a T001/TR02-01 US receiver reference, normal NTSC is the natural first baseline.

Because the universal bench independently conditions the video level and DC bias presented to Seiko pin 6, differences in source pedestal can later be normalized by the interface if required.

Do not use this as a substitute for measuring the original receiver.

## Test sequence

Before MP4 playback, use deterministic patterns.

### Stage R1 — static black

Purpose:
- prove stable composite output;
- verify sync extraction;
- establish black/blanking reference.

### Stage R2 — white field

Purpose:
- measure available luminance swing;
- set maximum safe Seiko video excursion.

### Stage R3 — grayscale ramp

Purpose:
- map source luma to visible Seiko gray levels;
- adjust gain and offset.

### Stage R4 — vertical bars / checkerboard

Purpose:
- evaluate horizontal sampling and effective resolution;
- observe edge behavior.

### Stage R5 — moving pattern

Purpose:
- verify stable frame/field tracking.

### Stage R6 — MP4

Purpose:
- demonstrate arbitrary modern media playback after the electrical interface is already validated.

## Audio

Zero 2 W does not provide a normal analog AV headphone jack as part of the compact board interface used here.

Audio is optional and separate from the Seiko watch connector.

For a self-contained display station, use one of:

- small USB audio adapter;
- I2S DAC / headphone module;
- external media/audio device.

Feed that audio into the universal station's independent audio input/volume/headphone path.

## Media-processing policy

Do not optimize media for the tiny Seiko panel until the electrical path is stable.

Later software work may add:

- grayscale conversion;
- contrast/gamma shaping;
- aspect-ratio control;
- crop/letterbox;
- prefiltering for the ~152 x 210 panel;
- subtitles/text optimized for low resolution;
- automatic looping for exhibition.

These are presentation improvements, not requirements for first-light testing.

## V0.1 acceptance

The Raspberry source is accepted when:

- Zero 2 W boots reliably with composite output enabled;
- TV pad produces stable NTSC CVBS;
- the universal station extracts stable CSYNC;
- static black/white/gray patterns are reproducible;
- no separate GPIO sync generator is needed.
