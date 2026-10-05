# How the Seiko converts NTSC video to its LCD matrix

## Key conclusion

The Seiko TV Watch does **not** appear to digitize a full NTSC frame into a framebuffer and then average or rescale it digitally.

Primary Suwa Seikosha documentation describes a direct, synchronized analog-sampling architecture.

## Signal flow

The pocket receiver supplies two relevant signals to the wrist unit:

- **VID1** — synchronization information;
- **VID2** — video information.

Inside the wrist unit:

1. VID1 is separated into horizontal and vertical synchronization.
2. A PLL/timing section derives the clocks used by the LVD matrix.
3. VID2 is amplified.
4. The video polarity is switched by field as required by the LCD drive method.
5. The X/Y scanning circuitry selects individual display cells.
6. The instantaneous analog video voltage is written into the selected pixel through its transistor.
7. A storage capacitor associated with the pixel holds that level until the next refresh.

The display therefore behaves much more like an analog sample-and-hold matrix than a digital framebuffer.

## Why this matters

The external adapter does not need to know the physical pixel matrix in order to display ordinary moving video.

If the adapter supplies:
- correctly timed synchronization; and
- correctly scaled/bias-conditioned analog video,

the original Seiko timing and LVD electronics perform the raster-to-panel sampling.

## Resolution

Contemporary documentation describes the LVD as approximately **152 × 210 active pixels** (31,920 cells) with multiple gray levels.

The exact mapping between NTSC active-video timing and those physical cells should be treated as a function of the original Seiko timing circuitry, not reproduced externally unless later measurements show otherwise.

## Open measurement: chroma

An NTSC composite source such as an RP2C02 contains chroma/burst as well as luminance and sync.

The original Seiko display is monochrome. We must therefore measure the original receiver's VID2 output with a color-bar input and determine whether:
- the chroma subcarrier/burst is still present;
- it is attenuated by the receiver;
- VID2 is effectively a luma-only signal.

That result will determine whether the modern adapter needs a dedicated chroma/luma low-pass stage before driving pin 6.
