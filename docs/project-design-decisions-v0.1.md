# Project Design Decisions and Ideas — V0.1

Status: **authoritative project idea/decision log**

This file exists so that important engineering ideas do not remain only in chat history. It records the current project direction, alternatives, hypotheses, safety rules and deferred implementation paths.

---

## 1. Project identity

The project is **not** presented as a permanent replacement for the original Seiko TV Watch receiver.

It is a reversible modern:

- display station;
- calibration station;
- diagnostic bench;
- repair/restoration aid;
- interface-characterization platform;
- modern-source integration platform;
- exhibition/museum/collector tool.

The original receiver remains historically significant and should not be treated as obsolete or disposable.

The wrist unit should remain unmodified wherever practical.

---

## 2. Preservation rule

Preferred implementation:

```text
modern source / test source
        |
external reversible station
        |
original Seiko connector
        |
original wrist unit
```

No destructive modification of the watch is part of the baseline design.

Any replacement or modern interface should be removable.

---

## 3. Working Seiko interface model

Current working connector interpretation:

| Pin | Function | Status |
|---|---|---|
| 1 | ~8.9 V supply | verify on original unit |
| 2 | ~13.2 V supply | verify on original unit |
| 3 | ~4.1 V supply | verify on original unit |
| 4 | electrical GND | confirmed function |
| 5 | composite sync / VID1 | exact levels/impedance to measure |
| 6 | analog video / VID2 with DC operating point | exact transfer to measure |
| extra contact | chassis ground | verify |

The external connection is treated as analog video + separate sync + power rails, not as a proprietary digital pixel bus.

---

## 4. Display architecture interpretation

Primary technical documentation indicates the wrist unit itself:

- separates H/V timing from VID1;
- generates panel clocks internally;
- amplifies/conditions VID2;
- writes analog levels into the active-matrix LVD cells;
- uses storage capacitors / sample-and-hold behavior.

Therefore the external adapter does **not** need to generate a 152 x 210 digital pixel bus.

The watch performs the final analog raster-to-panel sampling internally.

---

## 5. Universal CVBS bench concept

The core station is source-independent.

```text
Game Boy / RP2C02 ----\
Raspberry Pi ----------+--> standard CVBS input
DVD / camera ----------/
pattern generator -----/
                             |
                             v
                    UNIVERSAL CVBS BENCH
                    - 75-ohm / Hi-Z input
                    - buffer/splitter
                    - sync extraction
                    - video conditioning
                    - Seiko power rails
                    - independent audio path
                             |
                             v
                        Seiko watch
```

The Seiko-side electronics should not be redesigned for every source.

---

## 6. Audio concept

Audio is handled as a separate station function.

The wrist connector under study is treated as power + sync + video + ground.

Optional station audio path:

```text
LINE AUDIO IN
     |
volume / headphone amp
     |
HEADPHONE OUT
```

This allows the modern station to behave more like the original receiver during exhibition without mixing audio into the wrist connector.

---

## 7. Game Boy / RP2C02 source

Related project:

`SamDelorean/gameboy-rp2c02-crt-adapter`

The useful Seiko integration point is the **RP2C02 composite output**, not the raw Game Boy LCD signals.

Available source-side Game Boy signals include:

- LD0
- LD1
- CP
- CPL
- ST
- S

These are useful for Game Boy capture/timing but are not the preferred Seiko sync source.

The preferred path is:

```text
RP2C02 VOUT / PPU_VIDEO_RAW
         |
         +--> video branch --> Seiko pin 6
         |
         +--> sync separator --> Seiko pin 5
```

Reason: video and sync then originate from the same final raster and remain phase-coherent.

Do not use RP2C02 /INT alone as Seiko composite sync; it is only a VBlank/frame reference.

---

## 8. LM1881 sync-separator idea

The first sync-separator candidate is LM1881-class.

Purpose:

```text
standard CVBS
    |
LM1881
    |
composite sync
    |
later Seiko-specific level/output stage
```

