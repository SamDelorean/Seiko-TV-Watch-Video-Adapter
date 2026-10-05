# CVBS-to-Seiko Video Level Converter — V0.1

Status: **transfer model defined / physical implementation intentionally open pending TR02-01 measurement**

## Purpose

Convert a normal 75-ohm composite-video source into the separate electrical signals expected by the Seiko TV Watch wrist unit:

- pin 5: composite synchronization;
- pin 6: analog picture signal with the Seiko-required DC operating point and amplitude.

The converter is deliberately **calibratable**. It must not depend on the currently reported ~8 V operating point or ~1.5 V video excursion being exact, and it must not assume that the original receiver obtains those values by voltage gain. The ~8 V may simply be a DC bias/reference onto which an already suitable video excursion is superimposed.

## 1. Input reference model

A conventional standard-definition composite signal is approximately 1 V p-p into 75 ohms:

- synchronization occupies roughly 0.3 V below the blanking reference;
- active picture information occupies roughly 0.7 V above the blanking reference.

Exact black setup/pedestal depends on the source/norm and must not be assumed by the adapter.

Therefore the adapter does not calibrate from nominal IRE alone. It measures or derives two practical source references using the station patterns:

- `VIN_BLACK`: CVBS video level produced by pattern A00;
- `VIN_WHITE`: CVBS video level produced by pattern A01.

The active input excursion is:

```text
ΔVIN = VIN_WHITE - VIN_BLACK
```

## 2. Seiko output model

The corresponding target values are measured on the original TR02-01:

- `VSEIKO_BLACK`: pin-6 voltage with a black raster;
- `VSEIKO_WHITE`: pin-6 voltage with a white raster.

The required picture excursion is:

```text
ΔVSEIKO = VSEIKO_WHITE - VSEIKO_BLACK
```

The sign of `ΔVSEIKO` automatically defines picture polarity.

Current independent reports suggest an operating point near 8 V and a video excursion on the order of 1.5 V, but these are provisional only.

## 3. Competing physical interpretations

At least three circuit interpretations remain plausible until the original TR02-01 is measured:

### H1 — DC bias / level translation only

```text
luma(t) -> AC coupling / clamp -> + VBIAS -> pin 6
```

In this case the picture excursion already has approximately the required amplitude and the receiver mainly establishes a DC operating point near the reported ~8 V.

### H2 — DC bias plus modest gain

```text
luma(t) -> gain K -> + VBIAS -> pin 6
```

Here the receiver changes both amplitude and operating point.

### H3 — active level translator / output driver

The output stage may use a transistor or amplifier referenced to one of the receiver rails. Its observed ~8 V level may then be a consequence of that topology rather than a separately generated "8 V bias source."

These hypotheses are electrically different even though all can produce a waveform that looks like a video signal riding on a high DC level.

## 4. Required transfer function

Regardless of implementation, the external behavior can be represented as an affine transformation:

```text
G = (VSEIKO_WHITE - VSEIKO_BLACK) / (VIN_WHITE - VIN_BLACK)

VOUT = VSEIKO_BLACK + G × (VIN - VIN_BLACK)
```

This equation is a **measurement model**, not proof that the original receiver contains a literal gain stage followed by a summing amplifier.

It separates three observable parameters:

1. **BLACK LEVEL / DC OPERATING POINT** — `VSEIKO_BLACK`;
2. **PICTURE EXCURSION RATIO** — magnitude of `G`;
3. **POLARITY** — sign of `G`.

If measurement shows `|G| ≈ 1`, the preferred implementation should be a unity-gain bias/level-shift stage, not an unnecessary amplifier.

### Nominal illustration only

If the usable input luma excursion were 0.70 V and the Seiko required 1.50 V:

```text
|G| ≈ 1.50 / 0.70 ≈ 2.14
```

If white is above black:

```text
G ≈ +2.14
```

If white is below black:

```text
G ≈ -2.14
```

This is **not** a frozen gain value. Actual A00/A01 measurements replace the nominal 0.70 V assumption.

## 5. Functional video path

