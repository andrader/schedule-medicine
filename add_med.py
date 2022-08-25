import streamlit as st
import datetime as dt
from schedmeds.med import Med

def add_med():

    meds = st.session_state.meds

    med_name = st.text_input("Name")

    col1, col2 = st.columns(2)
    dose_interval = col1.text_input("Dose interval ('12h', '1d')", value='12h')
    total_period = col2.text_input("Total period ('7d')", value='7d')
    start_date = col1.date_input("Start Date")
    start_time = col2.text_input("Start Time", value=dt.datetime.now().time().strftime('%H:%M'))
    
    start_datetime = dt.datetime.combine(start_date, dt.time.fromisoformat(start_time))

    if med_name in meds:
        if col1.button("Update", key="add_med"):
            # update
            med = meds[med_name]
            med.med_name = med_name
            med.dose_interval = dose_interval
            med.total_period = total_period
            med.history[0] = start_datetime
            st.write(f"Updated {med_name}!")
    else:
        if col1.button("Add", key="add_med"):
            # create
            med = Med(
                med_name, dose_interval, total_period, history=[start_datetime]
            )
            meds[med_name] = med

            st.write(f"Added {med_name}!")
    
    if med_name in meds:
        if col2.button("Delete", key="del_med"):
            _=meds.pop(med_name)
            st.write(f"Deleted {med_name}!")