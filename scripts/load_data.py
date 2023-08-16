import os
import streamlit as st
import numpy as np
import geopandas as gpd


@st.cache_resource
def loop_files(path, file_name, start_date, end_date):
    arr = None
    for year in range(start_date, end_date):
        part = 0
        while True:
            file_path = path + file_name + "_" + str(year) + "_" + str(part) + ".npy"
            if os.path.isfile(file_path):
                new_data = np.load(file_path)
                if arr is None:
                    arr = new_data
                else:
                    arr = np.concatenate([arr, new_data], axis=0)
                part += 1
            else:
                break

        # If no split files are found for a year, try to load the single annual file
        if part == 0:
            file_path = path + file_name + "_" + str(year) + ".npy"
            if os.path.isfile(file_path):
                new_data = np.load(file_path)
                if arr is None:
                    arr = new_data
                else:
                    arr = np.concatenate([arr, new_data], axis=0)
                
    return arr

def load_data(start_date, end_date):
    # Load precipitation
    prcp_path = "./data/precipitation/"
    prcp_true = loop_files(prcp_path, "prcp_true", start_date, end_date)
    prcp_pred = loop_files(prcp_path, "prcp_pred", start_date, end_date)

    # Load SPI
    spi_path = "./data/spi/"
    spi_true = loop_files(spi_path, "spi_true", start_date, end_date)
    spi_pred = loop_files(spi_path, "spi_pred", start_date, end_date)

    # Load coastlines
    world = gpd.read_file('./static/assets/ne_10m_coastline.shp')

    # Load reservoir data
    reservoirs_gdf = gpd.read_file("./data/singapore_reservoirs.geojson")
    return prcp_true, prcp_pred, spi_true, spi_pred, world, reservoirs_gdf