```text
CVBS IN
  |
75-ohm termination
  |
wideband unity buffer
  |
  +---------------------------> LM1881 sync branch
  |
  v
optional luma low-pass / chroma rejection
  |
DC restoration / keyed clamp
  |
sync removal / blanking
  |
polarity-selectable amplitude stage
  |
(unity gain preferred if measurement permits)
  |
adjustable DC bias / level shift
  |
output buffer + current limiting
  |
SEIKO PIN 6
```

## 6. Why DC restoration is mandatory

CVBS may be AC-coupled. Once AC-coupled, average picture content changes the apparent DC level unless a reference point is restored.

The converter therefore must not simply:

```text
CVBS -> capacitor -> gain -> +8 V
```

because black level would wander with average picture level.

Instead, the video waveform is clamped to a stable reference before gain/offset conversion.

Preferred V0.1 method:

- use the LM1881 timing outputs to obtain a repeatable back-porch/clamp window;
- restore the blanking/black reference with a keyed clamp or equivalent DC-restoration circuit;
- perform gain and level translation only after the reference is stable.

A simple sync-tip diode clamp is acceptable as an early breadboard comparison, but the keyed method is preferred for calibration work.

## 7. Sync removal

The Seiko interface separates VID1/sync from VID2/video, so the video output should not intentionally reproduce the negative composite-sync pulse.

V0.1 architecture:

```text
restored luma/video ----+---- active picture ----> gain/offset
                       |
LM1881 CSYNC ----------+---- force output to reference during sync
```

An analog switch, clamp or controlled blanking stage can hold the video path at the selected blank/black reference while composite sync is active.

The exact blanking strategy remains subject to comparison with the original TR02-01 pin-6 waveform.

## 8. Chroma rejection

The Seiko display is monochrome.

A normal NTSC composite source contains a color subcarrier near 3.58 MHz. Whether the original TR02-01 delivers significant chroma energy on VID2 is still TO MEASURE.

Therefore V0.1 provides a selectable video filter:

```text
BYPASS
  or
LUMA LPF
```

Initial engineering range for evaluation:

- approximately 1.5 to 2.5 MHz low-pass corner.

Rationale:
- enough bandwidth for the small Seiko matrix;
- significant attenuation of the 3.58-MHz chroma component;
- adjustable/bypassable so the original receiver can determine the final requirement.

No final cutoff is frozen before oscilloscope comparison.

## 9. Sync branch

The same terminated/buffered CVBS signal feeds an LM1881-class separator.

The LM1881 accepts AC-coupled composite video in the approximate 0.5–2 V p-p range and provides:

- composite sync;
- vertical sync;
- burst/back-porch timing;
- odd/even field information.

For the wrist interface only composite sync is mandatory initially.

```text
CVBS BUFFER
   |
AC coupling
   |
LM1881
   |
CSYNC
   |
polarity/level/output-impedance conditioning
   |
SEIKO PIN 5
```

Pin-5 voltage levels remain TO MEASURE.

## 10. Analog supply strategy

The video-conditioning output stage must reproduce the Seiko video operating point, potentially around 8 V with an excursion of approximately 1.5 V. It may need voltage gain, unity gain, attenuation, inversion, or only DC translation; this is intentionally left open until the original receiver is measured.

Therefore the video amplifier must **not** be powered only from 3.3 V or 5 V.

Preferred station architecture:

- separate analog adapter supply, nominally 12–15 V or suitable split rails;
- the Seiko 4.1/8.9/13.2 V power outputs remain separately current-limited loads;
- do not consume the watch's sensitive supply rails as the primary video-amplifier supply unless later measurements justify it.

The selected amplifier must have:
- adequate output swing at the target bias;
- several-MHz small-signal bandwidth;
- sufficient slew rate;
- stable operation at the expected capacitive/cable load;
- low output impedance through an intentional protection resistor.

Component selection is a later increment.

## 11. Controls / calibration points

### Front-panel or internal trims

- `VIDEO LEVEL` — sets `VSEIKO_BLACK`;
- `VIDEO AMPLITUDE` — sets `|G|`; unity gain is preferred if the original receiver shows no meaningful amplitude gain;
- `VIDEO POLARITY` — positive / negative;
- `LUMA FILTER` — bypass / filtered.

