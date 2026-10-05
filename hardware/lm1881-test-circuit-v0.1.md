# LM1881 Datasheet Test Circuit — V0.1

Status: **bench circuit / based directly on TI typical connection**

Primary reference:

- Texas Instruments, **LM1881 Video Sync Separator**, SNLS384G.
- Core values below follow the datasheet Typical Connection Diagram.
- Additional bench protection/termination parts are clearly identified as project additions.

## 1. Purpose

Validate sync extraction from a standard CVBS source before any connection to the Seiko TV Watch.

This circuit is intentionally independent of the Seiko output-level circuitry.

The first acceptance target is only:

```text
CVBS IN -> LM1881 -> clean composite sync on CSOUT
```

## 2. Datasheet-core circuit

TI's typical connection uses:

- pin 1 — Composite Sync Output;
- pin 2 — Composite Video Input through 0.1 uF series coupling capacitor;
- pin 3 — Vertical Sync Output;
- pin 4 — Ground;
- pin 5 — Burst / Back Porch Output;
- pin 6 — RSET node with 680 kOhm to ground and 0.1 uF to ground;
- pin 7 — Odd / Even Output;
- pin 8 — VCC, 5 to 12 V.

For this project the first bench test will use **5 V**.

## 3. Proposed breadboard schematic

```text
                          +5 V
                           |
                       +---+--------------------+
                       |                        |
                     C3 0.1 uF                 |
                       |                        |
                      GND                  pin 8 VCC
                                                |
                                         +-------------+
CVBS IN --+-- RTERM 75R -- GND           |    LM1881   |
          |                              |             |
          +-- TP_CVBS_IN                 |         1 --+---- TP_CSYNC
          |                              |             |
          +-- C1 0.1 uF -----------------+-- 2      7 --+---- TP_ODD_EVEN
                                         |             |
                              TP_VSYNC ---+-- 3      6 --+----+---- R1 680k ---- GND
                                         |             |    |
                                  GND ----+-- 4      5 --+    +---- C2 0.1uF --- GND
                                         |             |
                                         +-------------+
                                                |
                                          TP_BACKPORCH
```

### Core values from TI typical connection

| Ref | Value | Function |
|---|---:|---|
| C1 | 0.1 uF | AC coupling into pin 2 |
| R1 | 680 kOhm | RSET, pin 6 to GND |
| C2 | 0.1 uF | pin-6 decoupling / set-current node |
| VCC | 5 V for first test | LM1881 supply |

### Project bench additions

| Ref | Value | Function |
|---|---:|---|
| RTERM | 75 Ohm, switchable | terminate a normal 75-Ohm CVBS source |
| C3 | 0.1 uF ceramic | local VCC bypass, pin 8 to pin 4 |
| TP_* | test points | oscilloscope access |

The 75-Ohm termination is **not part of the LM1881 Typical Connection Diagram**. It belongs to the source interface and should be enabled only when the source expects a 75-Ohm load.

The local 0.1-uF VCC bypass is a project implementation choice consistent with the datasheet requirement for supply decoupling. Keep it physically close to pins 8 and 4.

## 4. Exact pin map

```text
       LM1881
      +-------+
CSOUT |1     8| VCC
 CVIN |2     7| ODD/EVEN
VSOUT |3     6| RSET
  GND |4     5| BURST/BACK PORCH
      +-------+
```

For the first Seiko-related test:

- pin 1 is the primary output under test;
- pin 5 is also important because it can later provide the timing window for black-level/DC restoration;
- pins 3 and 7 are diagnostic only initially.

## 5. Optional TI input filter

The TI datasheet describes an optional filter for low-impedance/noisy video sources:

```text
CVBS source -- 620 Ohm series --+-- C1 0.1 uF --> LM1881 pin 2
                                |
                              510 pF
                                |
                               GND
```

TI describes this as approximately a 500-kHz low-pass arrangement for a low-impedance source. It strongly attenuates chroma/noise while retaining sync.

### Project implementation

Do **not** install this filter permanently in the first build.

Provide it as a jumper-selectable path:

```text
SYNC FILTER:
[ BYPASS ]  [ 620R + 510pF ]
```

Reason:

- a clean Raspberry Pi / RP2C02 CVBS source should first be tested without extra delay;
- the filter can then be enabled if chroma/noise causes false sync transitions.

The datasheet notes that this filtering can add roughly tens to hundreds of nanoseconds of delay, so it should not be inserted without need.

## 6. Test setup

### Equipment

- regulated 5-V bench supply with current limit;
- oscilloscope, preferably two channels or more;
- known NTSC composite source;
- 75-Ohm termination enabled if required by the source;
- no Seiko wrist unit connected.

