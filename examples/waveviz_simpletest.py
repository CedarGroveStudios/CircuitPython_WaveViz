# SPDX-FileCopyrightText: Copyright (c) 2024 JG for Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

import board
import displayio
from cedargrove_wavebuilder import WaveBuilder, WaveShape
from cedargrove_waveviz import WaveViz
import adafruit_ili9341

# Define size and offset for display plot window
PLOT_SIZE = (300, 240)  # The plot window (width, height) in pixels
PLOT_OFFSET = (0, 0)  # Left x-axis origin point (x, y)

# Define synth parameters
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
    (WaveShape.Sine, 6.00, 0.00),
    (WaveShape.Sine, 7.00, 0.00),
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

# Display a small version on the bottom layer
splash.append(WaveViz(wave.wave_table, (20, 80), (25, 25), back_color=0x0000A0))

# Display a full-sized version on the top layer
splash.append(
    WaveViz(wave.wave_table, PLOT_OFFSET, PLOT_SIZE, back_color=None, scale=1)
)

while True:
    pass
