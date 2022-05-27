#!/usr/bin/env python

"""
    bgc.py: module to compute IRI-16 and nrlmsise-00.
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
import geomagindices as gi
from nrlmsise00 import msise_flat
from iri2016 import IRI


class Background(object):
    """
    Load background ionosphere.
    """

    def __init__(self, loc, date, smoothdays=81):
        """
        Load background values based on grid location.
        Parameters:
        -----------
        loc: Location information
        date: Start date of simulation (python.datetime)
        """
        logger.info(
            f"Setup background ionosphere for [{loc.lat}, {loc.lon}, {loc.h}] on {date}"
        )
        indices = gi.get_indices(date, smoothdays)
        msise = msise_flat(
            date,
            loc.h,
            loc.lat,
            loc.lon,
            indices["f107"],
            indices["f107s"],
            indices["Ap"],
        )
        self.msise = dict(
            zip(
                ["He", "O", "N2", "O2", "Ar", "density", "H", "N", "Oa", "Texo", "T"],
                msise[0, :],
            )
        )
        iri = IRI(date, [loc.h, loc.h, 1], loc.lat, loc.lon)
        cols = [
            "ne",
            "Tn",
            "Ti",
            "Te",
            "nO+",
            "nH+",
            "nHe+",
            "nNO+",
            "nO2+",
            "nCI",
            "nN+",
        ]
        self.iri = dict(
            zip(
                cols,
                [iri.variables[col].data[0] for col in cols],
            )
        )
        return
