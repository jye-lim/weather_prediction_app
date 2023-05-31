---
layout: default
title: Future Works
nav_order: 4
---

# Future Works
{: .no_toc }

Discussions on the future works for the web app.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

There are several opportunities for future research to improve the prediction of extreme weather events using the ConvLSTM2D model and better understand its limitations and potential enhancements. Here we discuss several avenues for consideration:

## Data Scaling

The predicted data could be scaled to match the mean of the WRF Simulated values. This scaling could be accomplished by applying min-max scaling to the predicted dataset using the min and max of the WRF Simulated values. The resultant scaled dataset could then be shifted by adding or subtracting a constant to align the means of the predictions and WRF Simulated values.

## Enhancing the FSS Loss Function

The model currently has a tendency to make "safe" predictions that avoid extreme values, such as 0 or extreme precipitation. Future research can further refine the FSS loss function to allow the model to better capture the extreme events that are central to this study.

## Improving Long-term Forecasting

![Precipitation Steps](../../assets/images/steps_prcp.png)
{: .text-center .my-6 }

WRF Simulated vs Predicted Precipitation at n-steps
{: .text-center .fs-3 .fw-300 }

The above plot demonstrates longer-term forecasting of precipitation, where n-Step Prediction refers to n number of days ahead the model is predicting. The results section in this documentation used the 1-Step Prediction model for its discussions. The plot shows the 1, 3, and 7-step predictions of the model. The model performs well for the 1-step prediction, but the performance degrades as the number of steps increases.

Although the larger step models perform significantly worse, we can still observe that the model is able to capture the location of intense precipitation. Future research could investigate potential improvements to the model's architecture, the inclusion of additional meteorological features, or alternative machine-learning techniques to enhance the model's longer-term forecasting capabilities.

## Investigating Regional Errors

![Mean Absolute Error Steps](../../assets/images/steps_error.png)
{: .text-center .my-6 }

Mean Absolute Error at n-steps
{: .text-center .fs-3 .fw-300 }

We computed the Mean Absolute Error (MAE) for each grid cell in the study area to investigate the spatial distribution of the model's error. Our analysis has revealed that the bottom-left corner of our area of interest experiences an unusually high error.

Further investigation of the dataset for this location should be performed to determine if the data within this region is reasonable. If the data proves to be reliable, additional research could aim to understand why the model performs poorly in this specific location.

## Categorical Prediction of SPI Classes

Adjusting the ConvLSTM2D model to perform categorical prediction of SPI classes, yielding a probabilistic output of the events, could be more useful in a practical setting. Our study attempted to incorporate a SoftMax output layer for this purpose, but this did not yield satisfactory results.

This could be due to the significant reduction in the dataset count when daily data is resampled to monthly steps. Future research could explore the use of Bayesian probability to compute the weights for each class, potentially improving the model's performance in this context.
