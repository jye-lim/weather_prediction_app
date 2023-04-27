import streamlit as st
import numpy as np
from scripts.load_data import load_data
from scripts.sidebar import create_sidebar
from scripts.subpages import display_about_page, display_dashboard_page, display_analysis_page, display_download_page


def main():
    # Create a Streamlit application
    logo = "./static/images/logo.png"
    st.set_page_config(page_title="Weather App Dashboard", layout='wide', initial_sidebar_state='auto', page_icon=logo)
    st.title("Weather Prediction App")

    # Load data
    spi_true, spi_pred_dict, prcp_true, prcp_pred_dict, world, reservoirs_gdf = load_data()

    # Store key variables in session state
    st.session_state['spi_true'] = spi_true
    st.session_state['spi_pred_dict'] = spi_pred_dict
    st.session_state['prcp_true'] = prcp_true
    st.session_state['prcp_pred_dict'] = prcp_pred_dict
    st.session_state['reservoirs_gdf'] = reservoirs_gdf

    # Initialize session state variables if they do not exist
    variables = ['plot_type', 'dates', 'split_date', 'year', 'split_year', 'waterbody', 'true_target', 'pred_target', 'true_reservoir', 'pred_reservoir']
    for v in variables:
        if v not in st.session_state:
            st.session_state[v] = None

    # Self-define parameters and store key variables in session state
    start_date = 1981
    end_date = 2021
    train_split = 0.70
    val_split = 0.15
    n_input = 7
    rows = 1
    cols = 2
    xlat = np.load("./static/assets/coords_xlat.npy")
    xlong = np.load("./static/assets/coords_xlong.npy")

    # Initialize sidebar
    selected_page = create_sidebar(start_date, end_date, train_split, val_split, n_input, logo, reservoirs_gdf)

    if selected_page == "About":
        display_about_page()

    elif selected_page == "Dashboard":
        display_dashboard_page(world, rows, cols, xlat, xlong)
        display_analysis_page(start_date)
        
    elif selected_page == "Data":
        display_download_page()


if __name__ == "__main__":
    main()
