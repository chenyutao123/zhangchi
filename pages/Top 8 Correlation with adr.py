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
import seaborn as sns
import streamlit as st
st.write("# This demo shows Top 8 Correlation with adr")
# obtain dataset
data = pd.read_csv('hotel_bookings(1).csv')

# Data initialization
data['arrival_date_month'] = pd.to_numeric(data['arrival_date_month'], errors='coerce')
data['meal'] = pd.to_numeric(data['meal'], errors='coerce')
data['country'] = pd.to_numeric(data['country'], errors='coerce')
data['market_segment'] = pd.to_numeric(data['market_segment'], errors='coerce')
data['distribution_channel'] = pd.to_numeric(data['distribution_channel'], errors='coerce')
data['deposit_type'] = pd.to_numeric(data['deposit_type'], errors='coerce')
data['customer_type'] = pd.to_numeric(data['customer_type'], errors='coerce')
data['reservation_status'] = pd.to_numeric(data['reservation_status'], errors='coerce')
data['reservation_status_date'] = pd.to_numeric(data['reservation_status_date'], errors='coerce')

# Find the column that needs to be analyzed
columns_to_analyze = [
 'is_canceled',
 'lead_time',
 'arrival_date_year',
 'arrival_date_week_number',
 'arrival_date_day_of_month',
 'stays_in_weekend_nights',
 'stays_in_week_nights',
 'adults',
 'children',
 'babies',
 'is_repeated_guest',
 'previous_cancellations',
 'previous_bookings_not_canceled',
 'booking_changes',
 'agent',
 'company',
 'days_in_waiting_list',
 'adr',
 'required_car_parking_spaces',
 'total_of_special_requests',
]
data = data[columns_to_analyze]

# Find the most relevant eight variables
correlation_matrix = data.corr().abs().nlargest(8,'adr')['adr'].index
cm = data[correlation_matrix].corr()

# Draw a heat map
plt.figure(figsize=(12, 9))
sns.heatmap(cm, annot=True, cmap='Blues')
plt.title('Top 8 Correlation with adr');

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()




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

#show_code(data_frame_demo)
