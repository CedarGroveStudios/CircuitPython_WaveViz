# SPDX-FileCopyrightText: Copyright (c) 2024 JG for Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

"""
`cedargrove_waveviz`
===============================================================================
A CircuitPython class to create a positionable ``displayio.Group`` object
widget from a ``synthio.ReadableBuffer`` wave table. The class also makes
the underlying bitmap object available.
https://github.com/CedarGroveStudios/CircuitPython_WaveViz

* Author(s): JG for Cedar Grove Maker Studios

Implementation Notes
--------------------
**Software and Dependencies:**
* ulab for CircuitPython
* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

from array import array
import displayio
import bitmaptools


class WaveViz(displayio.Group):
    """
    The WaveViz class creates a displayio.Group from a composite
    ``synthio`` waveform table. The group is created from size and color parameters.

    :param synthio.ReadableBuffer wave_table: The synthio waveform object of type 'h'
    (signed 16-bit). No default.
    :param tuple origin: The group's origin coordinate integer tuple value (x, y). The
    origin is the top left corner of the resultant group. No default.
    :param tuple size: The group size integer tuple value (width, height) in pixels.
    No default.
    :param integer plot_color: The waveform trace color. Defaults to 0x00FF00 (green).
    :param integer grid_color: The perimeter grid color. Defaults to 0x808080 (gray).
    :param integer back_color: The grid background color. Defaults to None (transparent).
    :param integer scale: The group scale factor. Defaults to 1.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        wave_table,
        origin,
        size,
        plot_color=0x00FF00,
        grid_color=0x808080,
        back_color=None,
        scale=1,
    ):
        """Instantiate the tile generator class."""
        self._wave_table = wave_table
        self._origin = origin
        self._size = size
        self._scale = scale
        self._y_offset = self._size[1] // 2

        self._palette = displayio.Palette(3)
        self._palette[1] = plot_color
        self._palette[2] = grid_color
        if back_color is None:
            self._palette[0] = 0x000000
            self._palette.make_transparent(0)
        else:
            self._palette[0] = back_color

        # Instantiate the target bitmap
        self._bmp = displayio.Bitmap(self._size[0], self._size[1], len(self._palette))
        self._bmp.fill(0)

        # self becomes a displayio.Group; plot grid and wave table
        super().__init__(scale=self._scale, x=self._origin[0], y=self._origin[1])
        self._plot_grid()  # Plot the grid
        self._plot_wave()  # Plot the wave table
        self._tile_grid = displayio.TileGrid(self._bmp, pixel_shader=self._palette)
        self.append(self._tile_grid)

    @property
    def bitmap(self):
        """The resultant bitmap object."""
        return self._bmp

    @property
    def palette(self):
        """The resultant displayio.Palette object."""
        return self._palette

    def _plot_wave(self):
        """Plot the wave_table as a bitmap. Extract samples from the wave
        table to fill the bitmap object's x-axis. Y-axis scale factor is
        determined from the extracted sample values."""
        samples = len(self._wave_table)  # Samples in wave table

        # Create and fill the polygon arrays
        x_points = array("h", [])
        y_points = array("h", [])
        for x in range(self._size[0]):
            x_points.append(x)
            table_idx = int(x * (samples / self._size[0]))
            y_points.append(self._wave_table[table_idx])
        # Update the final point
        y_points[-1] = self._wave_table[-1]

        # Calculate the y-axis scale factor and adjust y values
        max_sample_value = max(y_points)
        scale_y = self._size[1] / max_sample_value / 2
        for y in range(self._size[0]):
            y_points[y] = self._y_offset + int(y_points[y] * scale_y)

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
            array("h", [0, self._size[0] - 1, self._size[0] - 1, 0]),
            array("h", [0, 0, self._size[1] - 1, self._size[1] - 1]),
            2,
        )

        # Draw x-axis line
        bitmaptools.draw_line(
            self._bmp,
            0,
            self._y_offset,
            self._size[0],
            self._y_offset,
            2,
        )
