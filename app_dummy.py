import streamlit as st
import datetime

# Get current date and time
now = datetime.datetime.now()
max_date = now + datetime.timedelta(days=5)

st.title("Date and Time Input App")

# Date input
date_input = st.date_input("Select a date", value=now.date(), min_value=now.date(), max_value=max_date.date())

# Time input
time_input = st.time_input("Select a time")

# Submit button
if st.button("Submit"):
    # Process the inputs
    datetime_input = datetime.datetime.combine(date_input, time_input)
    st.write("Submitted Date and Time:", datetime_input)
