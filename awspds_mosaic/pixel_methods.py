"""ard-tiler.mosaic: create mosaicJSON from a stac query."""

import numpy

from rio_tiler_mosaic.methods import defaults
from rio_tiler_mosaic.methods.base import MosaicMethodBase


class allStack(MosaicMethodBase):
    """Stack the tiles and return the Median pixel value."""

    def __init__(self):
        """Overwrite base and init Median method."""
        super(allStack, self).__init__()
        self.tile = []

    @property
    def data(self):
        """Return data and mask."""
        if self.tile:
            return list(zip(*[(tile.data, ~tile.mask[0] * 255) for tile in self.tile]))
        else:
            return None, None

    def feed(self, tile):
        """Create a stack of tile."""
        self.tile.append(tile)


class LastBandHigh(MosaicMethodBase):
    """Feed the mosaic tile using the last band as decision factor."""

    @property
    def data(self):
        """Return data and mask."""
        if self.tile is not None:
            return self.tile.data[:-1], ~self.tile.mask[0] * 255
        else:
            return None, None

    def feed(self, tile: numpy.ma.array):
        """Add data to tile."""
        if self.tile is None:
            self.tile = tile
            return

        pidex = (
            numpy.bitwise_and(tile.data[-1] > self.tile.data[-1], ~tile.mask)
            | self.tile.mask
        )

        mask = numpy.where(pidex, tile.mask, self.tile.mask)
        self.tile = numpy.ma.where(pidex, tile, self.tile)
        self.tile.mask = mask


class CountValidMethod(MosaicMethodBase):
    """Feed the mosaic tile and return the number of valid observation by pixel."""

    def feed(self, tile):
        """Add data to tile."""
        tile = numpy.ma.array(~tile.mask * 1, mask=tile.mask)
        if self.tile is None:
            self.tile = tile
            return

        mask = numpy.bitwise_or(~tile.mask, ~self.tile.mask)
        self.tile = numpy.ma.array(self.tile.data + tile.data, fill_value=0)
        self.tile.mask = ~mask


pixSel = {
    "first": defaults.FirstMethod,
    "highest": defaults.HighestMethod,
    "lowest": defaults.LowestMethod,
    "mean": defaults.MeanMethod,
    "median": defaults.MedianMethod,
    "stdev": defaults.StdevMethod,
    "all": allStack,
    "count": CountValidMethod,
    "lastband": LastBandHigh,
}
