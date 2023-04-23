import streamlit as st
import pandas as pd
import calendar
from streamlit_option_menu import option_menu


def navigation():
    with st.sidebar:
        selected_page = option_menu(
            menu_title=None,
            options=["About", "Dashboard", "Data"],
            icons=["house", "book", "envelope"],
            menu_icon="cast",
            default_index=0,
        )

    return selected_page


def create_sidebar(start_date, end_date, train_split, val_split, n_input, logo, reservoirs_gdf):

    dates = pd.date_range(start=str(start_date), end=str(end_date), freq='D')[:-1]
    split_year = dates[int(len(dates)*(train_split + val_split))].year

    with st.sidebar:
        # Display logo
        st.image(logo, use_column_width='auto')

        # Navigation
        selected_page = navigation()

        # Select the plot type
        plot_type = st.selectbox('Plot Type', ['SPI', 'Precipitation'])

        # Create buttons to select the step
        step = st.radio('Select the step', [1, 3, 7], horizontal=True, index=0)

        # Target date selection
        year = st.selectbox('Year', range(split_year, end_date))
        month = st.selectbox('Month', range(1, 13))
        split_date = dates[int(len(dates) * (train_split + val_split)) + n_input]

        if plot_type == 'Precipitation':
            last_day = calendar.monthrange(year, month)[1]
            if (year == split_date.year) and (month == split_date.month):
                day = st.selectbox('Day', range(split_date.day, last_day+1))
            else:
                day = st.selectbox('Day', range(1, last_day+1))

            true_target = dates.get_loc(f"{year}-{month:02d}-{day:02d}")
            pred_target = true_target - dates.get_loc(f"{split_date.year}-{split_date.month:02d}-{split_date.day:02d}")

        elif plot_type == 'SPI':
            dates = pd.date_range(start=str(start_date), end=str(end_date), freq='M')
            true_target = dates.get_loc(f"{year}-{month:02d}").start
            pred_target = true_target - dates.get_loc(f"{split_date.year}-{split_date.month:02d}").start

        waterbody = st.selectbox('Select Waterbody', reservoirs_gdf['name'].values)

    st.session_state['plot_type'] = plot_type
    st.session_state['step'] = step
    st.session_state['dates'] = dates
    st.session_state['split_date'] = split_date
    st.session_state['year'] = year
    st.session_state['split_year'] = split_year
    st.session_state['true_target'] = true_target
    st.session_state['pred_target'] = pred_target
    st.session_state['waterbody'] = waterbody

    return selected_page
