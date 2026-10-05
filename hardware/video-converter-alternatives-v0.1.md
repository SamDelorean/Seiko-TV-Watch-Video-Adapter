# Alternative Video-Level Converter Designs — V0.1

Status: **three mutually exclusive implementation candidates pending TR02-01 measurement**

## Purpose

The currently reported Seiko pin-6 waveform may result from:

1. a normal video excursion added to a high DC bias;
2. a video signal that is both amplified and biased;
3. an active transistor/amplifier output stage whose operating point happens to sit near the reported voltage.

These cases can look similar on a simple oscilloscope capture but require different replacement circuitry.

This document therefore defines one implementation candidate for each hypothesis.

---

# DESIGN A — DC bias / level translation only

## Use this design if

Measurements show:

- the AC video excursion at Seiko pin 6 is approximately the same as the usable video/luma excursion presented to the receiver;
- the principal difference is the absolute DC operating point;
- polarity is unchanged;
- no significant gain or attenuation is required.

In shorthand:

```text
|G| ≈ 1
```

## Functional topology

```text
CVBS
 |
75-ohm termination
 |
buffer
 |
luma / optional chroma filter
 |
DC restoration / clamp
 |
sync blanking
 |
AC coupling
 |
DC bias insertion
 |
unity-gain output buffer
 |
series protection resistor
 |
Seiko pin 6
```

## Electrical concept

The useful image waveform is preserved at approximately its native amplitude.

A stable reference `VBIAS` is then added:

```text
VOUT(t) = VBIAS + video(t)
```

or, for inverted polarity:

```text
VOUT(t) = VBIAS - video(t)
```

The bias may be established by:

- a precision reference/divider followed by a buffer;
- an op-amp summing/level-shift stage operated at unity signal gain;
- an AC-coupled video waveform biased through a low-impedance reference node.

## Preferred implementation philosophy

Use the **minimum active circuitry necessary**.

If the original receiver does not amplify the picture component, the adapter should not add an unnecessary gain stage.

### Adjustable parameters

- BLACK/BIASED LEVEL
- POLARITY
- optional small trim around unity amplitude

## Advantages

- lowest component count;
- lowest accumulated noise;
- lowest risk of bandwidth distortion;
- easiest to calibrate;
- closest electrical imitation if the receiver simply shifts the operating point.

## WARNING — Design A

**Do not use Design A merely because pin 6 measures near 8 V DC.**

A large DC level does not prove unity video gain.

Before selecting this design, AC-coupled measurements must show that the source-video excursion and Seiko pin-6 excursion are substantially equal.

If the original receiver actually amplifies the video, this design will under-drive contrast.

If the original receiver attenuates the video, this design may over-drive the wrist unit.

A wrong bias voltage may also place the Seiko input outside its intended common-mode range even when the AC amplitude appears safe.

---

# DESIGN B — Gain / attenuation plus DC bias

## Use this design if

Measurements show:

- pin-6 picture excursion is measurably different from the source-video excursion;
- the transfer remains approximately linear;
- the output can still be described by a stable gain plus offset.

In shorthand:

```text
|G| != 1
```

## Functional topology

```text
CVBS
 |
75-ohm termination
 |
buffer
 |
luma / optional chroma filter
 |
DC restoration / clamp
 |
sync blanking
 |
variable linear gain stage
 |
polarity selection / inversion if required
 |
DC level shift
 |
wideband output buffer
 |
series protection resistor
 |
Seiko pin 6
```

## Transfer function

```text
VOUT = VBLACK + G × (VIN - VIN_BLACK)
```

where:

- `VBLACK` sets the Seiko black operating level;
- `G` sets picture amplitude;
- sign of `G` sets polarity.

## Gain architecture

The practical range should be deliberately bounded rather than arbitrary.

Suggested breadboard design range:

```text
|G| ≈ 0.5 ... 3
```

This comfortably covers:

- modest attenuation;
- unity operation;
- approximately 2.1× gain if a 0.7 V input must become ~1.5 V;
- moderate uncertainty in the reported values.

The final production range should be reduced once measurements are known.

## Adjustment strategy

Use two independent trims:

```text
VIDEO LEVEL      -> black/DC point
VIDEO AMPLITUDE  -> white-black excursion
```

A separate polarity jumper/switch is preferable to allowing the operator to sweep continuously through unstable or unintended operating configurations.

## Advantages

- handles the widest plausible linear case;
- easy A00/A01 calibration;
- can emulate amplification, attenuation or unity;
- independent control of black point and contrast.

