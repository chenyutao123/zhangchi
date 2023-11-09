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

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Analyze the hotel_booking dataset 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(  
        """

        This project is made by Team 6, whose name is The six. Our group contains coincidently 6 people ———— 
        Xingchen Xu, Zhixuan Ye, Chi Zhang, Ruopu Wang, Wanyin Yang, Yutao Chen! 
        
        ### Readme to describe the dataset 
        - Analyze the hotel_booking dataset 
        In this page, we examine several aspects of hotel booking and analyze the data to gain a deeper understanding

        - Some factors about hotel booking

        (1)Factor 1:
        Average length of stay for each hotel


        (2) Factor 2:
        Cancellation rate for each month

        (3) Factor 3:
        Number of booking for each market segment and distribution  channel

        (4)Factor 4:
        Average cancellation rate for each market segment and distribution channel

        - source
        We use the source about Average Daily Rate ,Occupancy Rate, Cancellation Rate and so on to gain a deeper understanding of the reasons for changes in hotel bookings.

        ### Simple analyze using numpy and pandas about the dataset :books:
        ### Use chart or plot to visualize the dataset and do the interaction
        -  ADR in City and Resort Hotel
        - Average Price of each room type
        - proportion of orders per month
        - Top 8 Correlation with adr
    """
    )


if __name__ == "__main__":
    run()
