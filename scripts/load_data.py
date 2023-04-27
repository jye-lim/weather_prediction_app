import streamlit as st
import numpy as np
import geopandas as gpd


@st.cache_resource
def load_data():
    # Load precipitation
    prcp_path = "./data/precipitation/"
    prcp_true = np.load(prcp_path + "prcp_true.npy")
    prcp_pred1 = np.load(prcp_path + "prcp_pred_1step.npy")
    prcp_pred3 = np.load(prcp_path + "prcp_pred_3step.npy")
    prcp_pred7 = np.load(prcp_path + "prcp_pred_7step.npy")
    prcp_pred_dict = {1: prcp_pred1, 3: prcp_pred3, 7: prcp_pred7}

    # Load SPI
    spi_path = "./data/spi/"
    spi_true = np.load(spi_path + "spi_true.npy")
    spi_pred1 = np.load(spi_path + "spi_pred_1step.npy")
    spi_pred3 = np.load(spi_path + "spi_pred_3step.npy")
    spi_pred7 = np.load(spi_path + "spi_pred_7step.npy")
    spi_pred_dict = {1: spi_pred1, 3: spi_pred3, 7: spi_pred7}

    # Load coastlines
    world = gpd.read_file('./static/assets/ne_10m_coastline.shp')

    # Load reservoir data
    reservoirs_gdf = gpd.read_file("./data/singapore_reservoirs.geojson")
    return spi_true, spi_pred_dict, prcp_true, prcp_pred_dict, world, reservoirs_gdf