## WARNING — Design B

**This design has more ways to produce a dangerous but visually plausible waveform.**

An incorrect combination of gain and offset can keep the average voltage near the expected ~8 V while allowing black or white peaks outside the original receiver envelope.

Therefore:

- adjust into a dummy load, not into the watch;
- set gain minimum before first power-up;
- establish black level first;
- then increase amplitude;
- verify absolute minimum and maximum voltage with the oscilloscope;
- use hardware output limiting/protection where practical.

Do not infer safety from average DC voltage alone.

---

# DESIGN C — Active receiver-like output driver

## Use this design if

Measurements or circuit tracing show that the original TR02-01 does not merely sum an offset, but instead drives pin 6 through a transistor/amplifier stage tied to one of its supply rails.

Evidence could include:

- emitter/source follower topology;
- collector/drain load;
- active pull-up/pull-down behavior;
- measurable source impedance characteristic of a transistor stage;
- asymmetrical clipping;
- load-dependent gain/offset;
- pin-6 behavior that cannot be reproduced accurately by a simple linear summing amplifier.

## Functional topology

Example conceptual structure:

```text
CVBS / luma
   |
buffer + clamp
   |
amplitude-setting stage
   |
receiver-like driver transistor
   |
bias/reference network
   |
output protection
   |
Seiko pin 6
```

Possible physical forms:

### C1 — emitter/source follower

```text
video-controlled device
       |
       +----> Seiko pin 6
       |
reference/bias network
```

Useful when the original stage appears primarily to provide low output impedance and DC translation.

### C2 — common-emitter/common-source level translator

Useful if the original receiver inverts the signal or derives the high operating point from a collector/drain load.

### C3 — op-amp/transistor hybrid

A modern precision implementation can reproduce the measured transfer function and output impedance while remaining easier to calibrate than a literal transistor clone.

## Design objective

For Design C, the target is not merely:

```text
same black voltage
same white voltage
```

It should also reproduce:

- source/output impedance;
- transient response;
- load dependence;
- clipping behavior only insofar as it exists in normal operation;
- startup/shutdown behavior;
- safe loss-of-video state.

## Advantages

- closest possible electrical emulation of the original receiver;
- useful if the wrist unit depends on source impedance or dynamic behavior;
- may reproduce subtle loading effects that a laboratory op-amp source would not.

## WARNING — Design C

**Do not build a transistor-level clone merely because it looks historically authentic.**

This is the highest-risk option because the wrong bias network, device polarity, rail connection or source impedance can place the wrist input outside its safe range.

Select Design C only after one or more of the following are available:

- traced original output-stage schematic;
- reliable transistor/node identification;
- measured pin-6 source impedance;
- load-response data;
- startup/shutdown captures.

A visually similar waveform into a high-impedance oscilloscope does not prove that the circuit will behave correctly when connected to the wrist unit.

---

# Decision matrix

| Observation on original TR02-01 | Preferred design |
|---|---|
| AC amplitude essentially unchanged, only DC level shifted | **A — Bias only** |
| Linear amplitude change plus DC level shift | **B — Gain/attenuation + bias** |
| Load-dependent / transistor-driver behavior | **C — Receiver-like active driver** |
| Polarity inverted but otherwise linear | **A or B with inversion** |
| Unknown | **Do not choose yet** |

# Recommended investigation order

The safest engineering order is:

```text
1. test H1 / Design A
2. test H2 / Design B
3. investigate H3 / Design C only if evidence requires it
```

This is not because Design A is assumed correct.

It is because Design A has the fewest degrees of freedom and is easiest to falsify with measurements.

# Common mandatory protections

All three designs require:

- no direct connection to the watch during initial calibration;
- dummy load / high-impedance measurement first;
- current-limited Seiko supply rails;
- output series resistance;
- defined startup/shutdown state;
- defined loss-of-video state;
- test point immediately before the wrist connector;
- verification of absolute min/max pin-6 voltage;
- verification of pin-5 sync levels independently.

# Evidence required to select a design

Minimum data set:

1. A00 black absolute voltage at pin 6;
2. A01 white absolute voltage at pin 6;
3. A02 50% gray absolute voltage at pin 6;
4. AC-coupled black/white excursion;
5. no-video pin-6 DC level;
6. pin-6 source impedance estimate;
7. response to at least two known loads if safe;
8. polarity;
9. horizontal blanking waveform;
10. startup/shutdown transient.

Until this evidence exists, all three designs remain candidates and none should be called the definitive Seiko replacement interface.
