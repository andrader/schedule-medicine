import altair as alt
import streamlit as st
import datetime as dt
from schedmeds.parse_timedelta import strfdelta


def display_med(med):
    fmt = "%b %d, %H:%M"

    med.update_remaining()
    next_dose = med.remaining[0].strftime(fmt) if len(med.remaining) else ""

    col1, col2, col3 = st.columns([1,1,1])
    col1.header(med.name)
    col2.metric("Next intake at", next_dose)
    col3.metric("Next intake in", strfdelta(med.remaining[0] - dt.datetime.now()))

    st.write('---')

def plot_med2(med):

    df = med.get_df()
    


    base = alt.Chart(df.reset_index()).encode(
        alt.X("monthdate(history):O", title="intake"),
        alt.Y("hoursminutes(history)", title="hour of day"),
        
        tooltip=[
            alt.Tooltip("hoursminutes(history)", title="intake"),
            alt.Tooltip("hoursminutes(planned)", title="planned"),
            #alt.Tooltip("dif_hist_planned", title="dif_hist_planned"),
        ]
    ).properties(
        title='Planned vs Actual Intakes'
    )

    bar = base.mark_bar(size=5).encode(
        alt.Y2("hoursminutes(planned)"),
        color=alt.value("darkgray"),
        
    )

    
    point1 = base.mark_point(size=50).encode(
        alt.Y("hoursminutes(planned)", title="hour of day"),
        fill=alt.value("green"),
        stroke=alt.value("green"),
    )

    point2 = base.mark_point(size=50).encode(
        fill=alt.value("red"),
        stroke=alt.value("red"),
    )

    chart = bar + point1 + point2
    st.altair_chart(chart, use_container_width=True)

    st.markdown(f"Data for `{med.name}`")
    st.write(df.astype(str))