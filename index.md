---
layout: default
title: Home
nav_order: 1
description: "Weather Prediction App"
permalink: /
---

# Weather Prediction App Documentation
{: .fs-9 }

This web app demonstrates the capabilities of using a ConvLSTM2D model to predict extreme weather events across Singapore.
{: .fs-6 .fw-300 }

[Get started now](https://jye-lim-weather.streamlit.app/){:target="_blank"}{: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View it on GitHub](https://github.com/jye-lim/weather_prediction_app){:target="_blank"}{: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Overview

Welcome to our weather prediction web app! This web app demonstrates the capabilities of using a ConvLSTM2D model to predict extreme weather events across Singapore. Through this web app, we hope to showcase the potential of using Deep Neural Networks to capture spatiotemporal dependencies within meteorological datasets to predict the onset of extreme weather events.

The accuracy of the deployed models in this web app has much room for improvement. However, we hope that by sharing our findings and potential areas for future research, we can contribute to developing more reliable forecasting systems for Singapore.

## Installation

To access the web app, clone the repo and follow the steps below to run it locally:

1. Create a virtual environment with `Python 3.10.6` and activate it.

    ```bash
    conda create -n wpa python=3.10.6
    conda activate wpa
    ```

2. Clone the repo.

    ```bash
    git clone https://github.com/jye-lim/weather_prediction_app
    ```

3. Navigate to the repo.

    ```bash
    cd weather_prediction_app
    ```

4. Install the required packages using the requirements.txt file.

    ```bash
    pip install -r requirements.txt
    ```

5. Run the app.py file

    ```bash
    streamlit run app.py
    ```

## User guide

Refer to the User Guide video to use the Web App in [our GitHub repo](https://github.com/jye-lim/weather_prediction_app#user-guide){:target="_blank"}.

## About the project

This Weather Prediction App is &copy; 2023-{{ "now" | date: "%Y" }} by [Lim Jian Ye](https://www.linkedin.com/in/limjianye/){:target="_blank"}, under the supervision of [Dr He Xiaogang](https://scholar.google.com/citations?user=AWfzBLMAAAAJ&hl=en){:target="_blank"}.

### License

This Weather Prediction App is distributed by an [MIT license](https://github.com/jye-lim/weather_prediction_app/blob/main/LICENSE){:target="_blank"}.

### Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, [email](mailto:jianye_lim@outlook.com), or any other method with the owners of this repository before making a change. Read more about becoming a contributor in [our GitHub repo](https://github.com/jye-lim/weather_prediction_app#contributing){:target="_blank"}.

#### Thank you to the contributors of this project!

<ul class="list-style-none">
{% for contributor in site.github.contributors %}
  <li class="d-inline-block mr-1">
     <a href="{{ contributor.html_url }}"><img src="{{ contributor.avatar_url }}" width="32" height="32" alt="{{ contributor.login }}"></a>
  </li>
{% endfor %}
</ul>
