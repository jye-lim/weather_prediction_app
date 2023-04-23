import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from scipy.stats import genextreme as gev


def add_mean_annotation(fig, mean_value, text_template, color):
    fig.add_annotation(
        text=text_template.format(mean_value),
        xref="paper",
        yref="y",
        x=1,
        y=mean_value,
        yshift=-12 if color == "red" else 12,
        showarrow=False,
        font=dict(color=color),
        bgcolor="rgba(255, 255, 255, 0.7)",
        bordercolor="white",
        borderwidth=1
    )


def get_true_pred_max(dates, true_reservoir, pred_reservoir, split_date):
    split_idx = dates.get_loc(f"{split_date.year}-{split_date.month:02d}-{split_date.day:02d}")
    df_true_max = pd.DataFrame(true_reservoir.T, index=dates).resample('Y').max()
    df_pred_max = pd.DataFrame(pred_reservoir.T, index=dates[split_idx:]).resample('Y').max()
    true_yearly_max = df_true_max.max(axis=1)
    pred_yearly_max = df_pred_max.max(axis=1)
    return true_yearly_max, pred_yearly_max


def get_gev_fit(true_yearly_max, max_rp):
    c0, loc0, scale0 = gev.fit(true_yearly_max, method="MLE")
    GEV = gev(c0, loc=loc0, scale=scale0)
    rp = np.arange(2, max_rp+1)
    gev_true = GEV.ppf(1.0 - (1.0 / rp))
    return pd.DataFrame(gev_true, index=rp)


def display_return_period_plot(dates, split_date, year, waterbody, true_reservoir, pred_reservoir):
    st.markdown(
        """
        :red[Please adjust 'year' parameter at the sidebar to see the return period plot for that year.]
        """
    )

    # Get GEV fit
    max_rp = 1000
    true_yearly_max, pred_yearly_max = get_true_pred_max(dates, true_reservoir, pred_reservoir, split_date)
    df_gev_true = get_gev_fit(true_yearly_max, max_rp)

    # Get true and predicted annual max and return period
    true_max = true_yearly_max[true_yearly_max.index.year == year].values[0]
    pred_max = pred_yearly_max[pred_yearly_max.index.year == year].values[0]
    true_rp = df_gev_true[df_gev_true >= true_max].index[0]
    pred_rp = df_gev_true[df_gev_true >= pred_max].index[0]

    # Plot GEV fit
    fig = px.line(
        df_gev_true,
        x=np.arange(2, max_rp+1),
        y=df_gev_true.values[:, 0],
        log_x=True,
        log_y=False,
        title=f"{waterbody} Precipitation (mm) Return Period",
        line_shape='spline'
    )

    # Plot true and predicted annual maxima
    fig.add_trace(go.Scatter(
        x=[true_rp],
        y=[true_max],
        mode='markers',
        marker=dict(size=10, color='red'),
        name=f"<b>True</b><br>Mean: {true_max:.2f} mm<br>Return Period: {true_rp} yrs"
    ))

    fig.add_trace(go.Scatter(
        x=[pred_rp],
        y=[pred_max],
        mode='markers',
        marker=dict(size=10, color='green'),
        name=f"<b>Predicted</b><br>Mean: {pred_max:.2f} mm<br>Return Period: {pred_rp} yrs"
    ))

    # Update hover template
    fig.update_traces(hovertemplate="Return Period: <b>%{x}</b> yrs<br>Precipitation: <b>%{y:.2f}</b> mm")

    st.plotly_chart(fig, use_container_width=True)


def display_histogram_plot(true_reservoir, pred_reservoir, true_target, pred_target, waterbody, vmin, vmax, bin_size):
    true = np.nanmean(true_reservoir[:, true_target])
    pred = np.nanmean(pred_reservoir[:, pred_target])

    # Initialize histogram plot
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=true_reservoir.flatten(),
        name="Observed SPI",
        xbins=dict(start=vmin, end=vmax, size=bin_size),
        marker_color='#1f77b4',
        showlegend=False,
        hovertemplate="Value: %{x:.2f}<br>Count: %{y}<br><extra></extra>",
    ))

    # Add vertical lines for mean values
    fig.add_vline(x=true, line_width=2, line_color='Red', name='Observed')
    fig.add_vline(x=pred, line_width=2, line_color='Green', name='Predicted')

    # Add annotations for mean values
    fig.add_annotation(x=true, y=0, text=f"<b>Observed: {true:.2f}</b>", font=dict(color="red"), showarrow=False,
                       bgcolor="rgba(255, 255, 255, 1)", bordercolor="white", borderwidth=1, xref="x", yref="y", yshift=10)
    fig.add_annotation(x=pred, y=0, text=f"<b>Predicted: {pred:.2f}</b>", font=dict(color="green"), showarrow=False,
                       bgcolor="rgba(255, 255, 255, 1)", bordercolor="white", borderwidth=1, xref="x", yref="y", yshift=-10)

    # Update layout for aesthetics
    fig.update_layout(
        title=f"Histogram of SPI values for {waterbody} (1981 - 2020)",
        xaxis_title="SPI",
        yaxis_title="Frequency",
        autosize=True,
        margin=dict(l=0, r=0, t=30, b=0),
        bargap=0.03
    )

    st.plotly_chart(fig, use_container_width=True)


