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
def dec2deci(dec: str | np.float64) -> float:
    if isinstance(dec, np.float64):
        return round(dec, 4)
    
    dec_s = dec.split(" ")
    is_neg = dec_s[0][0] == '-'
    
    deg, am, _as = float(dec_s[0]), float(dec_s[1]), float(dec_s[2])

    return round(-1 * (deg + am/60 + _as/3600), 4) if is_neg else round(deg + am/60 + _as/3600, 4)

def ra2deci(ra: str | np.float64) -> float:
    if isinstance(ra, np.float64):
        return round(ra, 4)
    
    h, m, s = ra.split(" ")
    
    return round((int(h) + (int(m) / 60) + (float(s) / 3600)) * 15, 4)


def radeg2deci(ra: str) -> float:
    return ra2deci(np.radians(float(ra)))

def decdeg2deci(dec: str) -> float:
    return dec2deci(np.radians(float(dec)))

def radec2cartesian(ra: float, dec: float, parallax: float) -> tuple[float]:
    # x = D * cos(Dec) * cos(RA)
    # y = D * cos(Dec) * sin(RA)
    # z = D * sin(Dec)
    x = parallax * np.cos(dec) * np.cos(ra)
    y = parallax * np.cos(dec) * np.sin(ra)
    z = parallax * np.sin(dec)
    return x, y, z

# ---- NOTE: from inspection we note that only the harris_ident_pos_df RA and DEC values need to be converted to decimal ----
raw_harris_ident_pos_df.ra = raw_harris_ident_pos_df.ra.apply(ra2deci)
raw_harris_ident_pos_df.dec = raw_harris_ident_pos_df.dec.apply(dec2deci)
raw_gaia_df.ra = raw_gaia_df.ra.apply(radeg2deci)
raw_gaia_df.dec = raw_gaia_df.dec.apply(decdeg2deci)


# ---- apply cartesian to gaia ----
raw_gaia_df["cartesian"] = raw_gaia_df.apply(
    lambda row: radec2cartesian(row["ra"], row["dec"], row["parallax"]), axis=1
)

# ---- drop na ----
raw_harris_ident_pos_df.dropna(inplace=True, subset=["ra", "dec"])
raw_harris_metallicity_photometry_df.dropna(inplace=True)
raw_harris_velocity_struct_params_df.dropna(inplace=True)
raw_gaia_df.dropna(inplace=True, subset=["ra", "dec"])

# ---- create exports ----
harris_ident_pos_df = raw_harris_ident_pos_df.copy(True)
harris_metallicity_photometry_df = raw_harris_metallicity_photometry_df.copy(True)
harris_velocity_struct_params_df = raw_harris_velocity_struct_params_df.copy(True)
gaia_df = raw_gaia_df[["solution_id", "designation", "ra", "dec", "parallax", "cartesian"]]