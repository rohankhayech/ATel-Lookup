"""
The constants module contains all general constants used throughout the application.

Author:
    Rohan Khayech

Contributors:
    Nathan Sutardi

License Terms and Copyright:
    Copyright (C) 2021 Rohan Khayech and Nathan Sutardi

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
"""


def valid_keyword(keyword: str) -> bool:
    """
    Checks if the given string is a valid fixed ATel keyword. This is case insensitive. 

    Args:
        keyword (str): The keyword to check.

    Returns:
        bool: True if the string is a valid keyword, False otherwise.
    """
    return keyword.lower() in FIXED_KEYWORDS

# List of fixed keywords.
FIXED_KEYWORDS = ["radio",
                   "millimeter",
                   "sub-millimeter",
                   "far-infra-red",
                   "infra-red",
                   "optical",
                   "ultra-violet",
                   "x-ray",
                   "gamma ray",
                   "> gev",
                   "tev",
                   "vhe",
                   "uhe",
                   "neutrinos",
                   "a comment",
                   "agn",
                   "asteroid",
                   "asteroid(binary)",
                   "binary",
                   "black hole",
                   "blazar",
                   "cataclysmic variable",
                   "comet",
                   "cosmic rays",
                   "direct collapse event",
                   "exoplanet",
                   "fast radio burst",
                   "gamma-ray burst",
                   "globular cluster",
                   "gravitational lensing",
                   "gravitational waves",
                   "magnetar",
                   "meteor",
                   "microlensing event",
                   "near-earth object",
                   "neutron star",
                   "nova",
                   "planet",
                   "planet(minor)",
                   "potentially hazardous asteroid",
                   "pre-main-sequence star",
                   "pulsar",
                   "quasar",
                   "request for observations",
                   "soft gamma-ray repeater",
                   "solar system object",
                   "star",
                   "supernova remnant",
                   "supernovae",
                   "the sun",
                   "tidal disruption event",
                   "transient",
                   "variables",
                   "young stellar object" ]

# Optimised for regex
FIXED_KEYWORDS_REGEX = ["radio",
                        "millimeter",
                        "sub-millimeter",
                        "far-infra-red",
                        "infra-red",
                        "optical",
                        "ultra-violet",
                        "x-ray",
                        "gamma ray",
                        "> gev",
                        "tev",
                        "vhe",
                        "uhe",
                        "neutrinos",
                        "a comment",
                        "agn",
                        "asteroid\(binary\)",
                        "asteroid",
                        "binary",
                        "black hole",
                        "blazar",
                        "cataclysmic variable",
                        "comet",
                        "cosmic rays",
                        "direct collapse event",
                        "exoplanet",
                        "fast radio burst",
                        "gamma-ray burst",
                        "globular cluster",
                        "gravitational lensing",
                        "gravitational waves",
                        "magnetar",
                        "meteor",
                        "microlensing event",
                        "near-earth object",
                        "neutron star",
                        "nova",
                        "planet\(minor\)",
                        "planet",
                        "potentially hazardous asteroid",
                        "pre-main-sequence star",
                        "pulsar",
                        "quasar",
                        "request for observations",
                        "soft gamma-ray repeater",
                        "solar system object",
                        "star",
                        "supernova remnant",
                        "supernovae",
                        "the sun",
                        "tidal disruption event",
                        "transient",
                        "variables",
                        "young stellar object" ]