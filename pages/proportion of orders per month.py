# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib.error import URLError

import altair as alt

import streamlit as st
from streamlit.hello.utils import show_code

import numpy as np
import pandas as pd

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")
st.write("# This demo shows proportion of Rosort/City Hotel orders per month")


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import tempfile

plt.style.use("ggplot")

# obtain dataset
hotel_booking_frame = pd.read_csv("hotel_bookings(1).csv")

# convert date string to datetime
hotel_booking_frame['reservation_status_date'] = pd.to_datetime(hotel_booking_frame['reservation_status_date'])

# separate data of different hotels
resort_hotel = hotel_booking_frame[hotel_booking_frame['hotel'] == 'Resort Hotel']
city_hotel = hotel_booking_frame[hotel_booking_frame['hotel'] == 'City Hotel']

resort_hotel = resort_hotel.assign(month=resort_hotel["reservation_status_date"].dt.strftime("%m"))
city_hotel = city_hotel.assign(month=city_hotel["reservation_status_date"].dt.strftime("%m"))

total_adr_resort = resort_hotel.groupby(["month"])["adr"].sum()
total_adr_city = city_hotel.groupby(["month"])["adr"].sum()

labels = ['Resort Hotel', 'City Hotel']

# Add a sidebar for user input
st.sidebar.header('Select Hotel Type')
hotel_type = st.sidebar.selectbox('Choose a hotel type:', ['Resort Hotel', 'City Hotel'])

# Create a figure with a single subplot
fig, ax = plt.subplots(figsize=(8, 6))

if hotel_type == 'Resort Hotel':
    # Plot the ADR for Resort Hotel
    ax.pie(total_adr_resort, labels=total_adr_resort.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Resort Hotel ADR by Month')
    ax.axis('equal')
else:
    # Plot the ADR for City Hotel
    ax.pie(total_adr_city, labels=total_adr_city.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('City Hotel ADR by Month')
    ax.axis('equal')

# Save the figure as a temporary file
temp_file_name = tempfile.mkstemp(suffix='.png')[1]
fig.savefig(temp_file_name)
plt.close(fig)

# Display the image using Streamlit
st.image(temp_file_name)

st.pyplot()

# %%




def data_frame_demo():
    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )




#data_frame_demo()

show_code(data_frame_demo)
