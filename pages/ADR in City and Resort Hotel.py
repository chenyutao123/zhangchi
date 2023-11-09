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
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code

import numpy as np




import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
hotel_booking_frame = pd.read_csv("hotel_bookings(1).csv")

# Convert date string to datetime
hotel_booking_frame['reservation_status_date'] = pd.to_datetime(hotel_booking_frame['reservation_status_date'])

# Separate data of different hotels
resort_hotel = hotel_booking_frame[hotel_booking_frame['hotel'] == 'Resort Hotel']
city_hotel = hotel_booking_frame[hotel_booking_frame['hotel'] == 'City Hotel']
resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()

# Create interactive view
st.title('ADR in City and Resort Hotel')

slider_value = st.slider("Select maximum ADR value:", 0, 300, 50, 1)

plt.figure(figsize=(16, 6))
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)


ax.plot(resort_hotel.index, resort_hotel['adr'], label='Resort Hotel')
ax.plot(city_hotel.index, city_hotel['adr'], label='City Hotel')
ax.set_xlabel('Date')
ax.set_ylabel('ADR')
ax.set_ylim(0, slider_value)
ax.legend()





# Create the dropdown menu
#hotel_dropdown = widgets.Dropdown(options=['Resort Hotel', 'City Hotel'], value='Resort Hotel', description='Hotel:')

# Call the update_plot() function when the dropdown menu is changed
#widgets.interact(update_plot, hotel=hotel_dropdown)

#update_plot('Resort Hotel')

# %




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
st.pyplot()




#data_frame_demo()

show_code(data_frame_demo)