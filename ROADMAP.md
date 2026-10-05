# Roadmap

## v0.1 — Interface reconstruction

Goal: establish a defensible electrical model of the original receiver-to-watch connection.

Exit criteria:
- pinout documented;
- known evidence separated from inference;
- original receiver measurement plan defined;
- no unresolved ambiguity about which conductors are power, ground, sync and video.

## v0.2 — Universal CVBS / AV bench

Goal: build a source-independent bench station that accepts standard composite video and reproduces the Seiko-facing power, video and synchronization interface.

Deliverables:
- switchable 75-ohm / high-impedance CVBS input;
- input buffer/splitter;
- LM1881-class composite-sync extraction;
- protected/conditioned Seiko sync output;
- adjustable Seiko video bias/gain stage;
- regulated 4.1 V, 8.9 V and 13.2 V rails;
- current limiting and output protection;
- independent audio passthrough/headphone path;
- oscilloscope test points on all critical nodes;
- comparison against the original receiver.

PASS criterion:
bench outputs remain inside the measured safe envelope of the original receiver and stable sync is recovered from a standard NTSC source.

## v0.3 — Raspberry Pi Zero 2 W source

Goal: use Raspberry Pi Zero 2 W as the first compact modern source connected to the universal CVBS bench.

Initial target:
- hardware composite output from the Zero 2 W TV pad;
- current Raspberry Pi OS KMS composite configuration;
- normal NTSC as first baseline;
- static black/white/gray patterns;
- bars/checkerboard;
- moving pattern;
- MP4 only after timing and electrical stability are demonstrated.

PASS criterion:
the Pi produces stable CVBS and the universal station converts it into repeatable Seiko-compatible sync/video test outputs without a separate GPIO sync generator.

## v0.4 — First watch display

Goal: first protected connection to an original Seiko TV Watch.

Sequence:
1. power only;
2. sync only where electrically safe;
3. black video;
4. gray ramp;
5. static image;
6. moving test pattern.

Every step must be reversible and current-limited.

## v0.5 — MP4 playback / exhibition mode

Goal: reliable playback of local media on the original display through the universal station.

Work items:
- aspect-ratio handling;
- crop/letterbox policy;
- grayscale/luminance optimization for the LVD;
- contrast/gamma shaping;
- playback controls;
- automatic loop mode;
- clean startup/shutdown;
- optional independent audio playback.

## v1.0 — Reproducible display and test station

Goal: documented hardware/software package that another technically competent builder can reproduce as a reversible Seiko TV Watch display, diagnostic and integration station without modifying the watch or treating the original receiver as disposable.

Deliverables:
- final schematic;
- PCB or reproducible perfboard wiring;
- BOM;
- enclosure/cable interface;
- Raspberry Pi image/configuration;
- setup instructions;
- validation procedure;
- demonstration video;
- diagnostic/test usage notes;
- clearly documented reversible connection methods for collectors and repair work.
