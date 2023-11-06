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

# Read the data file


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
st.write("# Question 5: Average price of assigned rooms in City Hotel and Resort Hotel")
st.write(pivot_df)  # This will display the pivot table with average adr for each hotel and assigned room type

# %%import pandas
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use("ggplot")

# obtain dataset
hotel_booking_frame = pd.read_csv("hotel_bookings(1).csv")
assigned_price_frame = hotel_booking_frame.groupby(["hotel", "assigned_room_type"])["adr"].mean().reset_index()

# pivot process
pivot_df = assigned_price_frame.pivot_table(index='hotel', columns='assigned_room_type', values='adr')

# draw the bar
ax = pivot_df.plot(kind="bar", yerr=hotel_booking_frame.groupby(['hotel', 'assigned_room_type'])['adr'].std().unstack(), figsize=(30, 8))
ax.set_xlabel('hotel')
ax.set_ylabel('adr')
ax.set_title('Average Price and Standard Deviation of Assigned Rooms')
ax.legend(title='assigned_room_type', title_fontsize='12')
ax.set_xticklabels(hotel_booking_frame['hotel'].unique(), rotation=0)

# The number of prices is displayed at the top of the bar chart
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=8)

# show table
st.table(plt)


import pandas
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

plt.style.use("ggplot")

# obtain dataset
hotel_booking_frame = pandas.read_csv("hotel_bookings(1).csv")
assigned_price_frame = hotel_booking_frame.groupby(["hotel", "assigned_room_type"])["adr"].mean().reset_index()

# pivot process
pivot_df = assigned_price_frame.pivot_table(index='hotel', columns='assigned_room_type', values='adr')

# create a slider
slider = widgets.IntSlider(value=1, min=1, max=len(pivot_df.columns), step=1, description='Number of Room Types', continuous_update=False)

def update_chart(num_of_room_types):
    # filter columns based on the selected number of room types
    selected_columns = pivot_df.columns[:num_of_room_types]
    selected_df = pivot_df[selected_columns]
    
    # draw the bar
    ax = selected_df.plot(kind="bar", yerr=hotel_booking_frame.groupby(['hotel', 'assigned_room_type'])['adr'].std().unstack(), figsize=(30, 8))
    ax.set_xlabel('hotel')
    ax.set_ylabel('adr')
    ax.set_title('Average Price and Standard Deviation of Assigned Rooms')
    ax.legend(title='assigned_room_type', title_fontsize='12')
    ax.set_xticklabels(hotel_booking_frame['hotel'].unique(), rotation=0)

    # The number of prices is displayed at the top of the bar chart
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=8)

    # show table
    plt.show()

# display the slider
display(slider)

# update the chart whenever the slider value changes
widgets.interact(update_chart, num_of_room_types=slider)



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
