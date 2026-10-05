# Candidate video-input paths

This project will evaluate three source paths against the same Seiko receiver-emulation interface.

## A. Game Boy / RP2C02 path

Related repository:

- https://github.com/SamDelorean/gameboy-rp2c02-crt-adapter

That project already defines a Game Boy DMG/SGB logical-video path ending in an RP2C02-class NTSC composite output stage.

For the Seiko application, the preferred tap point is the **composite output of the RP2C02 path**, not the raw Game Boy LCD bus.

Proposed signal chain:

```text
Game Boy / SameBoy-compatible source
        |
existing GB -> RP2C02 bridge
        |
RP2C02 composite NTSC
        +----------------------+
        |                      |
        v                      v
 sync separator          video conditioning
        |                      |
 Seiko pin 5              Seiko pin 6
```

Important: the RP2C02 composite output already contains synchronization. The Seiko requires synchronization and video on separate conductors, so the adapter should derive both from the same composite source to preserve phase coherence.

The video branch may require:
- removal/clamping of sync intervals;
- optional chroma suppression / low-pass filtering;
- gain scaling;
- DC level shifting to the Seiko operating point;
- output-current limiting and protection.

Exact requirements remain TO MEASURE on an original receiver.

## B. Raspberry Pi path

A Raspberry Pi composite-video source can use the same front-end philosophy:

```text
Pi composite output
        +----------------------+
        |                      |
        v                      v
 sync separator          video conditioning
        |                      |
 Seiko pin 5              Seiko pin 6
```

The sync should normally be extracted from the same composite signal rather than generated independently on a GPIO. This avoids phase drift and reduces timing variables.

## C. Bench pattern-generator path

Before either Game Boy or Raspberry Pi is connected to the watch, a deterministic bench source should reproduce:

- measured pin-5 synchronization;
- measured pin-6 black level;
- measured pin-6 white level;
- a gray ramp;
- simple bars.

This path is the preferred first electrical validation.

## Power architecture

For initial bench work, use three independently current-limited rails adjusted to the values measured on the original receiver.

Nominal values currently documented:
- ~4.1 V
- ~8.9 V
- ~13.2 V

Do not freeze current limits or startup sequencing until the original receiver/watch pair has been measured under load.

For a later compact adapter, commercial regulator modules may be treated as black-box power blocks provided that:
- all required rails share the correct reference;
- ripple/noise is acceptable for the analog video path;
- startup and shutdown stay inside the measured safe envelope;
- current limiting/protection is retained.

## Safety rule for video injection

Do **not** interpret the reported ~8 V DC video bias and ~1.5 V video excursion as proof of a symmetrical ±0.75 V signal.

The safe first injection is:
1. reproduce the measured DC black/blanking operating point;
2. set AC/video amplitude to zero;
3. add a small excursion in the **measured polarity**;
4. increase only while remaining within the minimum and maximum voltages observed from the original receiver.

This preserves the user's intended conservative approach without assuming an unverified polarity.
