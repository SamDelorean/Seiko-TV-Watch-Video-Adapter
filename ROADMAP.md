# Roadmap

## v0.1 — Interface reconstruction

Goal: establish a defensible electrical model of the original receiver-to-watch connection.

Exit criteria:
- pinout documented;
- known evidence separated from inference;
- original receiver measurement plan defined;
- no unresolved ambiguity about which conductors are power, ground, sync and video.

## v0.2 — Bench electrical emulator

Goal: reproduce the receiver outputs without connecting the watch initially.

Deliverables:
- regulated 4.1 V, 8.9 V and 13.2 V rails;
- synthetic composite-sync output matching captured waveform;
- synthetic analog video waveform matching captured black/white levels;
- current limiting and output protection;
- oscilloscope comparison against original receiver.

PASS criterion:
prototype waveforms stay within the measured safe envelope of the original receiver.

## v0.3 — Raspberry Pi video source

Goal: convert local media into the signal expected by the analog interface.

Initial target:
- Raspberry Pi Zero 2 W;
- deterministic NTSC output;
- still-image and test-pattern playback first;
- MP4/H.264 after timing stability is demonstrated.

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

## v0.5 — MP4 playback

Goal: reliable playback of local MP4 files on the original display.

Work items:
- aspect-ratio handling;
- crop/letterbox policy;
- grayscale/luminance optimization for the LVD;
- playback controls;
- clean startup/shutdown.

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