### Suggested supply limit

Start with a conservative bench current limit of approximately **20 mA**.

The datasheet specifies LM1881 supply current below 10 mA under its stated conditions, so 20 mA leaves margin for the IC plus small breadboard loads while still making wiring errors obvious.

This 20-mA value is a project bench limit, not a TI specification.

## 7. First power-up sequence

1. Leave CVBS disconnected.
2. Verify resistance from +5 V to GND is not a short.
3. Set bench supply to 5.0 V and current limit ~20 mA.
4. Power the LM1881.
5. Verify no abnormal current draw or heating.
6. Verify pin 8 is 5 V relative to pin 4.
7. Connect the CVBS source.
8. Observe TP_CVBS_IN.
9. Confirm source amplitude is within the LM1881 input range.
10. Observe pin 1 / TP_CSYNC.

## 8. Expected observations

With valid NTSC-like negative-going sync composite video:

### Pin 2 — CVIN

The IC internally clamps the incoming waveform. Do not expect pin 2 DC level to look identical to the external CVBS connector.

### Pin 1 — CSOUT

Expected:
- composite sync only;
- active sync timing preserved;
- active-video picture information removed.

At 5-V VCC, treat this as a logic output from the LM1881, **not yet as a validated Seiko pin-5 signal**.

### Pin 3 — VSOUT

Expected:
- vertical sync timing pulse.

### Pin 5 — BPOUT

Expected:
- burst/back-porch timing pulse of roughly a few microseconds;
- useful later as the clamp key for restoring video black level.

### Pin 7 — OEOUT

Expected:
- odd/even field indication for interlaced input.

## 9. Oscilloscope capture set

Record at minimum:

### Capture L1
- CH1: CVBS input
- CH2: CSOUT pin 1
- timebase: several horizontal lines

Purpose:
- horizontal sync extraction;
- polarity;
- propagation delay.

### Capture L2
- CH1: CVBS input
- CH2: CSOUT pin 1
- timebase: one vertical field

Purpose:
- vertical interval behavior.

### Capture L3
- CH1: CVBS input
- CH2: BPOUT pin 5

Purpose:
- confirm back-porch timing for later DC-restoration work.

### Capture L4
Repeat L1 with optional 620-Ohm / 510-pF filter enabled.

Purpose:
- determine whether filtering materially improves sync quality;
- measure added delay.

## 10. PASS criteria for LM1881 bench block

PASS if:

- LM1881 powers normally at 5 V;
- current remains normal;
- CVBS input is not visibly distorted by the branch;
- pin 1 produces stable composite sync for black, white, gray, bars and moving video;
- vertical interval remains stable;
- no false pulses appear from ordinary chroma/picture content;
- back-porch output is present and repeatable.

The block can pass even though its pin-1 amplitude is not yet suitable for the Seiko.

## 11. FAIL / STOP criteria

STOP immediately if:

- supply current reaches the bench limit unexpectedly;
- IC heats noticeably;
- 5-V rail collapses;
- input video is severely loaded/distorted;
- pin 2 sees a waveform outside the device's permitted input conditions;
- breadboard wiring is uncertain.

Do not connect pin 1 to the Seiko during this test.

## 12. Critical warning for the Seiko project

**LM1881 pin 1 is only a recovered logic sync reference. It is not automatically a drop-in replacement for Seiko pin 5.**

Before those nodes are connected, the original TR02-01 pin 5 must still be characterized for:

- high voltage;
- low voltage;
- polarity;
- source impedance;
- load current;
- horizontal pulse width;
- vertical interval;
- startup/no-signal behavior.

A separate level/output-conditioning stage will be designed only after those measurements are known.

## 13. Parts for first breadboard

- 1 × LM1881, 8-pin package suitable for prototype;
- 1 × 680 kOhm resistor;
- 3 × 0.1 uF capacitors (C1, C2, C3);
- 1 × 75-Ohm termination resistor or switchable 75-Ohm terminator;
- optional 1 × 620-Ohm resistor;
- optional 1 × 510-pF capacitor;
- test-point/header pins;
- RCA/BNC input connector;
- 5-V current-limited supply.

## 14. Scope of this circuit

This circuit validates only:

```text
standard CVBS -> reliable recovered timing
```

It deliberately does **not** yet solve:

- Seiko pin-5 output level adaptation;
- pin-6 video bias/amplitude;
- chroma/luma filtering for the wrist video;
- the 4.1/8.9/13.2-V Seiko supply rails.

Those remain separate blocks so each can be validated independently.
