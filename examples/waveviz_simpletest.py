# SPDX-FileCopyrightText: Copyright (c) 2024 JG for Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

import board
import displayio
import synthio
import adafruit_ili9341
from cedargrove_wavebuilder import WaveBuilder, WaveShape
from cedargrove_waveviz import WaveViz

# Define wave table parameters
WAVE_TABLE_LENGTH = 512  # The wave table length in samples
SAMPLE_MAXIMUM = 32700  # The maximum value of a sample

# Instantiate a built-in display
# display = board.DISPLAY

# Instantiate the FeatherS2 with 2.4-inch TFT FeatherWing display
displayio.release_displays()  # Release display resources
display_bus = displayio.FourWire(
    board.SPI(), command=board.D6, chip_select=board.D5, reset=None
)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)
display.rotation = 0

splash = displayio.Group()
display.root_group = splash

# Define the Harmonica wave shape, overtone ratio, and amplitude
tone = [
    (WaveShape.Sine, 1.00, 0.10),
    (WaveShape.Sine, 2.00, 0.48),
    (WaveShape.Sine, 3.00, 0.28),
    (WaveShape.Sine, 4.00, 0.02),
    (WaveShape.Sine, 5.00, 0.12),
]

# Create the wave table (wave.wave_table)
wave = WaveBuilder(
    oscillators=tone,
    table_length=WAVE_TABLE_LENGTH,
    sample_max=SAMPLE_MAXIMUM,
    lambda_factor=1.0,
    loop_smoothing=True,
    debug=False,
)

# Create a synthio.Envelope object
env = synthio.Envelope(
    attack_time=0.05,
    attack_level=1.0,
    decay_time=0.1,
    release_time=0.1,
    sustain_level=0.5,
)


# Display a small version on the bottom layer
splash.append(
    WaveViz(wave.wave_table, x=20, y=80, width=25, height=25, back_color=0x0000A0)
)

# Display a full-sized version on the middle layer
splash.append(
    WaveViz(wave.wave_table, x=0, y=0, width=300, height=240, back_color=None)
)

# Display the envelope object on the top layer
splash.append(
    WaveViz(
        env,
        x=150,
        y=170,
        width=80,
        height=40,
        plot_color=0xFFFFFF,
        back_color=0x800080,
        envelope_plot=True,
    )
)

while True:
    pass