### Test points

- `TP_CVBS_IN`
- `TP_CVBS_BUFFERED`
- `TP_LUMA`
- `TP_CLAMPED_VIDEO`
- `TP_VIDEO_PRE_OFFSET`
- `TP_VIDEO_OUT`
- `TP_CSYNC_RAW`
- `TP_CSYNC_OUT`
- `TP_VIDEO_REF`

## 12. Calibration procedure

### Step 1 — characterize source

With the Seiko disconnected:

1. display A00 BLACK;
2. measure `VIN_BLACK`;
3. display A01 WHITE;
4. measure `VIN_WHITE`;
5. record `ΔVIN`.

### Step 2 — characterize original receiver

Using the original TR02-01 with the same known pictures:

1. measure pin-6 black level;
2. measure pin-6 white level;
3. calculate `ΔVSEIKO`;
4. determine polarity;
5. capture pin-6 waveform during horizontal/vertical blanking.

### Step 3 — set adapter without watch

Using oscilloscope/dummy load:

1. set A00;
2. adjust VIDEO LEVEL to `VSEIKO_BLACK`;
3. set A01;
4. adjust VIDEO GAIN until `VOUT = VSEIKO_WHITE`;
5. repeat A00/A01 until offset and gain converge;
6. verify A02 50% gray lies near the expected midpoint;
7. run A03/A04/A05 and verify monotonicity/no clipping.

### Step 4 — protection check

Before connecting the wrist unit:

- verify minimum and maximum VOUT never exceed the original receiver envelope;
- verify loss of CVBS produces a defined safe output;
- verify startup/shutdown transients;
- verify current-limiting resistor/output buffer behavior.


## 13. Distinguishing bias from gain on the real receiver

Use the oscilloscope in both DC- and AC-coupled views.

### DC-coupled measurement

With A00 BLACK, A01 WHITE and A02 50% gray:

- record the absolute pin-6 voltage;
- identify black level;
- identify white level;
- identify the midpoint.

This reveals the operating point and polarity.

### AC-coupled measurement

Repeat the same patterns with the scope channel AC-coupled:

- measure only the picture excursion;
- compare pin-6 p-p amplitude with the demodulated/source video amplitude at the nearest accessible point in the receiver.

Interpretation:

- same amplitude, large DC shift -> primarily **bias/level translation**;
- larger amplitude on pin 6 -> **gain + bias**;
- smaller amplitude on pin 6 -> **attenuation + bias**.

### No-signal measurement

Also record pin 6 with:

- receiver powered but no RF/video;
- valid sync but black picture;
- full black raster.

If the ~8 V level remains with no picture content, that is strong evidence that it is a DC operating bias/reference rather than the result of amplification.

### Schematic/topology evidence

If the receiver can be traced safely, look specifically for:

- coupling capacitor feeding pin-6 driver;
- resistor divider or reference establishing a DC operating point;
- emitter/source follower;
- collector/drain load tied to the ~8.9 V rail;
- op-amp/transistor stage with explicit gain-setting resistors.

This topology evidence should be used together with waveform measurements before choosing the final adapter circuit.

## 14. Fail-safe behavior

Preferred loss-of-video state:

- pin 6 returns to a defined black/blanking reference;
- pin 5 becomes inactive or reproduces the safest state observed from the original receiver;
- no uncontrolled amplifier saturation reaches the watch.

Final fail-safe levels remain TO MEASURE.

## 15. What is already fixed vs still open

### Fixed architecture

- standard 75-ohm CVBS input;
- buffer/split;
- LM1881-derived synchronization;
- restored/clamped video reference;
- separate video and sync outputs;
- affine external behavior, implemented with the minimum necessary amplitude change plus DC bias/translation;
- selectable polarity;
- selectable chroma filtering;
- protected outputs.

### Still open

- exact Seiko black voltage;
- exact Seiko white voltage;
- exact video polarity;
- pin-6 load/input impedance;
- required source impedance;
- exact luma filter cutoff;
- pin-5 logic levels/load;
- final amplifier and analog-switch part numbers;
- final resistor/capacitor values.

Those measurements determine component values, not the overall topology.
