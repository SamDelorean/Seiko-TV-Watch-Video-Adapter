# Pattern Generator References

External software is used as design reference and optional tooling, not as an unreviewed dependency.

## FFmpeg

FFmpeg's libavfilter includes deterministic video sources useful for baseline validation and comparison, including `color`, `testsrc`, `testsrc2`, `smptebars`, `smptehdbars`, `rgbtestsrc` and `yuvtestsrc`.

Project role:
- standard-reference patterns;
- quick smoke tests;
- video/tone generation;
- media preprocessing.

The project-owned Seiko diagnostic patterns remain separately defined and reproducible.

## PGenerator+

Repository:
`BigShoots/PGenerator-Plus`

A current Raspberry Pi calibration suite providing full-screen patches, grayscale ramps, windows, bars and network control through a local web interface.

Project role:
- architecture/UI inspiration;
- evidence that Raspberry Pi can serve as a self-contained calibration appliance.

Not adopted as the runtime baseline because it is centered on HDMI SDR/HDR/Dolby Vision workflows rather than vintage NTSC/CVBS monochrome diagnostics.

License observed at review time: GPL-3.0.

## pico-pattern

Repository:
`sharpie7/pico-pattern`

Small test-pattern generator aimed at vintage CRT testing. Its pattern set includes bars, white, grids, dots and crosshairs.

Project role:
- reference for a deliberately small vintage-display test workflow.

It targets Raspberry Pi Pico and TTL/CRT interfaces, not the Zero 2 W CVBS station.

## testcardgen

Repository:
`mayafeur/testcardgen`

Generates common test-card elements such as blank fields, bars, grids, checkerboard, overscan border and circles.

Project role:
- visual/pattern inventory reference.

No source code is to be copied without first resolving licensing.

## smpte-test-media

Repository:
`ldjessee-code/smpte-test-media`

Uses FFmpeg/LAVFI to generate SMPTE bars, tones, motion loops and stress media.

Project role:
- FFmpeg workflow reference for repeatable generated media.

## Project policy

Prefer:
1. project-authored Seiko-specific pattern definitions;
2. standard FFmpeg filters invoked as external tools;
3. external projects as conceptual/reference material.

Do not vendor third-party code merely to obtain a pattern that can be generated trivially and reproducibly within this repository.
