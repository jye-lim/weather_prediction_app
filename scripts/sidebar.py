import streamlit as st
import pandas as pd
import calendar
from streamlit_option_menu import option_menu


def navigation():
    with st.sidebar:
        selected_page = option_menu(
            menu_title=None,
            options=["About", "Dashboard", "Data"],
            icons=["house", "book", "list-task"],
            menu_icon="cast",
            default_index=0,
        )

    return selected_page


def create_sidebar(start_date, end_date, n_input, logo, reservoirs_gdf):

    dates = pd.date_range(start=str(start_date), end=str(end_date), freq='D')[:-1][n_input:]

    with st.sidebar:
        # Display logo
        st.image(logo, use_column_width='auto')

        # Navigation
        selected_page = navigation()

        # Select the plot type
        plot_type = st.selectbox('Plot Type', ['SPI', 'Precipitation'])

        # Target date selection
        year = st.selectbox('Year', range(start_date, end_date))
        month = st.selectbox('Month', range(1, 13))

        if plot_type == 'Precipitation':
            last_day = calendar.monthrange(year, month)[1]
            if (year == start_date) and (month == 1):
                day = st.selectbox('Day', range(n_input+1, last_day+1))
            else:
                day = st.selectbox('Day', range(1, last_day+1))
            target = dates.get_loc(f"{year}-{month:02d}-{day:02d}")

        elif plot_type == 'SPI':
            dates = pd.date_range(start=str(start_date), end=str(end_date), freq='M')
            target = dates.get_loc(f"{year}-{month:02d}").start

        waterbody = st.selectbox('Select Waterbody', reservoirs_gdf['name'].values)

    st.session_state['plot_type'] = plot_type
    st.session_state['dates'] = dates
    st.session_state['year'] = year
    st.session_state['target'] = target
    st.session_state['waterbody'] = waterbody

    return selected_page
