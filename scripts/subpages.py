import streamlit as st
import pandas as pd
from scripts.plot_functions import get_plots, show_distribution
from scripts.analysis_functions import display_analysis_section
from scripts.download import get_file_download_link


def display_about_page():
    # Add section headers and descriptions
    st.markdown("## Overview")
    st.markdown("""
    Welcome to our weather prediction web app! This web app demonstrates the capabilities of using a ConvLSTM2D model to predict extreme weather events across Singapore. 
    Through this web app, we hope to showcase the potential of using Deep Neural Networks to capture spatiotemporal dependencies within meteorological datasets to predict 
    the onset of extreme weather events. The accuracy of the deployed models in this web app has much room for improvement. However, we hope that by sharing our findings 
    and potential areas for future research, we can contribute to developing more reliable forecasting systems for Singapore.
    """)

    st.markdown("## Methodology")
    st.markdown("""
    The methodology for predicting extreme weather events in Singapore using the ConvLSTM2D model involves data pre-processing, model architecture design, and evaluation. 
    We used the statistically downscaled data from [SgCALE's WRF dataset](https://sgcale.github.io/research/climate-downscaling/), and select relevant variables. The data 
    is split into training, validation, and test sets and normalized based on the training set distribution.

    A custom loss function, [Fractions Skill Score](https://doi.org/10.48550/arXiv.2106.09757) (FSS) loss, is employed to compute the model loss across an area rather than 
    a pixel-to-pixel comparison. This approach prevents the model from being penalized twice for a reasonable prediction. The FSS loss is a mix of MSE and MAE losses, with 
    weights of 0.70 and 0.30, respectively, and computes the average precipitation within a user-defined mask size before calculating the weighted losses between the true 
    and predicted values.
    """)

    st.markdown("## User Guide")
    st.video("https://youtu.be/HqK29T7Tny8")
    
    st.markdown("## Future Works")
    st.markdown("""
    <ol>
        <li>
            <b><u>Data Scaling</u></b></br>
            Scale the predicted data to match the mean of our WRF Simulated values. Can be achieved by applying min-max scaling to the predicted dataset using 
            the WRF Simulated values before adding or subtracting the scaled dataset to align the means.
        </li></br>
        <li>
            <b><u>Improving the FSS Loss Function</u></b></br>
            Refine FSS loss to penalise the model from making "safe" predictions that avoid extreme values, such as 0 or extreme precipitation. This enhancement 
            could better capture the onset of extreme weather events.
        </li></br>
        <li>
            <b><u>Longer-term Forecasting</u></b></br>
            The ConvLSTM2D model currently does not perform well for longer-term forecasting. Future research could investigate potential improvements to the model 
            architecture, additional meteorological features, or alternative machine-learning techniques to enhance the model's performance in this regard.
        </li></br>
        <li>
            <b><u>Investigating Regional Errors</u></b></br>
            Our analysis revealed that the bottom-left corner of our area of interest has an unusually high error. Further investigation into the dataset for that 
            location is warranted to determine if the data is reasonable. If reasonable, additional studies to understand why the model performs poorly in that specific 
            location should be conducted.
        </li></br>
        <li>
            <b><u>Categorical Prediction of SPI Classes</u></b></br>
            An alternative approach would be to adjust the ConvLSTM2D model to perform categorical prediction of SPI classes, yielding a probabilistic output of the events. 
            During our study, we attempted to incorporate a SoftMax output layer for this purpose, but all iterations of the model performed poorly. This may be due to the 
            significant reduction in the dataset count when daily data is resampled to monthly steps. We also tried incorporating weights based on the inverse class 
            frequencies technique discussed earlier in the report, but this was also unsuccessful. Future research can explore the use of Bayesian probability to compute 
            the weights for each class, potentially improving model performance in this context.
        </li>
    </ol>
    """,
    unsafe_allow_html=True)

    st.markdown("## Disclaimers")
    st.markdown("""
    The data and predictions presented in this dashboard are for informational purposes only and should not be used for decision-making without further verification. 
    The creators of this dashboard are not responsible for any errors or inaccuracies in the data or predictions or for any decisions made based on the information 
    provided here.
    """)


def display_dashboard_page(world, rows, cols, xlat, xlong):
    # Get loaded values
    prcp_true = st.session_state['prcp_true']
    prcp_pred = st.session_state['prcp_pred']
    spi_true = st.session_state['spi_true']
    spi_pred = st.session_state['spi_pred']
    reservoirs_gdf = st.session_state['reservoirs_gdf']

    # Get user input values
    plot_type = st.session_state['plot_type']
    dates = st.session_state['dates']
    target = st.session_state['target']
    waterbody = st.session_state['waterbody']

    # Plot SPI for target date
    true, pred, true_reservoir, pred_reservoir = get_plots(world, rows, cols, xlat, xlong, plot_type, dates, target, waterbody, 
                                                           prcp_true, prcp_pred, spi_true, spi_pred, reservoirs_gdf)
    
    # Show data distribution
    show_distribution(true, pred, plot_type)

    # Store values in session state
    st.session_state['true_reservoir'] = true_reservoir
    st.session_state['pred_reservoir'] = pred_reservoir


def display_analysis_page():
    # Get values from session state
    plot_type = st.session_state['plot_type']
    dates = st.session_state['dates']
    year = st.session_state['year']
    waterbody = st.session_state['waterbody']
    true_reservoir = st.session_state['true_reservoir']
    pred_reservoir = st.session_state['pred_reservoir']

    # Display the analysis section
    display_analysis_section(plot_type, dates, year, waterbody, true_reservoir, pred_reservoir)


def display_download_page():
    st.write("## Download Reservoir Data")

    # Generate download link for reservoir geojson data
    st.write("### Reservoir Coordinates")
    file_name = "singapore_reservoirs.geojson"
    data_path = "./data/" + file_name
    download_link = get_file_download_link(data_path, "Download Reservoir Coordinates")
    st.markdown(download_link, unsafe_allow_html=True)

    # Read the precipitation data
    st.write("### Daily Mean Precipitation")
    file_name = "reservoir_mean_precipitation.csv"
    data_path = "./static/downloads/" + file_name
    df = pd.read_csv(data_path)

    st.write(df.head())

    # Generate download link for precipitation CSV
    download_link = get_file_download_link(data_path, "Download Daily Mean Precipitation")
    st.markdown(download_link, unsafe_allow_html=True)

    # Read the spi data
    st.write("### Monthly Mean SPI")
    file_name = "reservoir_mean_spi.csv"
    data_path = "./static/downloads/" + file_name
    df = pd.read_csv(data_path)

    st.write(df.head())

    # Generate download link for spi CSV
    download_link = get_file_download_link(data_path, "Download Monthly Mean SPI")
    st.markdown(download_link, unsafe_allow_html=True)
