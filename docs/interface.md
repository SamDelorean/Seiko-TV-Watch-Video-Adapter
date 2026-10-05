# Seiko TV Watch external interface — working reconstruction

Status: **v0.1 research baseline**

This document records only the interface between the original pocket receiver and the wristwatch. It intentionally separates documented facts from engineering inference and measurements still required.

## 1. Connector model

Current evidence supports a **six-conductor electrical interface** plus a possible additional chassis-ground contact associated with the connector mechanics.

### Working pinout

| Pin | Working assignment | Evidence status | Notes |
|---|---|---|---|
| 1 | +8.9 V rail | CONFIRMED / VERIFY | Independent reverse-engineering measurement |
| 2 | +13.2 V rail | CONFIRMED / VERIFY | Independent reverse-engineering measurement |
| 3 | +4.1 V rail | CONFIRMED / VERIFY | Independent reverse-engineering measurement |
| 4 | Electrical ground | CONFIRMED | Signal/power reference |
| 5 | Composite Sync | CONFIRMED | Exact amplitude, duty and vertical interval still to capture |
| 6 | Analog video + bias | CONFIRMED | Exact transfer function and load still to characterize |

A separate connector/chassis contact has been described as chassis ground. Its electrical relationship to pin 4 must be checked on the actual hardware.

## 2. Functional architecture

The external receiver appears to perform RF reception and demodulation, then sends two principal information signals to the watch:

- a synchronization signal;
- an analog luminance/video signal.

The watch itself contains the timing/control and panel-driving electronics.

Primary technical documentation from Suwa Seikosha describes two receiver-to-watch signals:

- **VID1**: synchronization information, further separated into horizontal and vertical synchronization inside the wrist unit;
- **VID2**: video signal, amplified in the wrist unit and switched in polarity by field before driving the LVD.

The wrist unit generates display clocks internally. Reported values include approximately:

- horizontal/display-line synchronization: ~15.7 kHz;
- X-direction panel clock CLx: ~750 kHz, four-phase;
- Y-direction clock CLy: ~15.7 kHz, two-phase.

This strongly supports the conclusion that the external link is **not a raw digital pixel bus**.

## 3. Electrical values currently available

Independent reverse-engineering documentation reports approximately:

- 4.1 V
- 8.9 V
- 13.2 V

for the receiver-generated supply rails.

Additional reported interface values:

- pin 5: composite synchronization;
- pin 6: analog video with a substantial DC bias;
- sync described as active-low and roughly logic-level amplitude;
- video described around an ~8 V DC operating point with approximately ~1.5 V video excursion.

These waveform values are **not yet accepted as design limits**. They must be reproduced on the original receiver under controlled test conditions.

## 4. Measurements required before connecting a prototype

The following are mandatory before driving an original watch:

### Power
- pin 1 DC voltage under load
- pin 2 DC voltage under load
- pin 3 DC voltage under load
- current consumption on each rail
- startup order/transient behavior
- relationship between pin 4 ground and chassis ground

### Pin 5 — Sync
- low and high levels
- source impedance
- horizontal period
- pulse width
- vertical synchronization interval
- polarity
- behavior during loss of video

### Pin 6 — Video
- black level
- white level
- blanking level
- DC bias/pedestal
- peak-to-peak amplitude
- polarity
- source impedance
- input impedance presented by the wristwatch
- field-to-field behavior, if any occurs before the signal reaches the watch

## 5. Recommended characterization patterns

Feed the original receiver with known NTSC patterns and record pins 5 and 6 simultaneously:

1. black raster
2. white raster
3. 50% gray
4. vertical bars
5. horizontal bars
6. checkerboard
7. standard color bars if a monochrome-equivalent luminance reference is useful
8. signal loss / no RF input

Capture at least one complete vertical field and several horizontal lines.

## 6. Prototype architecture

Preferred first prototype:

```text
Raspberry Pi Zero 2 W
        |
decoded MP4
        |
NTSC/composite output
        |
+-----------------------------+
| analog interface            |
| - luminance scaling         |
| - DC restoration / bias     |
| - sync extraction/conditioning
| - output protection         |
+-----------------------------+
        |
+-----------------------------+
| power section               |
| 4.1 V / 8.9 V / 13.2 V     |
| current limiting            |
| soft-start / protection     |
+-----------------------------+
        |
original Seiko connector
        |
Seiko TV Watch
```

## 7. Design rule

The adapter must emulate the receiver, not redesign the wristwatch.

No direct connection from a Raspberry Pi or microcontroller GPIO to pins 5 or 6 is permitted in the design. Signal conditioning and protection are mandatory.

## 8. Open questions

- Exact numbering/orientation of the physical connector when viewed from each side.
- Exact waveform and impedance of pin 5.
- Exact polarity, pedestal and impedance of pin 6.
- Whether all three supply rails are continuously required or conditionally switched.
- Startup/shutdown sequencing.
- Whether the chassis contact must be tied directly to signal ground in the emulator.

These are the blocking questions for **v0.2 bench electrical emulator**.
