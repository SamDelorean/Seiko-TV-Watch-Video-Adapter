# Seiko TV Watch Diagnostic Pattern Catalog — V0.1

This catalog defines patterns by **diagnostic purpose**, not merely by appearance.

The NTSC source raster and the physical Seiko LVD pixel matrix are different domains. Until the exact source-to-panel sampling map has been characterized, terms such as "1 pixel" below refer to **source-raster pixels/lines**, not guaranteed one-to-one Seiko cells.

## Group A — Basic luminance and clipping

### A00 BLACK
Full-field black.

Detects:
- black level;
- unwanted glow/background;
- stuck bright cells;
- leakage/noise.

### A01 WHITE
Full-field white.

Detects:
- maximum drive;
- uniformity;
- stuck dark cells;
- rail sag under maximum picture level.

### A02 MIDGRAY
50% nominal luma.

Detects:
- uniformity;
- vertical/horizontal shading;
- analog noise;
- local cell defects that hide at extremes.

### A03 GRAY STEPS 0–100
11 full-height bars at nominal 0,10,...100% luminance.

Use:
- contrast range;
- gray discrimination;
- clipping.

### A04 CONTINUOUS GRAY RAMP H
Black-to-white horizontal continuous ramp.

### A05 CONTINUOUS GRAY RAMP V
Black-to-white vertical continuous ramp.

Use A04/A05 to distinguish direction-dependent nonuniformity.

### A06 NEAR-BLACK / PLUGE
Adjacent low-level patches around black.

Initial project set:
0 / 2 / 4 / 6 / 8 / 10% nominal luma.

Purpose:
- black-level calibration;
- low-level discrimination;
- reveal crushing.

### A07 NEAR-WHITE
90 / 92 / 94 / 96 / 98 / 100% nominal luma.

Purpose:
- highlight clipping;
- maximum-drive compression.

## Group B — Geometry and active-area mapping

### B00 BORDER / OVERSCAN
Bright outer border plus nested inset borders.

Purpose:
- identify visible active area;
- detect cropping;
- document source-to-panel mapping.

### B01 CENTER CROSS
Horizontal and vertical center axes plus center marker.

### B02 CIRCLE + CROSS
Central circle over crosshair.

Purpose:
- gross aspect/geometry evaluation;
- reveal unequal X/Y scaling.

### B03 COARSE GRID
Low-frequency square grid.

### B04 FINE GRID
Higher-frequency grid.

Purpose:
- scan linearity;
- local distortion;
- sampling stability.

### B05 CORNER MARKERS
Distinct shapes in all four corners.

Purpose:
- orientation;
- missing edge area;
- line/field displacement.

## Group C — Effective resolution / spatial response

### C00 VERTICAL LINE PAIRS
Groups of alternating vertical bars with progressively smaller pitch.

Measures:
- horizontal spatial response;
- effective resolvable detail.

### C01 HORIZONTAL LINE PAIRS
Equivalent test in the vertical direction.

### C02 CHECKERBOARD SERIES
Checkerboards at several source pitches:
16, 8, 4, 2 source pixels per cell initially.

### C03 DOT GRID
Regular bright dots over dark field.

Purpose:
- local focus/sampling;
- identify missing regions.

### C04 ZONE / FREQUENCY SWEEP
Optional later radial/linear spatial-frequency sweep.

Purpose:
- aliasing;
- bandwidth;
- sampling artifacts.

Do not use C04 as a pass/fail metric until its mapping is characterized.

## Group D — Defective cell / uniformity search

### D00 DEFECT SEARCH BLACK
Full black held for operator inspection.

### D01 DEFECT SEARCH WHITE
Full white held for operator inspection.

### D02 DEFECT SEARCH GRAY
25%, 50%, 75% fields sequentially.

### D03 SLOW INVERSION
Alternate black and white slowly, default 1 Hz or slower.

Purpose:
- reveal stuck/slow cells;
- persistence;
- differential response.

### D04 SCANNING BLOCK
Small bright block scans systematically over black field, followed by inverse mode.

Purpose:
- local defect localization;
- photograph/video correlation.

Do not claim one block = one physical LVD pixel until mapping is measured.

## Group E — Temporal response / ghosting

### E00 BLACK-WHITE STEP
Whole field changes black ↔ white at a slow controlled cadence.

Record:
- visible rise/fall behavior;
- asymmetry;
- persistence.

### E01 25–75% STEP
Smaller amplitude temporal step.

### E02 MOVING VERTICAL BAR
Bright vertical bar moves horizontally at selectable speed.

### E03 MOVING HORIZONTAL BAR
Bright horizontal bar moves vertically.

### E04 MOVING BOX
Square traverses a fixed path.

Purpose:
- smear;
- trailing;
- direction-dependent response.

### E05 CHECKERBOARD PHASE TOGGLE
Checkerboard alternates phase at slow cadence.

Purpose:
- residual image / retention;
- pixel response symmetry.

## Group F — Synchronization / field behavior

### F00 LOCK FRAME
Fixed border + center cross + frame counter.

Purpose:
- immediately reveal horizontal/vertical drift or roll.

### F01 LUMA EXTREME SYNC STRESS
Alternate black/white picture content while sync remains standard.

Purpose:
- check whether video-conditioning amplitude perturbs sync recovery.

### F02 SINGLE-LINE / LINE POSITION
Movable horizontal line.

Purpose:
- vertical positioning;
- line stability.

### F03 FIELD / INTERLACE PATTERN
Alternating one-line structures designed to expose odd/even field behavior.

Use only after the Pi composite timing mode has been characterized.

## Group G — Chroma rejection / monochrome path

### G00 SMPTE BARS
Standard SMPTE color bars from FFmpeg/reference generator.

Not for color calibration of the Seiko.

Purpose:
- inspect what the Seiko video branch does with chroma;
- compare original TR02-01 VID2 against universal bench output.

### G01 EQUAL-LUMA COLOR TEST
Later custom pattern using different chroma values with matched/near-matched luma.

Purpose:
- identify chroma leakage into apparent grayscale.

### G02 LUMA-ONLY REFERENCE
Grayscale equivalent of G00/G01.

Compare G00/G01 with G02 to determine whether a luma low-pass/chroma trap is required.

## Group H — Exhibition / real-content confidence

### H00 REFERENCE STILL
High-contrast photographic still with faces, text and fine detail.

### H01 LOW-CONTRAST STILL
Tests useful picture reproduction beyond synthetic patterns.

### H02 MOTION REFERENCE
Short uncompressed/lossless or high-quality motion sequence.

### H03 MP4 PLAYBACK
General media demonstration.

This is deliberately the last test in the engineering sequence.

## Automatic diagnostic sequence V0.1

Suggested initial AUTO order:

```text
A00 black             5 s
A01 white             5 s
A02 50% gray          5 s
A03 gray steps        8 s
A06 near-black        8 s
A07 near-white        8 s
B00 borders           8 s
B01 cross             5 s
B02 circle/cross      8 s
B03 coarse grid       8 s
C00 vertical pairs   10 s
C01 horizontal pairs 10 s
C02 checker series   12 s
D02 gray defect scan 15 s
E02 moving V bar     10 s
E03 moving H bar     10 s
E05 checker toggle   10 s
F00 lock/frame       10 s
G00 SMPTE bars       10 s
G02 luma reference   10 s
```

Durations are configurable. The sequence version must be stored in logs so results remain reproducible.

## Optional audio patterns

Because audio is independent of the wrist connector, the station may additionally provide:
- silence;
- 1 kHz reference tone;
- left/right identification;
- stepped tone levels.

These test the station audio path, not the Seiko wrist display itself.
