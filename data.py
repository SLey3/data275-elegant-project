"""
This module processes astronomical data from various CSV files, converting and preparing it for further analysis.
Imports:
    - numpy as np: Used for mathematical operations, including trigonometric functions.
    - pandas as pd: Used for data manipulation and analysis.
Exports:
    - harris_ident_pos_df: Processed DataFrame containing positional data from the Harris catalog.
    - harris_metallicity_photometry_df: Processed DataFrame containing metallicity and photometry data from the Harris catalog.
    - harris_velocity_struct_params_df: Processed DataFrame containing velocity and structural parameters from the Harris catalog.
    - gaia_df: Processed DataFrame containing data from the GaiaSource catalog.
Example:
    >>> from data import harris_ident_pos_df
    >>> harris_ident_pos_df.head()
"""
# ---- imports ----
import numpy as np
import pandas as pd


__all__ = [
    "harris_ident_pos_df",
    "harris_metallicity_photometry_df",
    "harris_velocity_struct_params_df",
    "gaia_df"
]

# ---- importing csv data ----
raw_harris_ident_pos_df = pd.read_csv("./data/harris_pt1.csv")
raw_harris_metallicity_photometry_df = pd.read_csv("./data/harris_pt2.csv")
raw_harris_velocity_struct_params_df = pd.read_csv("./data/harris_pt3.csv")
raw_gaia_df = pd.read_csv("./data/GaiaSource.csv")


#print(raw_harris_ident_pos_df.head())
#print(raw_harris_metallicity_photometry_df.head())
#print(raw_harris_velocity_struct_params_df.head())
#print(raw_gaia_df.head())


# ---- Renaming Columns in dfs' as needed ----
raw_harris_ident_pos_df.rename(columns={"RA (2000)": "ra", "DEC": "dec"}, inplace=True) # to match with gaiasource df

# ---- conversion functions ----
def dec2deci(dec: str) -> float:
    deg, arc_m, arc_s = dec.split(" ")

    return int(deg) + (int(arc_m) / 60) + (float(arc_s) / 3600)

def ra2deci(ra: str) -> float:
    h, m, s = ra.split(" ")
    
    return (int(h) + (int(m) / 60) + (float(s) / 3600)) * 15

def deci2cartesian(deci: float) -> tuple[float, int]:
    x = np.cos(np.radians(deci))
    y = np.sin(np.radians(deci))
    z = 0
    return x, y, z

# ---- NOTE: from inspection we note that only the harris_ident_pos_df RA and DEC values need to be converted to decimal ----
raw_harris_ident_pos_df.ra = raw_harris_ident_pos_df.ra.apply(ra2deci)
raw_harris_ident_pos_df.dec = raw_harris_ident_pos_df.dec.apply(dec2deci)


# ---- apply decimal degrees 2 cartesian ----
raw_harris_ident_pos_df.ra = raw_harris_ident_pos_df.ra.apply(deci2cartesian)
raw_harris_ident_pos_df.dec = raw_harris_ident_pos_df.dec.apply(deci2cartesian)
raw_gaia_df.ra = raw_gaia_df.ra.apply(deci2cartesian)
raw_gaia_df.dec = raw_gaia_df.dec.apply(deci2cartesian)

# ---- drop na ----
raw_harris_ident_pos_df.dropna(inplace=True)
raw_harris_metallicity_photometry_df.dropna(inplace=True)
raw_harris_velocity_struct_params_df.dropna(inplace=True)

# ---- create exports ----
harris_ident_pos_df = raw_harris_ident_pos_df.copy(True)
harris_metallicity_photometry_df = raw_harris_metallicity_photometry_df.copy(True)
harris_velocity_struct_params_df = raw_harris_velocity_struct_params_df.copy(True)
gaia_df = raw_gaia_df[["solution_id", "designation", "ra", "dec", "parallax"]]