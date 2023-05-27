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

[Get started now](#getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View it on GitHub](https://github.com/jye-lim/weather_prediction_app){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Overview

Welcome to our weather prediction web app! This web app demonstrates the capabilities of using a ConvLSTM2D model to predict extreme weather events across Singapore. Through this web app, we hope to showcase the potential of using Deep Neural Networks to capture spatiotemporal dependencies within meteorological datasets to predict the onset of extreme weather events.

The accuracy of the deployed models in this web app has much room for improvement. However, we hope that by sharing our findings and potential areas for future research, we can contribute to developing more reliable forecasting systems for Singapore.

## Getting started

To access the web app, follow the steps below to run it locally:

1. Clone the repo

    ```bash
    git clone https://github.com/jye-lim/weather_prediction_app
    ```

2. Install the required packages using the requirements.txt file

    ```bash
    pip install -r requirements.txt
    ```

3. Run the app.py file

    ```bash
    streamlit run app.py
    ```

## User guide

<video width="100%" height="auto" controls>
  <source src="./assets/videos/user_guide.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## About the project

This Weather Prediction App (2017-{{ "now" | date: "%Y" }}) by [Lim Jian Ye](https://www.linkedin.com/in/limjianye/), under the supervision of [Dr He Xiaogang](https://scholar.google.com/citations?user=AWfzBLMAAAAJ&hl=en).

### License

This Weather Prediction App is distributed by an [MIT license](https://github.com/jye-lim/weather_prediction_app/blob/main/LICENSE).

### Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, <a href="mailto:jianye_lim@outlook.com">email</a>, or any other method with the owners of this repository before making a change. Read more about becoming a contributor in [our GitHub repo](https://github.com/jye-lim/weather_prediction_app#contributing).

#### Thank you to the contributors of Just the Docs

<ul class="list-style-none">
{% for contributor in site.github.contributors %}
  <li class="d-inline-block mr-1">
     <a href="{{ contributor.html_url }}"><img src="{{ contributor.avatar_url }}" width="32" height="32" alt="{{ contributor.login }}"></a>
  </li>
{% endfor %}
</ul>
