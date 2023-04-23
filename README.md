# **Weather Prediction App**

-- Public link coming soon! --

## **Overview**

<p>
    Welcome to our weather prediction web app! This web app demonstrates the capabilities of using a ConvLSTM2D model to predict extreme weather events across Singapore. Through this web app, we hope to showcase the potential of using Deep Neural Networks to capture spatiotemporal dependencies within meteorological datasets to predict the onset of extreme weather events. The accuracy of the deployed models in this web app has much room for improvement. However, we hope that by sharing our findings and potential areas for future research, we can contribute to developing more reliable forecasting systems for Singapore.
</P>
<p>
    The folder structure is as follows:
</p>
<p>
    ...</br>
    ├─── data</br>
    │&nbsp;&nbsp;&nbsp;└─── precipitation : <i>(data in .npy)</i></br>
    │&nbsp;&nbsp;&nbsp;└─── precipitation : <i>(data in .npy)</i></br>
    ├─── scripts</br>
    ├─── static</br>
    │&nbsp;&nbsp;&nbsp;└─── assets : <i>(coordinates in .npy)</i></br>
    │&nbsp;&nbsp;&nbsp;└─── downloads : <i>(data in .csv)</i></br>
    │&nbsp;&nbsp;&nbsp;└─── images : <i>(images in .png)</i></br>
    ├─── .gitattributes</br>
    ├─── .gitignore</br>
    ├─── app.py</br>
    ├─── LICENSE</br>
    ├─── README.md</br>
    └─── requirements.txt</br>
    ...
</p>
<ul>
    <li>data: Contains WRF simulated and predicted data for plotting</li>
    <li>scripts: Contains self-defined functions for the web app</li>
    <li>static: Contains files that remains unchanged</li>
</ul>

## **Usage**

To access the web app, either use the public link at the top of this README document or fork it and follow the steps below to run it locally:

1. Ensure that **Python 3.10.6** and the required packages listed in requirements.txt are installed
2. Run the command `pip install -r requirements.txt` to install the necessary packages
3. Access the web app locally by running the command `streamlit run app.py` in the root directory

## **Methodology**

<p>
    The methodology for predicting extreme weather events in Singapore using the ConvLSTM2D model involves data pre-processing, model architecture design, and evaluation. We use the SgCALE's WRF dataset, perform statistical downscaling to refine its spatial resolution, and select relevant variables. The data is split into training, validation, and test sets and normalized based on the training set distribution.
</p>
<p>
    A custom loss function, Fractions Skill Score (FSS) loss, is employed to compute the model loss across an area rather than a pixel-to-pixel comparison. This approach prevents the model from being penalized twice for a reasonable prediction. The FSS loss is a mix of MSE and MAE losses, with weights of 0.70 and 0.30, respectively, and computes the average precipitation within a user-defined mask size before calculating the weighted losses between the true and predicted values.
</p>

## **Future Works**

<ol>
    <li>
        <u><b>Data Scaling</b></u>
        <p>
            Scale the predicted data to match the mean of our WRF Simulated values. Can be achieved by applying min-max scaling to the predicted dataset using the WRF Simulated values before adding or subtracting the scaled dataset to align the means.
        </p>
    </li>
    <li>
        <u><b>Improving the FSS Loss Function</b></u>
        <p>
            Refine FSS loss to penalise the model from making "safe" predictions that avoid extreme values, such as 0 or extreme precipitation. This enhancement could better capture the onset of extreme weather events.
        </p>
    </li>
    <li>
        <u><b>Longer-term Forecasting</b></u>
        <p>
            The ConvLSTM2D model currently does not perform well for longer-term forecasting. Future research could investigate potential improvements to the model architecture, additional meteorological features, or alternative machine-learning techniques to enhance the model's performance in this regard.
        </p>
    </li>
    <li>
        <u><b>Investigating Regional Errors</b></u>
        <p>
            Our analysis revealed that the bottom-left corner of our area of interest has an unusually high error. Further investigation into the dataset for that location is warranted to determine if the data is reasonable. If reasonable, additional studies to understand why the model performs poorly in that specific location should be conducted.
        </p>
    </li>
    <li>
        <u><b>Categorical Prediction of SPI Classes</b></u>
        <p>
            An alternative approach would be to adjust the ConvLSTM2D model to perform categorical prediction of SPI classes, yielding a probabilistic output of the events. During our study, we attempted to incorporate a SoftMax output layer for this purpose, but all iterations of the model performed poorly. This may be due to the significant reduction in the dataset count when daily data is resampled to monthly steps. We also tried incorporating weights based on the inverse class frequencies technique discussed earlier in the report, but this was also unsuccessful. Future research can explore the use of Bayesian probability to compute the weights for each class, potentially improving model performance in this context.
        </p>
    </li>
</ol>

## **Disclaimers**

<p>
    The data and predictions presented in this dashboard are for informational purposes only and should not be used for decision-making without further verification. The creators of this dashboard are not responsible for any errors or inaccuracies in the data or predictions or for any decisions made based on the information provided here.
</p>
