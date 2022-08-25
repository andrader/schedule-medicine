from pathlib import Path
import datetime as dt
import pickle
from time import sleep

import streamlit as st
import pandas as pd
import numpy as np

from schedmeds.med import Med


MEDS_PATH = Path("meds/")
DT_FMT = "%b %d, %H:%M"




# show a dataframe with all meds
def load_all_meds(path):
    med_paths = Path(path).glob("*.pickle")
    dict_meds = {}
    for med_path in med_paths:
        med = Med.load(med_path)
        dict_meds[med.name] = med
    return dict_meds


def write_meds(meds, path):
    s = pickle.dumps(meds, fix_imports=True)
    Path(path).write_bytes()


def load_meds(path):
    return pickle.loads(Path(path).read_bytes())

def get_df_from_meds(meds):
    if not meds:
        return "No meds to show."
    data = []
    for med in meds.values():

        last = med.history[-1].strftime(DT_FMT)
        remaining = med.get_remaining_doses()
        if len(remaining):
            next = remaining[0].strftime(DT_FMT)
        else:
            next = "Done"

        data.append(dict(name=med.name, interval=med.dose_interval, last=last, next=next))

    df = pd.DataFrame(data).set_index("name").astype(str)

    return df

def load_meds_to_session():
    if not 'meds' in st.session_state:
        try:
            st.session_state['meds'] = load_meds(SESSION_PICKLE_PATH)
        except FileNotFoundError:
            st.session_state['meds'] = {}
    return st.session_state['meds']




 
## app CONTENT
SESSION_PICKLE_PATH = MEDS_PATH/'allmeds.pickle'

with st.spinner("Loading meds data..."):
    meds = load_meds_to_session()



st.title("Medications")

df = get_df_from_meds(meds)
st.write(df)

st.caption(f'last updated {str(dt.datetime.now())}')

st.markdown("---")

# SIDEBAR

with st.sidebar:

    with st.expander('Session'):
        col1, col2, col3 = st.columns(3)
        btn_load_file = col1.button('Load')
        btn_write_file = col2.button('Write')
        if btn_load_file:
            meds = load_meds_to_session()
            col3.write('loaded meds!')
        
        if btn_write_file:
            write_meds(meds, SESSION_PICKLE_PATH)
            col3.write('wrote meds!')

    with st.expander('Record intake'):
        intake_sel_med = st.selectbox("Medication", meds)

        if intake_sel_med:

            med = meds[intake_sel_med]
            last = med.history[-1]

            td = dt.timedelta(days=2)
            intake_time = st.slider(
                "Time", 
                #value=now, 
                min_value=last, 
                max_value=last+td,
                step=dt.timedelta(minutes=1),
                format="MMM D, HH:mm")
            st.write("Intake time:", intake_time)

            record_intake = st.button("Record intake")
            if record_intake:
                st.write(f"Med {intake_sel_med} was updated!")
    

    with st.expander('Add Med'):

        med_name = st.text_input("Name")

        col1, col2 = st.columns(2)

        with col1:
            dose_interval = st.text_input("Dose interval ('12h', '1d')")
            start_date = st.date_input('Start Date')
        with col2:
            total_period = st.text_input("Total period ('7d')")
            start_time = st.slider(
                "Start Time",
                value=dt.time(),
                step=dt.timedelta(minutes=5))
        
        start_datetime = dt.datetime.combine(start_date, start_time)
        
        add_med = st.button("Add Med", key="add_med")
        if add_med:
            # create Med obj and writes to file
            with st.spinner("Adding..."):
                med = Med(med_name, dose_interval, total_period, history=[start_datetime])
                meds[med_name] = med
                #med.save(MEDS_PATH / (med.name + ".pickle"))

            st.write("success!")
        
    with st.expander('Del Med'):
        selected = st.multiselect('Meds', meds)
        [meds.pop(key) for key in selected]

    



st.session_state['meds'] = meds


