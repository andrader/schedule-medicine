from pathlib import Path
import datetime as dt
from turtle import width
import streamlit as st
import pandas as pd

from schedmeds.med import Med
from schedmeds.parse_timedelta import strfdelta
from schedmeds.helpers import load_data, write_data


from add_med import add_med


DT_FMT = "%b %d, %H:%M"

PATH_DATA = Path("data/")
PATH_DATA.mkdir(parents=True, exist_ok=True)
SESSION_PICKLE_PATH = PATH_DATA / "data_meds.pickle"


def get_df_from_meds(meds):
    if not meds:
        return "No meds to show."
    data = []
    for med in meds.values():
        last = med.history[-1].strftime(DT_FMT)
        remainings = med.remaining

        taken = len(med.history)
        remaining = len(remainings)

        next = remainings[0].strftime(DT_FMT) if remaining else "Done"

        data.append(
            dict(
                name=med.name,
                interval=strfdelta(med.dose_interval),
                period=med.total_period,
                taken=taken,
                remaining=remaining,
                last=last,
                next=next,
            )
        )

    df = pd.DataFrame(data).set_index("name").astype(str)

    return df


## app CONTENT
st.set_page_config(
    page_title="My Medicines",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

with st.spinner("Loading meds data..."):
    if not "meds" in st.session_state:
        try:
            st.session_state["meds"] = load_data(SESSION_PICKLE_PATH)
        except FileNotFoundError:
            st.session_state["meds"] = {}
    meds = st.session_state["meds"]


# SIDEBAR

with st.sidebar:

    st.title("My Medicines 💊")
    tab1, tab2, tab3 = st.tabs(["Add/remove", "Register intake", "Session"])

    with tab1:
        add_med()

    with tab2:
        intake_sel_med = st.selectbox("Medication", meds)

        if intake_sel_med:

            med = meds[intake_sel_med]
            last = med.history[-1]

            td = med.dose_interval  # dt.timedelta(days=2)
            intake_time = st.slider(
                "Time",
                value=last + td,
                min_value=last,
                max_value=last + 2 * td,
                step=dt.timedelta(minutes=5),
                format="MMM D, HH:mm",
            )
            st.write(
                "Passed time:",
                strfdelta(intake_time - last),
            )

            record_intake = st.button("Record intake")
            if record_intake:
                # med.register_intake(1, intake_time)
                if intake_time not in med.history:
                    med.history.append(intake_time)
                    st.write(f"Med {intake_sel_med} was updated!")
                else:
                    st.write("Intake already exists")

    with tab3:
        col1, col2, col3 = st.columns(3)
        btn_load_file = col1.button("Reload")
        btn_write_file = col2.button("Write")
        if btn_load_file:
            try:
                st.session_state["meds"] = load_data(SESSION_PICKLE_PATH)
                col3.write("loaded meds!")
            except FileNotFoundError:
                col3.write("file not found.")
                st.session_state["meds"] = {}

        if btn_write_file:
            write_data(st.session_state["meds"], SESSION_PICKLE_PATH)
            col3.write("wrote meds!")


# APP

from plot_med import display_med, plot_med2


for med in meds.values():
    display_med(med)


if intake_sel_med in meds:
    with st.expander(f"Details of {intake_sel_med}", expanded=True):
        plot_med2(meds[intake_sel_med])
    


