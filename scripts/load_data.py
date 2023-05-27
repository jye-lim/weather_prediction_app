import streamlit as st
import numpy as np
import geopandas as gpd


@st.cache_resource
def load_data():
    # Load precipitation
    prcp_path = "./data/precipitation/"
    prcp_true = np.load(prcp_path + "prcp_true.npy")
    prcp_pred = np.load(prcp_path + "prcp_pred.npy")

    # Load SPI
    spi_path = "./data/spi/"
    spi_true = np.load(spi_path + "spi_true.npy")
    spi_pred = np.load(spi_path + "spi_pred.npy")

    # Load coastlines
    world = gpd.read_file('./static/assets/ne_10m_coastline.shp')

    # Load reservoir data
    reservoirs_gdf = gpd.read_file("./data/singapore_reservoirs.geojson")
    return prcp_true, prcp_pred, spi_true, spi_pred, world, reservoirs_gdf
