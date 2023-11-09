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



# Read the data file
data = pd.read_csv('hotel_bookings(1).csv')

# Data preprocessing
# Drop missing values
data = data.dropna()

# Question 1: Calculate the average length of stay for each hotel
average_stay = data.groupby('hotel')['stays_in_week_nights'].mean()
st.write("# Question 1: Average length of stay for each hotel")
st.write(average_stay)

# Question 2: Calculate the cancellation rate for each month
# Convert arrival_date to datetime format
data['arrival_date'] = pd.to_datetime(data['arrival_date_year'].astype(str) + '-' + data['arrival_date_month'] + '-' + data['arrival_date_day_of_month'].astype(str))
# Extract year and month from arrival_date
data['year_month'] = data['arrival_date'].dt.to_period('M')
# Calculate cancellation rate by grouping data by year_month and taking the mean of is_canceled
cancellation_rate = data.groupby('year_month')['is_canceled'].mean()
st.write("# Question 2: Cancellation rate for each month")
st.write(cancellation_rate)

data = pd.read_csv('hotel_bookings(1).csv')

# Data preprocessing
# Drop missing values
data = data.dropna()

# Question 1: Calculate the number of bookings for each market segment and distribution channel
bookings_by_segment_channel = data.groupby(['market_segment', 'distribution_channel'])['hotel'].count()
st.write("# Question 3: Number of bookings for each market segment and distribution channel")
st.write(bookings_by_segment_channel)

# Question 2: Calculate the average cancellation rate for each market segment and distribution channel
cancellation_rate_by_segment_channel = data.groupby(['market_segment', 'distribution_channel'])['is_canceled'].mean()
st.write("# Question 4: Average cancellation rate for each market segment and distribution channel")
st.write(cancellation_rate_by_segment_channel)

import pandas as pd
import matplotlib.pyplot as plt

# Read the data file
hotel_booking_frame = pd.read_csv('hotel_bookings(1).csv')

# Group by hotel and assigned room type, calculate the mean of adr
assigned_price_frame = hotel_booking_frame.groupby(["hotel", "assigned_room_type"])["adr"].mean().reset_index()

# Pivot process
pivot_df = assigned_price_frame.pivot_table(index='hotel', columns='assigned_room_type', values='adr')

# Display the pivot table
st.write("# Question 5: Average price of assigned rooms in City Hotel and Resort Hotel")
st.write(pivot_df)  # This will display the pivot table with average adr for each hotel and assigned room type

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
st.write("# Question 6: Show the data to form the line chart")
st.write("Resort Hotel:")
st.write(resort_hotel)

# Print the mean adr of city hotel over time
st.write("City Hotel:")
st.write(city_hotel)

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
st.write("# Question 7: Avergae price of each month in Resort Hotel and City Hotel")
st.write("Resort Hotel:")
st.write(total_adr_resort)

# Print the total adr of city hotel for each month
st.write("City Hotel:")
st.write(total_adr_city)

# %%

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
