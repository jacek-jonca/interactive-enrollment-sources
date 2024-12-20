# -*- coding: utf-8 -*-
# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example of showing geographic enrollment data."""

import os
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Enrollment Sources", page_icon=":taxi:")

# LOAD DATA ONCE
@st.cache_resource
def load_data():
    path = "data.csv"
    if not os.path.isfile(path):
        path = f"https://github.com/jacek-jonca/interactive-enrollment-sources/raw/main/{path}"

    data = pd.read_csv(
        path,
#        nrows=100000,  # there shouldn't be more than 100k records
        names=[
            "lat",
            "lon",
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        usecols=[0, 1],  # only two columns so tobe safe loading two
#        parse_dates=[
#            "date/time"
#        ],  # set as datetime instead of converting after the fact
    )
    return data

# FUNCTION FOR MAPS
def map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["lon", "lat"],
                    radius=100,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )

# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.cache_data
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

# FILTER DATA BY HOUR
#@st.cache_data
#def histdata(df):
#    filtered = data[
#        (df["date/time"].dt.hour >= hr) & (df["date/time"].dt.hour < (hr + 1))
#    ]
#    hist = np.histogram(filtered["date/time"].dt.minute, bins=60, range=(0, 60))[0]
#    return pd.DataFrame({"minute": range(60), "pickups": hist})

# STREAMLIT APP LAYOUT
data = load_data()

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2, 3))

with row1_1:
    st.title("Enrollment Sources Data")

with row1_2:
    st.write(
        """
    ##
    Visualizing enrollments
    """
    )

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2 = st.columns((2, 2))

# SETTING GEOGRAPHIC CENTERS
texas = [31.391533, -99.17065]
houston = [29.7601, -95.3701]
dallas = [32.7079, -96.9209]
austin = [30.274722, -97.740556]
sanAntonio = [29.424349, -98.491142]
zoom_level = 9
midpoint = mpoint(data["lat"], data["lon"])

with row2_1:
    st.write(
        f"""**All Texas**"""
    )
    map(data, midpoint[0], midpoint[1], 11)

with row2_2:
    st.write("**Houston**")
    map(data, houston[0], houston[1], zoom_level)
