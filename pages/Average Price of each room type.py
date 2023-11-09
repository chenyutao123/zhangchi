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

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
st.write("# Average Price of each room type in Resort Hotel/City Hotel")
plt.style.use("ggplot")

# obtain dataset
hotel_booking_frame = pd.read_csv("hotel_bookings(1).csv")

# separate data of different hotels
resort_hotel = hotel_booking_frame[hotel_booking_frame['hotel'] == 'Resort Hotel']
city_hotel = hotel_booking_frame[hotel_booking_frame['hotel'] == 'City Hotel']

resort_hotel = resort_hotel.groupby(["assigned_room_type"])["adr"].mean().reset_index()
city_hotel = city_hotel.groupby(["assigned_room_type"])["adr"].mean().reset_index()


fig, ax = plt.subplots(1, 2, figsize=(18, 6))
ax1 = ax[0]
ax2 = ax[1]

ax1.bar(resort_hotel["assigned_room_type"], resort_hotel["adr"])
ax2.bar(city_hotel["assigned_room_type"], city_hotel["adr"])

ax1.set_title('Average Price and Standard Deviation of Resort Hotel')
ax2.set_title('Average Price and Standard Deviation of City Hotel')

ax1.set_xlabel("room_type")
ax2.set_xlabel("room_type")
ax1.set_ylabel("adr")
ax2.set_ylabel("adr")

# The number of prices is displayed at the top of the bar chart
for p in ax1.patches:
    ax1.annotate(f'{p.get_height():.2f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center',
                va='bottom',
                fontsize=8)

for p in ax2.patches:
    ax2.annotate(f'{p.get_height():.2f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center',
                va='bottom',
                fontsize=8)

# Add a selectbox to the sidebar:
option = st.sidebar.selectbox(
    'Which hotel do you want to see?',
    ('Resort Hotel', 'City Hotel')
)

# Display the selected hotel's data
if option == 'Resort Hotel':
    st.bar_chart(resort_hotel.set_index('assigned_room_type')['adr'])
else:
    st.bar_chart(city_hotel.set_index('assigned_room_type')['adr'])


plt.show()

#st.pyplot()

