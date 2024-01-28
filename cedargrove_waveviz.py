# SPDX-FileCopyrightText: Copyright (c) 2024 JG for Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

"""
`cedargrove_waveviz`
===============================================================================
A CircuitPython class to create a positionable ``displayio.TileGrid`` object
from a ``synthio.ReadableBuffer`` wave table. The class inherits all
properties of a ``TileGrid`` object including bitmap, pixel_shader, width,
height, x, y.

https://github.com/CedarGroveStudios/CircuitPython_WaveViz
https://docs.circuitpython.org/en/latest/shared-bindings/displayio/#displayio.TileGrid

* Author(s): JG for Cedar Grove Maker Studios

Implementation Notes
--------------------
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

from array import array
import displayio
import bitmaptools


# pylint: disable=too-few-public-methods
class WaveViz(displayio.TileGrid):
    """
    The WaveViz class creates a positionable ``displayio.TileGrid`` object
    from a ``synthio.ReadableBuffer`` wave table. The class inherits all
    properties of a ``TileGrid`` object including bitmap, pixel_shader, width,
    height, x, y.

    :param synthio.ReadableBuffer wave_table: The synthio waveform object of type 'h'
    (signed 16-bit). No default.
    :param int x: The tile grid's x-axis coordinate value. No default.
    :param int y: The tile grid's y-axis coordinate value. No default.
    :param int width: The tile grid's width in pixels. No default.
    :param int height: The tile grid's height in pixels. No default.
    :param integer plot_color: The waveform trace color. Defaults to 0x00FF00 (green).
    :param integer grid_color: The perimeter grid color. Defaults to 0x808080 (gray).
    :param integer back_color: The grid background color. Defaults to None (transparent).
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        wave_table,
        x,
        y,
        width,
        height,
        plot_color=0x00FF00,
        grid_color=0x808080,
        back_color=None,
    ):
        """Instantiate the tile generator class."""
        self._wave_table = wave_table
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._y_offset = self._height // 2

        self._palette = displayio.Palette(3)
        self._palette[1] = plot_color
        self._palette[2] = grid_color
        if back_color is None:
            self._palette[0] = 0x000000
            self._palette.make_transparent(0)
        else:
            self._palette[0] = back_color

        # Instantiate the target bitmap
        self._bmp = displayio.Bitmap(self._width, self._height, len(self._palette))
        self._bmp.fill(0)

        # Plot grid and wave table
        self._plot_grid()  # Plot the grid
        self._plot_wave()  # Plot the wave table
        # Bitmap becomes a displayio.TileGrid object
        super().__init__(self._bmp, pixel_shader=self._palette, x=self._x, y=self._y)

    @property
    def max_result(self):
        """The full-scale value of the plotted image."""
        return self._max_sample_value

    @property
    def width(self):
        """The width of the plotted image in pixels."""
        return self._width

    @property
    def height(self):
        """The height of the plotted image in pixels."""
        return self._height

    def _plot_wave(self):
        """Plot the wave_table as a bitmap. Extract samples from the wave
        table to fill the bitmap object's x-axis. Y-axis scale factor is
        determined from the extracted sample values."""
        samples = len(self._wave_table)  # Samples in wave table

        # Create and fill the polygon arrays
        x_points = array("h", [])
        y_points = array("h", [])
        for x in range(self._width):
            x_points.append(x)
            table_idx = int(x * (samples / self._width))
            y_points.append(self._wave_table[table_idx])
        # Update the final point
        y_points[-1] = self._wave_table[-1]

        # Calculate the y-axis scale factor and adjust y values
        self._max_sample_value = max(y_points)
        self._scale_y = self._height / self._max_sample_value / 2
        for y in range(self._width):
            y_points[y] = self._y_offset - int(y_points[y] * self._scale_y)

        # Draw the values as an open polygon
        bitmaptools.draw_polygon(
            self._bmp,
            x_points,
            y_points,
            1,
            False,
        )

    def _plot_grid(self):
        """Plot the grid lines."""
        # Draw the outer box
        bitmaptools.draw_polygon(
            self._bmp,
            array("h", [0, self._width - 1, self._width - 1, 0]),
            array("h", [0, 0, self._height - 1, self._height - 1]),
            2,
        )

        # Draw x-axis line
        bitmaptools.draw_line(
            self._bmp,
            0,
            self._y_offset,
            self._width,
            self._y_offset,
            2,
        )
