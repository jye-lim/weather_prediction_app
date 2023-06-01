---
layout: default
title: Methodology
nav_order: 2
---

# Methodology
{: .no_toc }

Discussions on the methodology of the project.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Model Selection

### CNN-LSTM

For the task of weather prediction using machine learning, the CNN-LSTM model is typically used. A CNN-LSTM model utilizes a convolutional layer to learn spatial features, which are then passed to an LSTM layer to capture temporal dependencies. The final fully connected layer processes the LSTM layer's output to minimize variability and improve predictions ([Sainath et al., 2015](https://ieeexplore.ieee.org/document/7178838){:target="_blank"}). However, the LSTM layer linearizes its input to the fully connected layer into a 1-dimensional array ([Hu et al., 2020](https://ieeexplore.ieee.org/document/8960629){:target="_blank"}), leading to a loss of spatial considerations while retaining only the temporal ones ([Shi et al., 2015](https://doi.org/10.48550/arXiv.1506.04214){:target="_blank"}); ([Hu et al., 2020](https://ieeexplore.ieee.org/document/8960629){:target="_blank"}).

![CNN-LSTM Model Architecture](../../assets/images/cnn-lstm.png)
{: .text-center .my-6 }

Typical CNN-LSTM Model Architecture ([Oh et al., 2018](https://pubmed.ncbi.nlm.nih.gov/29903630/){:target="_blank"})
{: .text-center .fs-3 .fw-300 }

### ConvLSTM2D

In contrast, ConvLSTM2D performs convolutional operations **within** the LSTM cell, allowing for a 3-dimensional input incorporating spatial and temporal dimensions ([Hu et al., 2020](https://ieeexplore.ieee.org/document/8960629){:target="_blank"}). This results in the retention of both spatial and temporal features, thus enhancing the learning of correlations within the data ([Shi et al., 2015](https://doi.org/10.48550/arXiv.1506.04214){:target="_blank"}); ([Gaur et al., 2020](https://doi.org/10.48550/arXiv.2203.13263){:target="_blank"}).

![ConvLSTM2D Inner Structure](../../assets/images/convlstm2d.png)
{: .text-center .my-6 }

Inner Structure of ConvLSTM2D ([Shi et al., 2015](https://doi.org/10.48550/arXiv.1506.04214){:target="_blank"})
{: .text-center .fs-3 .fw-300 }

## Data Source

This research utilizes the Weather Research & Forecasting (WRF) Model [dataset](https://sgcale.github.io/research/climate-downscaling/){:target="_blank"} provided by Singapore's Climate ArtificiaL intelligence Engine ([SgCALE](https://sgcale.github.io/){:target="_blank"}). The data was bias-corrected, downscaled, and refined from Global Climate Models (GCMs) and the European Centre for Medium-Range Weather Forecasts Reanalysis 5 (ERA5) dataset.

![Downscaling](../../assets/images/downscaling.png)
{: .text-center .my-6 }

Data Downscaling Process ([SgCALE, 2022](https://sgcale.github.io/research/climate-downscaling/){:target="_blank"})
{: .text-center .fs-3 .fw-300 }

## Dataset Characteristic

| Characteristics | Details                                                                      |
|:----------------|:-----------------------------------------------------------------------------|
| Source          | SgCALE                                                                       |
| Resolution      | 500 m grids                                                                  |
| Time Frame      | 1981 - 2020                                                                  |
| NaN Filling     | Linear interpolation of adjacent grids                                       |
| Input Variables | Temperature, Relative Humidity, Surface Pressure, Cloud Fraction, Wind Speed |
| Output Variable | Precipitation                                                                |
| Dataset Split   | Training (70%), Validation (15%), Test (15%)                                 |
| Batch Size      | 32                                                                           |
| Lookback        | 7                                                                            |

The model takes in data from the past 7-days *(t-6, t-5, ..., t)* to predict the next day precipitation *(t+1)*.

## ConvLSTM2D Model Architecture

The ConvLSTM2D model was designed with an input layer, two hidden ConvLSTM2D layers, a batch normalization layer, and a dense output layer.

| Layer               | Filters/Units | Filter Size | Output Shape            | Parameters |
|:--------------------|:--------------|:------------|:------------------------|:-----------|
| ConvLSTM2D          | 64            | 3 x 3       | (None, 7, 120, 160, 64) | 159,232    |
| Batch Normalisation | -             | -           | (None, 7, 120, 160, 64) | 256        |
| ConvLSTM2D          | 64            | 3 x 3       | (None, 7, 120, 160, 64) | 295,168    |
| Dense               | 1             | -           | (None, 120, 160, 1)     | 65         |

### Considerations

1. Two ConvLSTM2D layers with 64 filters were ideal for learning the dataset's spatiotemporal dependencies.
   1. More layers or filters led to overfitting and extended training times.
   2. Fewer layers or filters compromised performance.
2. Batch normalization was utilized to:
   1. Ensure faster model convergence by normalizing data between layers, as gradients maintain similar scales.
   2. Mitigate the risk of vanishing or exploding gradients as they maintain similar scales.
   3. Reduce overfitting by reducing the internal covariate shift.
3. Batch normalization is not used before the fully connected layer as it negatively impacts performance.
   1. Likely due to undesired shift in our data scale, mean, or variance.

## Model Training

We trained the proposed ConvLSTM2D model for 100 epochs, employing only model checkpointing without early stopping to save the model with the best validation loss during training. This approach helps avoid the double descent phenomenon ([Heckel & Yilmaz, 2020](https://arxiv.org/abs/2007.10099){:target="_blank"}) and ensures optimal model performance.

As for the optimization method, we chose the Adaptive Moment Estimation (Adam) optimizer. Adam is a popular choice due to its adaptive nature, adjusting the learning rate throughout the training process, thereby ensuring faster convergence and improved generalisation of the model.

### Loss Function

Unlike traditional convolutional outputs where loss computations often revolve around pixel-to-pixel comparisons, our model utilizes a custom loss function that computes loss over an area.

![FSS Loss](../../assets/images/fss.png)
{: .text-center .my-6 }

Neighbourhood Scanning Loss Function ([Uphoff, et al., 2021](https://arxiv.org/abs/2106.09757){:target="_blank"})
{: .text-center .fs-3 .fw-300 }

The predicted grids with rain are only one grid away from the observed values. Using the built-in loss functions, such as Mean Squared Error (MSE) loss, would result in the model being penalized **twice** for what could be considered a reasonable prediction. The first penalty would be applied to the grid that has observed precipitation but no predicted precipitation, while the second would apply to the grid with predicted precipitation but no observed precipitation. This is despite the model having fairly accurately identified the areas experiencing precipitation.

To overcome this issue, we implement a custom loss function called the Fractions Skill Score ([FSS](https://arxiv.org/abs/2106.09757){:target="_blank"}) loss. The FSS loss scans an area of size *m* x *m* (where *m* refers to the user-defined mask size), calculating the average precipitation within that area, and then computing the losses between the true and predicted values. This approach better accommodates the spatial nature of our data and mitigates overly penalizing reasonable predictions.

```bash
# Define modified FSS loss
def make_FSS_loss(mask_size):
    def my_FSS_loss(y_true, y_pred):

        cutoff = 0.5
        c = 10

        y_true_binary = tf.math.sigmoid( c * ( y_true - cutoff ))
        y_pred_binary = tf.math.sigmoid( c * ( y_pred - cutoff ))

        pool1 = tf.keras.layers.AveragePooling2D(pool_size=(mask_size, mask_size), strides=(1, 1), padding='same')
        y_true_density = pool1(y_true_binary);
        n_density_pixels = tf.cast( (tf.shape(y_true_density)[1] * tf.shape(y_true_density)[2]) , tf.float32 )

        pool2 = tf.keras.layers.AveragePooling2D(pool_size=(mask_size, mask_size), strides=(1, 1), padding='same')
        y_pred_density = pool2(y_pred_binary);

        # calculate MSE
        MSE_n = tf.keras.losses.MeanSquaredError()(y_true_density, y_pred_density)

        O_n_squared_image = tf.keras.layers.Multiply()([y_true_density, y_true_density])
        O_n_squared_vector = tf.keras.layers.Flatten()(O_n_squared_image)
        O_n_squared_sum = tf.reduce_sum(O_n_squared_vector)

        M_n_squared_image = tf.keras.layers.Multiply()([y_pred_density, y_pred_density])
        M_n_squared_vector = tf.keras.layers.Flatten()(M_n_squared_image)
        M_n_squared_sum = tf.reduce_sum(M_n_squared_vector)
        
        MSE_n_ref = (O_n_squared_sum + M_n_squared_sum) / n_density_pixels
        
        # calculate MAE
        MAE_n = tf.keras.losses.MeanAbsoluteError()(y_true_density, y_pred_density)
        MAE_n_ref = tf.reduce_sum(tf.abs(tf.subtract(y_true_density, y_pred_density))) / n_density_pixels

        # initialize weights
        alpha = 0.70 # for MSE loss 
        beta = 0.30 # for MAE loss 
        my_epsilon = tf.keras.backend.epsilon() # this is 10^(-7)

        return (alpha * (MSE_n / (MSE_n_ref + my_epsilon))) + (beta * (MAE_n / (MAE_n_ref + my_epsilon)))
    return my_FSS_loss
```

We modified the FSS loss to combine MSE and Mean Absolute Error (MAE) loss, weighted at 0.70 and 0.30 respectively. This places slightly less emphasis on the extreme values and more on the average values, which might be counterintuitive for our focus on the prediction of extreme weather events. However, we found that this approach resulted in better model prediction for both floods and droughts. The overprediction of precipitation intensity across all areas result in the underprediction of drought intensity, which is undesirable. Lastly, we used a mask size of 9 x 9 to scan the area, as it demonstrated the best performance.