The LM1881 output is **not** assumed to be directly compatible with Seiko pin 5.

Before connection to the watch, TR02-01 pin 5 must be measured for:

- high level;
- low level;
- polarity;
- pulse width;
- source impedance;
- load current;
- no-signal behavior.

A standalone LM1881 test circuit has been defined from the TI datasheet typical application.

---

## 9. LM1881 test-bench details

First bench implementation:

- VCC = 5 V;
- 0.1 uF AC-coupling capacitor to CVIN;
- 680 kOhm RSET;
- 0.1 uF on RSET node;
- 0.1 uF local VCC bypass;
- switchable 75-Ohm CVBS termination;
- test points on CVBS, CSYNC, VSYNC and BACK PORCH.

Optional TI-derived input filter:

```text
CVBS -- 620 Ohm --+--> LM1881
                  |
                510 pF
                  |
                 GND
```

Keep this filter switchable/bypassable.

The LM1881 back-porch output is considered useful for later keyed-clamp/DC-restoration work.

---

## 10. Raspberry Pi Zero 2 W source

The Raspberry Pi is treated as the first modern general-purpose source.

Preferred source path:

```text
test pattern / still / MP4
          |
Pi Zero 2 W
          |
hardware composite TV output
          |
universal CVBS bench
          |
Seiko
```

No independent GPIO sync generator is required in the baseline design.

Sync should be derived from the same CVBS waveform.

---

## 11. Raspberry as calibration instrument

The Raspberry is not primarily a media player.

It is a dedicated Seiko calibration/diagnostic appliance with modes for:

- AUTO DIAGNOSTIC;
- MANUAL PATTERN;
- DYNAMIC / RESPONSE TEST;
- SERVICE / MEASUREMENT;
- MEDIA / EXHIBITION.

The engineering sequence prioritizes deterministic patterns before arbitrary video playback.

---

## 12. Diagnostic pattern families

### Luminance / clipping

- full black;
- full white;
- 50% gray;
- grayscale steps;
- horizontal grayscale ramp;
- vertical grayscale ramp;
- near-black / PLUGE;
- near-white.

### Geometry

- border / overscan;
- center cross;
- circle + cross;
- coarse grid;
- fine grid;
- corner markers.

### Effective resolution

- vertical line pairs;
- horizontal line pairs;
- checkerboard series;
- dot grid;
- optional spatial-frequency sweep.

### Defect search

- black field;
- white field;
- gray fields;
- slow black/white inversion;
- scanning bright/dark block.

### Temporal behavior

- black/white step;
- 25/75% step;
- moving vertical bar;
- moving horizontal bar;
- moving box;
- checkerboard phase toggle.

### Sync / field behavior

- fixed lock frame;
- extreme-luma sync stress;
- movable horizontal line;
- odd/even field/interlace patterns.

### Chroma investigation

- SMPTE bars;
- equal-luma chroma test;
- luma-only equivalent.

### Real content

- reference still;
- low-contrast still;
- motion reference;
- MP4 playback.

---

## 13. Pixel-defect caution

Do not call one Raspberry source pixel one Seiko physical pixel until the raster-to-LVD sampling map is measured.

Use:

- **source pixel / source line** for Raspberry raster;
- **LVD cell** for the physical Seiko display element.

Later, a calibrated scan pattern can map source coordinates to actual LVD cells.

---

## 14. Implemented A00-A07 generator

The first executable pattern set is implemented in:

`raspberry/calibration_station/`

Patterns:

- A00 BLACK;
- A01 WHITE;
- A02 MIDGRAY;
- A03 11-step grayscale;
- A04 horizontal ramp;
- A05 vertical ramp;
- A06 near-black;
- A07 near-white.

Canonical assets are lossless PGM/P5 grayscale.

The generator produces SHA-256 hashes and a manifest so tests are reproducible.

Manual and timed AUTO modes are implemented separately from the pattern definitions.

