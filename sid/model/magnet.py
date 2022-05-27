#!/usr/bin/env python

"""
    magnet.py: module to compute B-Field from magnetic
               field for each grid.
"""

__author__ = "Chakraborty, S."
__copyright__ = ""
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "shibaji7@vt.edu"
__status__ = "Research"

from loguru import logger
import pyIGRF


class Magnet(object):
    """
    Load magnetic field data for each grid.
    """

    def __init__(self, loc, date, magnet_model="igrf", Re=6371.0, B0=3.12e-5):
        """
        Load magnetic field values based on grid location.
        Parameters:
        -----------
        loc: Location information
        date: Start date of simulation (python.datetime)
        magnet_model: Magnetic model
        Re: Earth radius
        B0: Magnetic field at equator-sea level
        """
        logger.info(
            f"Setup magnetic field {magnet_model} for [{loc.lat}, {loc.lon}, {loc.h}] on {date.year}"
        )
        self.B = {}
        if magnet_model == "igrf":
            r = Re + loc.h
            (
                self.B["d"],
                self.B["i"],
                self.B["h"],
                self.B["t"],
                self.B["p"],
                self.B["r"],
                self.B["b"],
            ) = pyIGRF.igrf_value(loc.lat, loc.lon, r, date.year)
        elif magnet_model == "dipole":
            r = Re + loc.h
            self.B["r"] = -2 * B0 * (Re / r) ** 3 * np.cos(np.deg2rad(theta_lat))
            self.B["t"] = -B0 * (Re / r) ** 3 * np.sin(np.deg2rad(theta_lat))
            self.B["b0"] = np.sqrt(self.B["r"] ** 2 + self.B["t"] ** 2)
        return
