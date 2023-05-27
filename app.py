import streamlit as st
import numpy as np
from scripts.load_data import load_data
from scripts.sidebar import create_sidebar
from scripts.subpages import display_about_page, display_dashboard_page, display_analysis_page, display_download_page


def main():
    # Create a Streamlit application
    logo = "./static/images/logo.png"
    st.set_page_config(page_title="Weather Prediction App", layout='wide', initial_sidebar_state='auto', page_icon=logo)
    st.title("Weather Prediction App")

    # Load data
    prcp_true, prcp_pred, spi_true, spi_pred, world, reservoirs_gdf = load_data()

    # Store key variables in session state
    st.session_state['prcp_true'] = prcp_true
    st.session_state['prcp_pred'] = prcp_pred
    st.session_state['spi_true'] = spi_true
    st.session_state['spi_pred'] = spi_pred
    st.session_state['reservoirs_gdf'] = reservoirs_gdf

    # Initialize session state variables if they do not exist
    variables = ['plot_type', 'dates', 'year', 'waterbody', 'target', 'true_reservoir', 'pred_reservoir']
    for v in variables:
        if v not in st.session_state:
            st.session_state[v] = None

    # Self-define parameters and store key variables in session state
    start_date = 2015
    end_date = 2021
    n_input = 7
    rows = 1
    cols = 2
    xlat = np.load("./static/assets/coords_xlat.npy")
    xlong = np.load("./static/assets/coords_xlong.npy")

    # Initialize sidebar
    selected_page = create_sidebar(start_date, end_date, n_input, logo, reservoirs_gdf)

    if selected_page == "About":
        display_about_page()

    elif selected_page == "Dashboard":
        display_dashboard_page(world, rows, cols, xlat, xlong)
        display_analysis_page()
        
    elif selected_page == "Data":
        display_download_page()


if __name__ == "__main__":
    main()
