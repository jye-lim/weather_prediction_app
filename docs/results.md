---
layout: default
title: Results
nav_order: 3
---

# Results
{: .no_toc }

Discussions on the predictions of the web app.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Overview

The web app is capable of predicting daily precipitation of our area of study from 2015 to 2020. While using the web app, the user can select their timestep of interest and compare the predicted results with the WRF simulated data, which serves as our "true" data for comparison. Additionally, the web app can also show the computed Standardized Precipitation Index (SPI) values for the predicted and WRF simulated precipitation.

This section will demonstrate the prediction capabilities of the web app for a single timestep and provide some insights to it by analyzing the results. The plots from this page, including the analysis, are all generated from the web app. We strongly encourage you to try out the web app and explore the results for yourself!

## Precipitation

![Predicted Precipitation](../../assets/images/predicted_prcp.png)
{: .text-center .my-6 }

WRF Simulated vs Predicted Precipitation
{: .text-center .fs-3 .fw-300 }

The model tends to overpredict the intensity of precipitation, yet it accurately captures areas experiencing intense precipitation. This overestimation could be primarily due to the loss function employed in the model, which heavily weighs the Mean Squared Error (MSE) component, thereby significantly penalizing the incorrect predictions of extreme values.

Predicting the location of intense precipitation accurately is important, particularly for flood forecasting. The predicted precipitation values can help assess the potential for flooding and evaluate the effectiveness of the local drainage networks. However, the overprediction of precipitation may pose challenges when computing the SPI values. This is further discussed in the [analysis](#analysis-of-predictions) section.

## Standardized Precipitation Index

Our research focuses on the prediction of extreme weather events, such as droughts and floods. To achieve this, we use the SPI as a metric to quantify the severity of droughts and floods. The SPI is a widely used drought index that is used to quantify the severity of droughts and floods. It is a measure of the number of standard deviations by which the precipitation deviates from the long-term mean precipitation. The following table summarizes the SPI values and their corresponding drought and flood categories.

| SPI Value     | Classification |
|:-------------:|:--------------:|
| ≥ 2.00        | Extremely Wet  |
| 1.50 - 1.99   | Severely Wet   |
| 1.00 - 1.49   | Moderately Wet |
| -0.99 - 0.99  | Near Normal    |
| -1.00 - -1.49 | Moderately Dry |
| -1.50 - -1.99 | Severely Dry   |
| ≤ -2.00       | Extremely Dry  |

For our research, we employ the 1-month SPI to quantify the severity of droughts and floods. The SPI values are computed for each grid cell in the study area. The SPI values are computed for the WRF simulated precipitation and our predicted precipitation. The SPI values are computed for each grid cell in the study area. The SPI values are computed for the observed precipitation and the predicted precipitation.

![Predicted SPI](../../assets/images/predicted_spi.png)
{: .text-center .my-6 }

WRF Simulated vs Predicted SPI
{: .text-center .fs-3 .fw-300 }

The SPI of the predicted values overestimates flood intensity and underestimates drought intensity, likely due to the ConvLSTM2D model's overprediction of precipitation across all grids and timesteps. Since our model tends to overpredict the intensity of precipitation, the higher predicted mean precipitation results in higher SPI values.

## Analysis of Predictions

Instead of averaging the predicted precipitation values across all grids, we can also analyze the predictions at key locations, such as waterbodies across Singapore. For this analysis, we will focus on the Upper Peirce Reservoir. For analysis of other waterbodies, do check out the web app, which offers analysis of more than 50 waterbodies across Singapore.

### Precipitation Analysis

![Upper Peirce Reservoir Precipitation](../../assets/images/upper_peirce_reservoir_prcp.png)
{: .text-center .my-6 }

Upper Peirce Reservoir Precipitation
{: .text-center .fs-3 .fw-300 }

To evaluate the precipitation predictions for Upper Peirce Reservoir, we compute the mean precipitation across each time step and generate a time series graph.

![Upper Peirce Reservoir Precipitation Time Series](../../assets/images/timeseries_prcp.png)
{: .text-center .my-6 }

Upper Peirce Reservoir Precipitation Time Series
{: .text-center .fs-3 .fw-300 }

Key observations include:

1. The overall mean precipitation across all time steps for the predicted values is slightly higher than that of the WRF Simulation - specifically, 9.04 mm for the model predictions and 7.13 mm for the WRF Simulation.

2. The model rarely predicts precipitation to be zero, which is a frequent observation in reality. This tendency is likely due to the strong emphasis on the MSE loss in the model, which heavily penalizes large discrepancies between predicted and actual values. Thus, the model may be motivated to maintain a higher, non-zero baseline to minimize the magnitude of the error.

3. Despite having a higher predicted baseline, the model tends to underpredict extreme precipitation across all time steps. This behavior could be attributed to the heavy penalties associated with large errors in the model's loss function. The model may aim to limit its predictions of extreme precipitation to a lower threshold to minimize the risk of high losses in case of inaccurate predictions.

### SPI Analysis

![Upper Peirce Reservoir SPI](../../assets/images/upper_peirce_reservoir_spi.png)
{: .text-center .my-6 }

Upper Peirce Reservoir SPI
{: .text-center .fs-3 .fw-300 }

Similarly, we can also evaluate the SPI predictions for Upper Peirce Reservoir by computing the mean SPI across each time step and generating a time series graph.

![Upper Peirce Reservoir SPI Time Series](../../assets/images/timeseries_spi.png)
{: .text-center .my-6 }

Upper Peirce Reservoir SPI Time Series
{: .text-center .fs-3 .fw-300 }

We can also plot the histogram of the mean SPI values for the daily timesteps for both the WRF Simulation and the predicted values. The vertical lines on the histogram represent the mean SPI values for our selected timestep of January 2015.

![Upper Peirce Reservoir SPI Time Series](../../assets/images/histogram_spi.png)
{: .text-center .my-6 }

Upper Peirce Reservoir SPI Histogram
{: .text-center .fs-3 .fw-300 }

Key observations include:

1. The predicted SPI follows the same general trend as the WRF Simulated values but at an elevated level, as depicted in the time series plot.
2. The histogram plot reinforces this observation by showing a higher mean for the predicted values. Specifically, on January 2015, the mean predicted SPI is 1.21, compared to the WRF Simulated mean of 0.58 for Upper Peirce Reservoir.
3. This tendency of the model to overpredict SPI, akin to the precipitation predictions, is likely due to its loss function configuration, which places a heavy emphasis on the MSE component and significantly penalizes inaccurate predictions of extreme values.
