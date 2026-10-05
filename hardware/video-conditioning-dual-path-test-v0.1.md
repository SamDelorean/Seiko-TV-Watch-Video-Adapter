# Dual-Path Video Conditioning Bench — V0.1

Status: **concrete bench design for comparing UNITY+BIAS vs GAIN+BIAS; Seiko still disconnected**

This document is **Phase 1** of the broader pin-6 waveform characterization. The complete polarity/centering matrix is defined in [`pin6-waveform-hypotheses-v0.1.md`](pin6-waveform-hypotheses-v0.1.md).

## 1. Question being tested

The two leading linear hypotheses for Seiko pin 6 are:

### Path A — unity amplitude plus DC intercept

```text
VOUT = VBIAS + 1 × VVIDEO
```

### Path B — amplified amplitude plus DC intercept

```text
VOUT = VBIAS + G × VVIDEO
```

with `G != 1`.

The difference to test is therefore **slope**, not the existence of a DC intercept: both candidates can have a non-zero intercept.

The bench shall switch between the two paths while keeping the same DC-restoration, bias reference, output buffer and protection.

## 2. Required common input node

This experiment begins at a common normalized video node called `VIDEO_NORM`.

Required behavior:

- synchronization removed/blanked;
- black/blanking = 0 V reference;
- active picture is a positive-going luma excursion;
- nominal white excursion expected near 0.7 V for a conventional CVBS-derived luma path, but actual value must be measured.

Conceptual front end:

```text
CVBS
 |
75-ohm termination
 |
buffer
 |
optional luma filter
 |
DC restoration / black clamp
 |
sync blanking
 |
VIDEO_NORM
```

The LM1881 provides CSYNC and back-porch timing for this front end.

Do not test the Seiko-level hypotheses using raw CVBS including the negative sync tip, because that mixes two different questions.

## 3. Candidate active parts for bench work

These are **bench candidates, not frozen production parts**.

### Wideband video amplifier/buffer: OPA810-class

Useful properties of TI OPA810:

- single-supply range up to 27 V;
- rail-to-rail input/output;
- unity-gain stable;
- approximately 140-MHz small-signal bandwidth;
- approximately 200 V/us slew rate.

For this bench, use a nominal **+15 V analog supply**.

This gives ample headroom for a provisional output around 8–10 V while preserving video bandwidth.

### Bias-reference buffer: OPA197-class

Useful properties:

- up to 36-V supply;
- rail-to-rail input/output;
- 10-MHz GBW;
- low offset;
- good capacitive-load capability.

Its job is DC reference generation, not the main video path.

### High-voltage clamp switch: TMUX621x-class

Useful properties:

- single-supply operation up to 36 V;
- analog signal range to the supply rails;
- approximately 2-ohm on resistance;
- logic control compatible down to 1.8 V.

Select the exact TMUX6211/6212/6213 logic variant, or add a logic inverter, so the switch is **closed only during the LM1881 back-porch clamp interval**.

## 4. Shared bias/clamp/output section

This section is identical for both hypotheses.

```text
                              +15 V
                                |
                           RV1 10k multiturn
                                |
                         adjustable VBIAS
                                |
                         UREF precision buffer
                                |
                              47R
                                |
                         S1 clamp switch
                                |
                                +---------+
                                          |
selected video ---- CSHIFT 10 nF --------+---- CLAMP_NODE
                                          |
                                    UOUT wideband
                                    unity buffer
                                          |
                                      RPROT
                                          |
                                       TP_OUT
                                          |
                                  dummy load only
```

Control:

```text
LM1881 BPOUT ---> S1 control
```

During back porch, S1 briefly forces `CLAMP_NODE` to `VBIAS`.

During active picture, S1 opens and the AC-coupled picture waveform rides on that stored DC level.

### Initial values