The current display frontend is replaceable and must not become part of the pattern definition.

---

## 15. Pin-6 central uncertainty

The reported pin-6 waveform near ~8 V with ~1.5 V video excursion does **not** prove that the receiver amplifies a normal 0.7-V luma signal up to 1.5 V.

The observed waveform may arise from:

### H1 — bias / level translation only

```text
video(t) + fixed DC operating point
```

### H2 — gain/attenuation plus bias

```text
K * video(t) + fixed DC operating point
```

### H3 — active receiver-like driver

A transistor/amplifier output stage tied to one of the receiver rails may create the observed level, impedance and polarity.

All three remain candidates until measurement.

---

## 16. Three alternative pin-6 converter designs

### Design A — bias only

Choose only if AC measurements show approximately unity picture amplitude.

Preferred philosophy:
- minimum active circuitry;
- restore/clamp reference;
- remove sync as required;
- add correct DC bias;
- unity buffer.

**Warning:** large DC offset alone is not evidence that unity gain is correct.

### Design B — gain/attenuation + bias

Choose if the pin-6 picture excursion differs linearly from the source.

Use:
- independent VIDEO LEVEL;
- independent VIDEO AMPLITUDE;
- explicit polarity selection;
- bounded gain range.

**Warning:** correct average DC level does not guarantee safe peak voltages.

### Design C — receiver-like active driver

Choose only if measurement/circuit tracing shows source impedance, load dependence or transistor-stage behavior matters.

Possible implementations:
- emitter/source follower;
- common-emitter/common-source translator;
- modern op-amp/transistor equivalent.

**Warning:** a correct waveform into a high-impedance scope does not prove correct behavior under watch load.

---

## 16A. Controlled A/B conditioning bench

A concrete comparison circuit is now defined in:

`hardware/video-conditioning-dual-path-test-v0.1.md`

It uses one common downstream keyed-bias/output section and switches only the video slope:

```text
MODE A = UNITY + BIAS
MODE B = 2.15x + BIAS (initial provisional test value)
```

This keeps the experimental variables orthogonal. The first test does not simultaneously vary polarity.

Candidate bench devices currently documented:

- OPA810-class wideband RRIO video amplifier/buffer;
- OPA197-class precision bias-reference buffer;
- TMUX621x-class high-voltage logic-controlled clamp switch.

These are candidates only and remain subject to real-hardware validation.

## 17. Decision order for pin-6 design

Engineering order:

```text
1. attempt to prove/refute Design A
2. use Design B if amplitude transformation is real
3. use Design C only if source/load behavior requires it
```

This order minimizes unnecessary complexity.

---

## 18. Pin-6 measurement method

Use both DC-coupled and AC-coupled oscilloscope measurements.

Patterns:

- A00 black;
- A01 white;
- A02 50% gray.

Measure:

- absolute black voltage;
- absolute white voltage;
- midpoint;
- AC picture excursion;
- polarity;
- no-video DC level.

Interpretation:

```text
same AC amplitude + large DC shift
    -> primarily bias/translation

larger pin-6 AC amplitude
    -> gain + bias

smaller pin-6 AC amplitude
    -> attenuation + bias
```

Also trace the original output topology if safely possible.

---

## 19. External transfer-function model

Even before knowing the original topology, the observed behavior can be represented as:

```text
G = (VSEIKO_WHITE - VSEIKO_BLACK)
    / (VIN_WHITE - VIN_BLACK)

VOUT = VSEIKO_BLACK + G * (VIN - VIN_BLACK)
```

This is a **measurement model**, not proof of a literal internal amplifier.

If `|G| ≈ 1`, prefer unity-gain level translation.

---

## 20. DC restoration

Do not simply AC-couple video, amplify it, and add a fixed voltage.

Average-picture-level changes can move the apparent black level.

Preferred architecture:

```text
CVBS
 |
buffer
 |
luma extraction
 |
keyed clamp / DC restoration
 |
sync blanking
 |
minimum necessary amplitude transformation
 |
DC bias/level shift
 |
protected output
```