def display_time_series_plot(plot_type, x_dates, start_date, split_year, waterbody, true_reservoir, pred_reservoir):
    threshold = true_reservoir.shape[-1] - len(x_dates)

    # Get mean for each timestep
    hist = np.nanmean(true_reservoir[:, :threshold], axis=0)
    true = np.nanmean(true_reservoir[:, threshold:], axis=0)
    pred = np.nanmean(pred_reservoir, axis=0)

    # Replace NaN values with mean
    all_mean = np.nanmean(true_reservoir)
    obs_mean = np.nanmean(true)
    pred_mean = np.nanmean(pred)

    hist = np.where(np.isnan(hist), all_mean, hist)
    true = np.where(np.isnan(true), obs_mean, true)
    pred = np.where(np.isnan(pred), pred_mean, pred)

    # Plot time series
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_dates, y=true, mode='lines', name=f'WRF Simulated {plot_type}', line=dict(color='#1f77b4'), line_width=1.5))
    fig.add_trace(go.Scatter(x=x_dates, y=pred, mode='lines', name=f'Predicted {plot_type}', line=dict(color='orange'), line_width=1.5))
    fig.add_hline(y=pred_mean, line_width=1.5, line_dash="dash", line_color="green", name="Predicted Mean")

    show_historical_data = st.checkbox("Include historical (training) data")

    if show_historical_data:
        historical_x_values = pd.date_range(start=str(start_date), end=str(split_year), freq='M')
        fig.add_trace(go.Scatter(x=historical_x_values, y=hist, mode='lines', name='Historical SPI', line=dict(color='black'), line_width=1))
        fig.add_hline(y=all_mean, line_width=1.5, line_dash="dash", line_color="red", name="WRF Simulated Mean")
        plt_start = start_date
    else:
        fig.add_hline(y=obs_mean, line_width=1.5, line_dash="dash", line_color="red", name="WRF Simulated Mean")
        plt_start = split_year

    add_mean_annotation(fig, obs_mean, "<b>WRF Simulated Mean: {:.2f}</b>", "red")
    add_mean_annotation(fig, pred_mean, "<b>Predicted Mean: {:.2f}</b>", "green")

    fig.update_layout(
        title=f"{plot_type} values over time for {waterbody} ({plt_start} - 2020)",
        xaxis_title="Time",
        yaxis_title="SPI",
        legend_title="SPI Values",
        hovermode="x",
        autosize=True,
        margin=dict(l=0, r=0, t=30, b=0),
        width=None
    )

    st.plotly_chart(fig, use_container_width=True)


def display_analysis_section(plot_type, dates, start_date, split_date, year, split_year, waterbody, true_reservoir, pred_reservoir, true_target, pred_target):
    st.markdown("## Analysis")

    if plot_type == 'Precipitation':
        vmin, vmax, bin_size = 0, 100, 10
        analysis_options = ["Time Series", "Return Period"]
    elif plot_type == 'SPI':
        vmin, vmax, bin_size = -3, 3, 0.2
        analysis_options = ["Time Series", "Histogram"]

    selected_option = st.radio("Choose analysis option", analysis_options, horizontal=True)

    if selected_option == "Return Period" and plot_type == 'Precipitation':
        display_return_period_plot(dates, split_date, year, waterbody, true_reservoir, pred_reservoir)

    elif selected_option == "Histogram" and plot_type == 'SPI':
        display_histogram_plot(true_reservoir, pred_reservoir, true_target, pred_target, waterbody, vmin, vmax, bin_size)

    elif selected_option == "Time Series":
        x_dates = dates[dates >= str(split_year)]
        display_time_series_plot(plot_type, x_dates, start_date, split_year, waterbody, true_reservoir, pred_reservoir)
