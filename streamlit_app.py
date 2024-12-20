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
st.set_page_config(layout="wide", page_title="Enrollment Sources", page_icon=":student:")

# LOAD DATA ONCE
@st.cache_resource
def load_data():
    path = "data.csv"
    if not os.path.isfile(path):
        path = f"https://github.com/jacek-jonca/interactive-enrollment-sources/raw/main/{path}"

    data = pd.read_csv(
        path,
        names=[
            "lon",
            "lat",
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        usecols=[0, 1],  # only two columns so tobe safe loading two
    )
    return data

# FUNCTION FOR MAPS
def map(data, lon, lat, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "longitude": lon,
                "latitude": lat,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    'HexagonLayer',
                    data=data,
                    get_position=['lon', 'lat'],
                    radius=100,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    auto_highlight=True,
                    pickable=True,
                    extruded=True,
                    coverage=1,
                ),
            ],
        )
    )

# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.cache_data
def mpoint(lon, lat):
    return (np.average(lon), np.average(lat))

# STREAMLIT APP LAYOUT
data = load_data()

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((3, 2))

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
texas = [-99.17065, 31.391533]
houston = [-95.3701, 29.7601]
dallas = [-96.9209, 32.7079]
austin = [-97.740556, 30.274722]
sanAntonio = [-98.491142, 29.424349]
zoom_level = 9
midpoint = mpoint(data["lon"], data["lat"])

with row2_1:
    st.write(
        f"""**All Texas**"""
    )
    map(data, midpoint[0], midpoint[1], 11)

with row2_2:
    st.write("**Houston**")
    map(data, houston[0], houston[1], zoom_level)