The LM1881 back-porch timing may be used as the clamp key.

---

## 21. Sync removal from the video branch

Because the Seiko has separate sync and video conductors, do not assume pin 6 should contain normal negative composite-sync pulses.

Candidate approach:

- use LM1881 CSYNC to blank/hold the video path at a reference level during sync;
- compare resulting waveform against original TR02-01 pin 6.

Final behavior must follow measured receiver evidence.

---

## 22. Chroma handling

The Seiko display is monochrome.

The project must determine whether original VID2 contains meaningful 3.58-MHz NTSC chroma energy.

Test:

- feed color bars to original receiver;
- inspect pin 6 spectrum/waveform;
- compare against luma-only reference.

Candidate adapter options:

- BYPASS;
- selectable luma low-pass.

A provisional 1.5–2.5 MHz low-pass evaluation range was proposed, but no final cutoff is frozen.

---

## 23. Power strategy

Initial watch power is supplied by three independent current-limited rails near:

- 4.1 V;
- 8.9 V;
- 13.2 V.

Actual values, currents and startup behavior must be measured on the original system.

The video-conditioning circuitry should preferably use its own analog supply rather than consume the watch's sensitive supply rails.

Commercial regulator modules may later be used as black-box blocks if:

- ripple is acceptable;
- common reference is correct;
- startup/shutdown behavior is safe;
- current limiting/protection is retained.

---

## 24. Mandatory original-receiver measurements

Before connecting the experimental station to the wrist unit, measure:

### Power
- all three rails under load;
- current consumption;
- startup transients/order;
- ground/chassis relationship.

### Pin 5
- high/low voltage;
- polarity;
- source impedance;
- horizontal period;
- pulse width;
- vertical interval;
- no-video behavior.

### Pin 6
- black;
- white;
- blanking;
- DC operating point;
- p-p excursion;
- polarity;
- source impedance;
- watch input impedance;
- field behavior;
- chroma/burst content.

Capture at least:
- several horizontal lines;
- one complete vertical field.

---

## 25. Safety rule

No signal is applied to an original watch until its voltage, polarity, impedance and waveform have been compared with the original receiver.

First validation occurs:

1. disconnected from watch;
2. into test points/dummy load;
3. under oscilloscope;
4. with current limiting;
5. with absolute min/max output checked.

---

## 26. Preferred staged watch connection

When electrical characterization is complete:

```text
1. power only
2. sync only, if verified safe
3. black video
4. gray
5. grayscale ramp
6. static geometry/pattern
7. moving pattern
8. real media
```

Every stage is reversible and has a STOP criterion.

---

## 27. Source-independence principle

The long-term bench should accept any valid CVBS source.

Examples:

- Game Boy / RP2C02;
- Raspberry Pi;
- DVD player;
- camera;
- external pattern generator;
- other NTSC source.

The source-specific project should end at standard CVBS wherever practical.

---

## 28. Repository role

This repository is the authoritative engineering bitácora for:

- architecture;
- interfaces;
- hypotheses;
- circuit candidates;
- test procedures;
- source integration;
- safety rules;
- calibration software.

Historical/original source documents may remain in Drive, but design decisions should be copied into Git documentation.

---

## 29. Open decisions

Still intentionally unresolved:

- exact physical connector orientation;
- exact pin-5 output conditioning;
- exact pin-6 design A/B/C selection;
- exact pin-6 black/white voltages;
- exact polarity;
- exact source/load impedances;
- final luma-filter cutoff;
- final op-amp/transistor choices;
- final regulator choices;
- final startup/shutdown sequencing;
- final enclosure/front-panel implementation.

These are unresolved because they require measurements, not because they were forgotten.

---

## 30. Rule for future ideas

Any new architectural idea, discarded alternative, safety constraint or test concept that materially changes the project should be added to Git documentation rather than left only in chat history.