| Ref | Initial bench value | Status |
|---|---:|---|
| Analog supply | +15 V | bench proposal |
| RV1 | 10 kOhm multiturn | wide temporary bias range |
| CSHIFT | 10 nF film/C0G where practical | bench starting value |
| RCLAMP | 47 Ohm | limits clamp-current spike |
| RPROT | 1 kOhm initially | protection-only starting value; reduce only after impedance measurement |
| UREF | OPA197-class | candidate |
| UOUT | OPA810-class | candidate |
| S1 | TMUX621x-class | candidate |

### Why keyed bias instead of a passive resistor sum

A passive resistor summing node would make the output offset depend on source impedance and could let picture-average level alter black level.

The keyed clamp directly defines the back-porch/black reference each line.

# PATH A — UNITY + BIAS

## 5. Circuit

```text
VIDEO_NORM
    |
  JP_MODE = A
    |
   direct
    |
 CSHIFT
    |
keyed VBIAS clamp
    |
 UOUT x1
    |
 RPROT
    |
 TP_OUT_A
```

Transfer after settling:

```text
VOUT_A approximately VBIAS + VVIDEO
```

For the first bench test, no intentional video gain is inserted.

## 6. Nominal example only

Assume:

```text
VIDEO_NORM:
black = 0.00 V
white = +0.70 V

VBIAS = 8.00 V
```

Expected:

```text
black -> 8.00 V
white -> 8.70 V
excursion -> 0.70 V
```

This is the direct test of the "video simply added to a DC operating point" hypothesis.

## 7. Warning for Path A

Do not interpret a good-looking waveform as proof of compatibility.

Path A is accepted only if the original TR02-01 shows approximately the same AC video excursion.

If the real pin 6 is ~1.5 V p-p and the normalized source is only ~0.7 V, Path A is falsified even if its DC level is correct.

# PATH B — GAIN + BIAS

## 8. Circuit

Insert a non-inverting wideband gain stage before the same keyed-bias section.

```text
VIDEO_NORM
    |
 UGAIN non-inverting
    |
  G = 1 + RF/RG
    |
 CSHIFT
    |
same keyed VBIAS clamp
    |
same UOUT x1
    |
same RPROT
    |
 TP_OUT_B
```

Because the clamp occurs **after** the gain stage, changing gain changes picture excursion but does not intentionally move the black/DC operating point.

This orthogonalizes the two adjustments.

## 9. Initial fixed gain for the published working hypothesis

The provisional reports suggest roughly:

```text
input active luma excursion ~0.70 V
Seiko video excursion       ~1.50 V
```

which would require approximately:

```text
G = 1.50 / 0.70 = 2.14
```

For an initial non-inverting test stage:

```text
RG = 1.00 kOhm
RF = 1.15 kOhm
G  = 1 + 1.15/1.00
   = 2.15
```

This is intentionally a **test value**, not a claim about the original receiver.

## 10. Nominal example

With:

```text
VIDEO_NORM black = 0.00 V
VIDEO_NORM white = +0.70 V
G = 2.15
VBIAS = 8.00 V
```

expected:

```text
black -> 8.00 V
white -> about 9.505 V
excursion -> about 1.505 V
```

This directly tests the published ~8-V / ~1.5-V interpretation.

## 11. Gain alternatives for the bench

Prefer fixed resistors/jumpers rather than a large high-frequency potentiometer.

With `RG = 1.00 kOhm`:

| RF | Gain |
|---:|---:|
| 0 Ohm / bypass | 1.00 |
| 499 Ohm | 1.499 |
| 1.00 kOhm | 2.00 |
| 1.15 kOhm | 2.15 |
| 2.00 kOhm | 3.00 |

A later fine trim can be added only if measurements require it.

Fixed selectable gains make oscilloscope comparisons reproducible.

## 12. Warning for Path B

Start with the gain stage bypassed.

Never connect the watch and then sweep gain.

An apparently correct 8-V average can coexist with unsafe picture peaks.

Before any wrist connection:

- confirm black voltage;
- confirm white voltage;
- confirm absolute minimum;
- confirm absolute maximum;
- confirm no clipping;
- confirm startup and loss-of-video behavior.

## 13. One-board A/B implementation

The preferred prototype is not two unrelated circuits.

Use one common board with:

```text
                    +---- BYPASS --------+
VIDEO_NORM ---------+                    +--> CSHIFT --> clamp --> buffer --> TP_OUT
                    +--> UGAIN (2.15x) ---+
```

Selector:

```text
MODE A = UNITY + BIAS
MODE B = 2.15x + BIAS
```

This makes the experiment controlled because only one variable changes: video slope.

Everything downstream remains identical.

## 14. Separate polarity question

Do not combine the first A/B experiment with polarity investigation.

First test positive-going picture in both modes.

If original pin-6 white is below black, add a separate **POLARITY** experiment using an inverting wideband stage.

Reason:

```text
A/B question       = amplitude gain?
polarity question  = sign?
bias question      = intercept?
```

Testing all three at once creates too many degrees of freedom.

## 15. Bench test without watch

### Instruments

- +15-V current-limited analog supply;
- +5-V LM1881 supply;
- oscilloscope;
- CVBS source;
- LM1881 bench block;
- dummy/high-impedance load;
- no wrist unit.

### Pattern sequence

Use:

- A00 BLACK;
- A01 WHITE;
- A02 50% GRAY;
- A03 GRAY STEPS;
- A04/A05 ramps.

### Test A1 — unity path

Set:

```text
MODE = A
VBIAS = provisional safe bench value
```

Measure:

- black;
- white;
- p-p excursion;
- clamp stability;
- line-to-line black drift.

### Test B1 — amplified path

Without changing VBIAS or output section:

```text
MODE = B
G = 2.15
```

Repeat the same measurements.

### Critical comparison

The useful result is not whether either looks "good."

Record:

```text
INPUT delta-V
OUTPUT_A delta-V
OUTPUT_B delta-V
OUTPUT black level
clamp droop
overshoot/ringing
```

Then compare those values against the TR02-01 reference when available.

## 16. PASS/FAIL for this bench increment

### PASS

The bench passes if:

- A and B can be selected reproducibly;
- black/DC level remains essentially unchanged between A and B;
- Path A preserves video excursion approximately 1:1;
- Path B produces the calculated gain without clipping;
- A02 and gray ramps remain monotonic;
- keyed clamp holds the black reference stable;
- output remains well behaved into the dummy measurement load.

### FAIL

Fail if:

- changing gain shifts black level materially;
- clamp produces excessive line-rate steps;
- amplifier rings/oscillates;
- output clips near expected 8–10 V region;
- mode switching creates uncontrolled transients;
- black level follows average picture content.

### BLOCKED

Blocked if the normalized, sync-free `VIDEO_NORM` node is not yet available or not stable enough to distinguish conditioning-stage behavior.

### STOP

Stop before wrist connection until original TR02-01 pin-6 limits and impedance are measured.

## 17. Breadboard/layout warning

OPA810-class devices are high-speed amplifiers.

Do not assume a long solderless breadboard is electrically equivalent to a proper prototype PCB/perfboard.

For first analog verification:

- very short feedback loops;
- local supply decoupling;
- ground plane or compact copper ground;
- no long flying leads on amplifier inputs;
- output isolation resistor where needed;
- oscilloscope probe ground spring preferred.

If a solderless breadboard oscillates, that is not evidence that the topology is wrong.

## 18. Candidate part status

The current parts are selected because their published electrical ranges fit the experiment, not because they are frozen BOM items.

Before PCB freeze verify:

- package availability;
- output swing at the actual load;
- stability with the clamp capacitance;
- input/output protection;
- control-polarity truth table of the selected TMUX621x;
- measured bandwidth needed after final luma filtering.

The final circuit may use slower/simpler parts if the measured Seiko bandwidth allows it.
