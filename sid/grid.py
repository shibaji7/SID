#!/usr/bin/env python

"""
    grid.py: module create grids and compute parameters
             simulate backgond and SID model.
"""

__author__ = "Chakraborty, S."
__copyright__ = ""
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "shibaji7@vt.edu"
__status__ = "Research"

import numpy as np
import datetime as dt
from loguru import logger
import pvlib
from model.magnet import Magnet
from model.bgc import Background


class GridSpec(object):
    """
    Specification of grid holding
    latitude, longitude, and height details.
    """

    def __init__(self, lat, lon, h):
        """
        Parameter:
        ----------
        lat: Latitude in degree
        lon: Longitude in degree
        h: Height in km
        """
        logger.info(f"Create grid_spec [{lat}, {lon}, {h}]")
        self.lat, self.lon, self.h = lat, lon, h
        return


def generate_grids(lats=[45, 45, 1], lons=[-75, -75, 1], heights=[50, 150, 1]):
    """
    Parameter:
    ----------
    lats: List of start, end, and seperation latitude in degree
    lons: List of start, end, and seperation longitudes in degree
    heights: List of start, end, and seperation heights in degree
    """
    Nx, Ny, Nz = (
        int((lats[1] - lats[0]) / lats[2]) + 1,
        int((lons[1] - lons[0]) / lons[2]) + 1,
        int((heights[1] - heights[0]) / heights[2]) + 1,
    )
    Lats, Lons, Hs = (
        np.zeros((Nx, Ny, Nz)),
        np.zeros((Nx, Ny, Nz)),
        np.zeros((Nx, Ny, Nz)),
    )
    lats, lons, heights = (
        np.linspace(lats[0], lats[1], Nx),
        np.linspace(lons[0], lons[1], Nx),
        np.linspace(heights[0], heights[1], Nz),
    )
    gdspcs = []
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                Lats[i, j, k], Lons[i, j, k], Hs[i, j, k] = (
                    lats[i],
                    lons[j],
                    heights[k],
                )
                gdspcs.append(GridSpec(lats[i], lons[j], heights[k]))
    return (Lats, Lons, Hs, gdspcs)


class Grid(Magnet, Background):
    """
    This class is dedicated to compute parameters
    simulate backgond and SID model.
    """

    def __init__(self, loc, date, seconds, magnet_model="igrf"):
        """
        Parameters:
        -----------
        loc: Location information
        date: Event start date (python.datetime)
        seconds: List of seconds
        magnet_model: Magnetic model
        """
        self.loc = loc
        self.date = date
        self.seconds = seconds
        self.magnet_model = magnet_model
        self.seconds2dates()
        self.computeSZAs()
        ## Call setup and compile functions
        return

    def seconds2dates(self):
        """
        Convert seconds list to date list.
        """
        self.dates = [self.date + dt.timedelta(seconds=s) for s in self.seconds]
        return

    def computeSZAs(self):
        """
        Compute solar zenith angles.
        """
        self.solpos = pvlib.solarposition.get_solarposition(
            self.dates, self.loc.lat, self.loc.lon, self.loc.h
        )
        return

    def setup(self):
        """
        Setup the background ionosphere.
        """
        Magnet.__init__(self, self.loc, self.date, self.magnet_model)
        Background.__init__(self, self.loc, self.date)
        return

    # TODO
    def compile(self):
        """
        Compile the final SID model
        """
        return


def formulate_grids(
    gdspcs,
    dates=[dt.datetime(2015, 3, 11, 16), dt.datetime(2015, 3, 11, 17), 60],
    magnet_model="igrf",
):
    """
    Create a list of sperate grids
    that compute parameters
    simulate backgond and SID model.
    Parameters:
    -----------
    gdspcs: List of grid specs
    dates: List of start, end, and speration (in sec) dates
    """
    grids = []
    Nd = int((dates[1] - dates[0]).total_seconds())
    seconds, date = range(0, Nd + 1, dates[2]), dates[0]
    for loc in gdspcs:
        grid = Grid(loc, date, seconds, magnet_model)
        grids.append(grid)
    return grids


if __name__ == "__main__":
    _, _, _, gdspcs = generate_grids()
    formulate_grids(gdspcs)
