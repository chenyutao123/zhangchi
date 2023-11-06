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
import pandas as pd

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")
st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)

# Read the data file
data = pd.read_csv('hotel_bookings(1).csv')

# Data preprocessing
# Drop missing values
data = data.dropna()

# Question 1: Calculate the average length of stay for each hotel
average_stay = data.groupby('hotel')['stays_in_week_nights'].mean()
print("Question 1: Average length of stay for each hotel")
st.show(average_stay)
print()

# Question 2: Calculate the cancellation rate for each month
# Convert arrival_date to datetime format
data['arrival_date'] = pd.to_datetime(data['arrival_date_year'].astype(str) + '-' + data['arrival_date_month'] + '-' + data['arrival_date_day_of_month'].astype(str))
# Extract year and month from arrival_date
data['year_month'] = data['arrival_date'].dt.to_period('M')
# Calculate cancellation rate by grouping data by year_month and taking the mean of is_canceled
cancellation_rate = data.groupby('year_month')['is_canceled'].mean()
print("Question 2: Cancellation rate for each month")
print(cancellation_rate)
print()

# %%
import numpy as np
import pandas as pd

# Read the data file
data = pd.read_csv('hotel_bookings(1).csv')

# Data preprocessing
# Drop missing values
data = data.dropna()

# Question 1: Calculate the number of bookings for each market segment and distribution channel
bookings_by_segment_channel = data.groupby(['market_segment', 'distribution_channel'])['hotel'].count()
print("Question 1: Number of bookings for each market segment and distribution channel")
print(bookings_by_segment_channel)
print()

# Question 2: Calculate the average cancellation rate for each market segment and distribution channel
cancellation_rate_by_segment_channel = data.groupby(['market_segment', 'distribution_channel'])['is_canceled'].mean()
print("Question 2: Average cancellation rate for each market segment and distribution channel")
print(cancellation_rate_by_segment_channel)
print()

# %%
import pandas as pd
import matplotlib.pyplot as plt

# Read the data file
hotel_booking_frame = pd.read_csv('hotel_bookings(1).csv')

# Group by hotel and assigned room type, calculate the mean of adr
assigned_price_frame = hotel_booking_frame.groupby(["hotel", "assigned_room_type"])["adr"].mean().reset_index()

# Pivot process
pivot_df = assigned_price_frame.pivot_table(index='hotel', columns='assigned_room_type', values='adr')

# Display the pivot table
pivot_df  # This will display the pivot table with average adr for each hotel and assigned room type

# %%
import pandas as pd
import matplotlib.pyplot as plt

# Set the plot style
plt.style.use("ggplot")

# Obtain the dataset
hotel_booking_frame = pd.read_csv('hotel_bookings(1).csv')

# Convert the date string to datetime
hotel_booking_frame['reservation_status_date'] = pd.to_datetime(hotel_booking_frame['reservation_status_date'])

# Separate the data of different hotels
resort_hotel = hotel_booking_frame[hotel_booking_frame['hotel'] == 'Resort Hotel']
city_hotel = hotel_booking_frame[hotel_booking_frame['hotel'] == 'City Hotel']

# Group by reservation status date and calculate the mean of adr
resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()

# Print the mean adr of resort hotel over time
print("Resort Hotel:")
print(resort_hotel)

# Print the mean adr of city hotel over time
print("City Hotel:")
print(city_hotel)

# %%
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("ggplot")

# Obtain the dataset
hotel_booking_frame = pd.read_csv('hotel_bookings(1).csv')

# Convert the date string to datetime
hotel_booking_frame['reservation_status_date'] = pd.to_datetime(hotel_booking_frame['reservation_status_date'])

# Separate the data of different hotels
resort_hotel = hotel_booking_frame[hotel_booking_frame['hotel'] == 'Resort Hotel']
city_hotel = hotel_booking_frame[hotel_booking_frame['hotel'] == 'City Hotel']

# Assign month column
resort_hotel = resort_hotel.assign(month=resort_hotel["reservation_status_date"].dt.strftime("%m"))
city_hotel = city_hotel.assign(month=city_hotel["reservation_status_date"].dt.strftime("%m"))

# Group by month and calculate the sum of adr
total_adr_resort = resort_hotel.groupby(["month"])["adr"].sum()
total_adr_city = city_hotel.groupby(["month"])["adr"].sum()

# Print the total adr of resort hotel for each month
print("Resort Hotel:")
print(total_adr_resort)

# Print the total adr of city hotel for each month
print("City Hotel:")
print(total_adr_city)

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
