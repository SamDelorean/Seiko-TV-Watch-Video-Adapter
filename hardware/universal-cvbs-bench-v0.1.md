# Universal CVBS / AV Test Station — V0.1

Status: **architecture frozen at block level / electrical values pending bench characterization**

## Purpose

Build one reversible bench interface that accepts a normal analog composite-video source and presents the electrical signals required by the Seiko TV Watch.

The station is intended for:

- diagnosis;
- repair;
- interface characterization;
- exhibition;
- test-pattern injection;
- Game Boy / RP2C02 experiments;
- Raspberry Pi playback;
- other NTSC-compatible video sources.

It is not a permanent replacement for the original receiver.

## Universal front-end concept

```text
                 STANDARD SOURCE
             video CVBS + optional audio
                        |
          +-------------+-------------+
          |                           |
          v                           v
      CVBS INPUT                  AUDIO INPUT
          |                           |
  selectable 75-ohm term.        passive/active
          |                     audio passthrough
          v                           |
      high-Z buffer                   v
          |                    headphones / amp
          |
          +-------------------------------+
          |                               |
          v                               v
     VIDEO branch                    SYNC branch
          |                               |
  luma/video conditioning             LM1881-class
  gain + DC offset                       |
          |                         CSYNC conditioning
          v                               v
     Seiko pin 6                     Seiko pin 5

   independent current-limited power rails
      4.1 V / 8.9 V / 13.2 V
                 |
           Seiko pins 3/1/2
                 |
               GND
                 |
           Seiko pin 4
```

## 1. Standard composite-video input

Input connector:

- RCA or BNC CVBS input;
- nominal standard composite-video source;
- common ground.

### Selectable termination

Provide a front-panel or internal jumper/switch:

- **75 OHM** — normal mode for a standard CVBS source;
- **HI-Z** — measurement/probing mode where the station must not additionally terminate a source already loaded elsewhere.

The sync separator input itself is high impedance and must not be relied upon as the 75-ohm video load.

Recommended test point:

- `TP_CVBS_IN`

## 2. Buffer / splitter

The terminated CVBS node feeds a high-input-impedance video buffer before the two functional branches.

Reasons:

- isolate the external video source;
- prevent the Seiko-conditioning branch from changing source termination;
- prevent the sync separator from affecting the video path;
- provide a stable test node.

Outputs:

- `CVBS_BUFFERED_VIDEO`
- `CVBS_BUFFERED_SYNC_FEED`

## 3. Sync branch

Baseline:

```text
CVBS_BUFFERED
     |
 AC coupling / input network
     |
 LM1881-class sync separator
     |
 raw CSYNC
     |
 configurable level/protection stage
     |
 Seiko pin 5
```

The LM1881 is selected as the first bench candidate because it extracts composite sync directly from standard NTSC/PAL-like composite video.

The standalone first-build bench circuit is documented in [`lm1881-test-circuit-v0.1.md`](lm1881-test-circuit-v0.1.md) and follows TI's Typical Connection Diagram before any Seiko-specific output-level adaptation.

Required test points:

- `TP_SYNC_RAW`
- `TP_SYNC_OUT`

### Important

The final Seiko pin-5 level, output impedance and protection values remain **TO MEASURE** on the original receiver.

No direct unprotected connection is permitted before that measurement.

## 4. Video branch

The video branch must convert standard CVBS amplitude/reference into the measured Seiko pin-6 waveform.

Baseline functions:

1. buffer;
2. remove or ignore the composite sync component as required;
3. optionally attenuate chroma / retain luminance;
4. set video gain;
5. establish the measured Seiko black/blanking DC level;
6. add the video excursion in the measured polarity;
7. current-limit/protect the output.

Conceptually:

```text
standard CVBS
    |
 luma/video extraction
    |
 adjustable gain
    |
 adjustable DC offset
    |
 protected output
    |
 Seiko pin 6
```

The reported ~8 V DC bias and ~1.5 V video excursion are **working evidence, not frozen design values**.

The detailed transfer-function and calibration design is documented in [`cvbs-to-seiko-level-converter-v0.1.md`](cvbs-to-seiko-level-converter-v0.1.md).

Required test points:

- `TP_VIDEO_AC`
- `TP_VIDEO_BIAS`
- `TP_VIDEO_OUT`

## 5. Power module

Initial bench implementation deliberately uses three independent regulated, current-limited supplies or modules.

Working nominal rails:

| Seiko pin | Nominal rail | Status |
|---|---:|---|
| 1 | ~8.9 V | verify under load |
| 2 | ~13.2 V | verify under load |
| 3 | ~4.1 V | verify under load |
| 4 | GND | common reference |

Each rail should provide:

- voltage adjustment or accurately fixed output;
- current limiting;
- individual test point;
- individual enable where practical;
- visible power state;
- fuse/PTC or equivalent secondary protection where useful.

Current limits and sequencing are not frozen until measured on the original receiver/watch pair.

## 6. Audio path

Audio is treated as a **separate station function**.

The six-conductor watch video connector under study carries power, sync, video and ground; the original system handles headphone audio at the receiver.

The universal station may therefore provide:

```text
LINE AUDIO IN
     |
 volume / optional headphone amp
     |
 HEADPHONE OUT
```

This makes the station functionally similar to the original receiver for demonstration while keeping audio electrically independent from the watch connector.

Mono or stereo can be supported at the station level; TV program audio may still be mono depending on source.

## 7. Suggested front panel

Inputs:
- VIDEO IN (RCA/BNC)
- AUDIO IN L/R or stereo 3.5 mm
- DC input / bench supply input

Controls:
- VIDEO termination: 75 OHM / HI-Z
- watch power enable
- rail enables if implemented
- video gain trim
- video DC/black-level trim
- audio volume

Outputs:
- original/reversible Seiko watch connector
- headphone output

Test points:
- GND
- CVBS input
- buffered CVBS
- raw CSYNC
- conditioned CSYNC
- raw/luma video
- conditioned video
- 4.1 V
- 8.9 V
- 13.2 V

## 8. Source independence

Any source that supplies valid composite video can use the same station:

```text
Game Boy / RP2C02 ----\
Raspberry Pi ----------+--> UNIVERSAL CVBS BENCH --> Seiko TV Watch
DVD / camera ----------/
pattern generator -----/
```

No source-specific Seiko interface should be required unless later bench evidence proves otherwise.

## 9. V0.1 acceptance

V0.1 is complete when the bench can, without the watch connected:

- terminate and buffer a standard CVBS input correctly;
- recover stable composite sync;
- produce adjustable protected video bias/amplitude;
- provide the three protected supply rails;
- expose all critical signals on test points;
- compare its outputs against the original Seiko receiver on an oscilloscope.
