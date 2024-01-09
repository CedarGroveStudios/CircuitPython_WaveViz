Introduction
============




.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_WaveViz/workflows/Build%20CI/badge.svg
    :target: https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_WaveViz/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

A CircuitPython class to create a positionable ``displayio.Group`` object
widget from a ``synthio.ReadableBuffer`` wave table. The class also makes
the underlying bitmap object available.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.


Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install cedargrove_waveviz

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python
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


Documentation
=============
API documentation for this library can be found in `Cedargrove_WaveViz <https://github.com/CedarGroveStudios/CircuitPython_WaveViz/blob/main/media/pseudo_rtd_cedargrove_waveviz.pdf>`_.

.. image:: https://github.com/CedarGroveStudios/CircuitPython_WaveViz/blob/main/media/waveviz_api_page1a.png

.. image:: https://github.com/CedarGroveStudios/CircuitPython_WaveViz/blob/main/media/waveviz_api_page2a.png

For additional detail about ``WaveViz``, see `WaveViz: Plot a synthio Waveform <https://adafruit-playground.com/u/CGrover/pages/waveviz-plot-a-synthio-waveform>`_

Planned Updates
---------------
* Use a .wav file as input.
* Design a scrolling window for visualizing long waveform arrays and files.
