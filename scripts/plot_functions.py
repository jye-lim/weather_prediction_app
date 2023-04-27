import streamlit as st
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from shapely.geometry import Point


def configure_plot(plot_type, dates, true_target, prcp_true, prcp_pred, spi_true, spi_pred):
    if plot_type == 'Precipitation':
        st.markdown("## Precipitation Comparison")
        data_true = prcp_true[..., 0]
        data_pred = prcp_pred[..., 0]
        plt_date = dates[true_target].strftime("%d %B %Y")

        cmap = 'Blues'
        cbar_label = 'Precipitation (mm)'
        rsvr_colour = 'magenta'
        vmin = 0
        vmax = 100

    elif plot_type == 'SPI':
        st.markdown("## SPI Comparison")
        data_true = spi_true
        data_pred = spi_pred
        plt_date = dates[true_target].strftime("%B %Y")

        cmap_options = ['RdBu', 'inferno_r', 'viridis_r']
        rsvr_options = ['magenta', 'lime', 'magenta']
        cmap_display = ['Red-Blue', 'Inferno', 'Viridis']
        cmap_dict = dict(zip(cmap_options, cmap_display))
        rsvr_dict = dict(zip(cmap_options, rsvr_options))

        cmap_col = st.columns(4)
        with cmap_col[0]:
            cmap = st.selectbox('Color map', cmap_options, format_func=lambda x: cmap_dict[x])

        cbar_label = 'SPI'
        rsvr_colour = rsvr_dict[cmap]
        vmin = -3
        vmax = 3

    return data_true, data_pred, plt_date, cmap, cbar_label, rsvr_colour, vmin, vmax


def add_colorbar(fig, ax, cmap, vmin, vmax, cbar_label):
    p0 = ax[0].get_position().get_points().flatten()
    p1 = ax[1].get_position().get_points().flatten()
    ax_cbar = fig.add_axes([p0[0], p0[1]-0.05, p1[2]-p0[0], 0.02])

    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm, plt.cm.get_cmap(cmap)), orientation="horizontal", cax=ax_cbar)
    cbar.ax.set_xlabel(cbar_label, fontsize=16, fontweight='bold', labelpad=-55)
    cbar.ax.tick_params(labelsize=14)


def set_ticks(ax, xlong_1, xlong_2, xlat_1, xlat_2):
    xticks = np.arange(np.ceil(xlong_1 * 10) / 10, np.floor(xlong_2 * 10) / 10 + 0.001, 0.1)
    yticks = np.arange(np.ceil(xlat_1 * 10) / 10, np.floor(xlat_2 * 10) / 10 + 0.001, 0.1)

    ax.set_xticks(xticks, minor=False)
    ax.set_yticks(yticks, minor=False)
    ax.set_xticklabels([f'{x:.1f}°E' for x in xticks])
    ax.set_yticklabels([f'{y:.2f}°N' for y in yticks])
    

def plot_subplot(world, ax, data, cmap, vmin, vmax, xlat, xlong, title, zoomed, target_reservoir, rsvr_colour):
    ax.imshow(
        data,
        cmap=cmap,
        vmin=vmin, vmax=vmax,
        extent=[np.min(xlong), np.max(xlong), np.min(xlat), np.max(xlat)],
        origin='upper'
    )

    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

    world.plot(ax=ax, edgecolor='black', linewidth=0.5)

    xlong_vals = sorted(xlong.flatten())
    xlat_vals = sorted(xlat.flatten())

    if zoomed:
        xlong_1, xlong_2 = xlong_vals[int(0.2 * len(xlong_vals))], xlong_vals[int(0.8 * len(xlong_vals))]
        xlat_1, xlat_2 = xlat_vals[int(0.15 * len(xlat_vals))], xlat_vals[int(0.75 * len(xlat_vals))]
    else:
        xlong_1, xlong_2 = xlong_vals[0], xlong_vals[-1]
        xlat_1, xlat_2 = xlat_vals[0], xlat_vals[-1]

    ax.set_xlim([xlong_1, xlong_2])
    ax.set_ylim([xlat_1, xlat_2])

    set_ticks(ax, xlong_1, xlong_2, xlat_1, xlat_2)
    ax.grid(True, linestyle='--', alpha=0.5, color='gray', which='both', zorder=0)

    target_reservoir.boundary.plot(ax=ax, facecolor=rsvr_colour, edgecolor=rsvr_colour, linewidth=1)


def get_reservoir_values(data, boundary, xlat_values, xlong_values):
    buffer_distance = 0.01
    buffered_boundary = boundary.buffer(buffer_distance)
    rsvr_c = None

    for i in range(data.shape[1]):
        for j in range(data.shape[2]):
            point = Point(xlong_values[i, j], xlat_values[i, j])

            if buffered_boundary.contains(point):
                if rsvr_c is None:
                    rsvr_c = np.array(data[:, i, j])
                else:
                    rsvr_c = np.vstack((rsvr_c, data[:, i, j]))

    return rsvr_c


def get_plots(world, rows, cols, xlat, xlong, plot_type, dates, true_target, pred_target, waterbody, step, spi_true, spi_pred_dict, prcp_true, prcp_pred_dict, reservoirs_gdf):
    fig, ax = plt.subplots(nrows=rows, ncols=cols, figsize=(cols * 8, rows * 7))
    fig.set_size_inches(cols * 8, rows * 7)

    data_true, data_pred, plt_date, cmap, cbar_label, rsvr_colour, vmin, vmax = configure_plot(plot_type, dates, true_target, prcp_true, prcp_pred_dict[step], 
                                                                                               spi_true, spi_pred_dict[step])

    add_colorbar(fig, ax, cmap, vmin, vmax, cbar_label)

    obs_mean = np.nanmean(data_true[true_target])
    pred_mean = np.nanmean(data_pred[pred_target])
    data_true[true_target] = np.where(np.isnan(data_true[true_target]), obs_mean, data_true[true_target])
    data_pred[pred_target] = np.where(np.isnan(data_pred[pred_target]), pred_mean, data_pred[pred_target])

    labels = ["WRF Simulation", "Predicted"]
    targets = [true_target, pred_target]
    zoomed = st.checkbox("Zoom", value=False)

    true_reservoir = None
    pred_reservoir = None
    target_reservoir = reservoirs_gdf[reservoirs_gdf["name"] == waterbody]

    for c in range(cols):
        plot_subplot(world, ax[c], data_true[targets[c]] if c == 0 else data_pred[targets[c]], cmap, vmin, vmax, xlat, xlong, labels[c], zoomed, target_reservoir, rsvr_colour)
        rsvr_c = get_reservoir_values(data_true if c == 0 else data_pred, target_reservoir.geometry.iloc[0], xlat, xlong)
        true_reservoir, pred_reservoir = (rsvr_c, pred_reservoir) if c == 0 else (true_reservoir, rsvr_c)

    fig.suptitle(plt_date, fontsize=20, fontweight='bold')
    st.pyplot(fig)

    return data_true[true_target], data_pred[pred_target], true_reservoir, pred_reservoir


def show_distribution(true, pred, plot_type):
    st.write('### Data Distribution')

    if plot_type == "Precipitation":
        categories = [
            "0 < x <= 20",
            "20 < x <= 40",
            "40 < x <= 60",
            "60 < x <= 80",
            "80 < x <= 100",
            "x > 100",
        ]
        bins = [0, 20, 40, 60, 80, 100, np.inf]

    elif plot_type == "SPI":
        categories = [
            "Extremely Wet (>= 2.00)",
            "Severely Wet (1.50 to 1.99)",
            "Moderately Wet (1.00 to 1.49)",
            "Near Normal (-0.99 to 0.99)",
            "Moderately Dry (-1.00 to -1.49)",
            "Severely Dry (-1.50 to -1.99)",
            "Extremely Dry (<= -2.00)",
        ]
        bins = [-np.inf, -2, -1.5, -1, 1, 1.5, 2, np.inf]

    true_counts, _ = np.histogram(true, bins=bins)
    pred_counts, _ = np.histogram(pred, bins=bins)

    true_perc = true_counts / true_counts.sum() * 100
    pred_perc = pred_counts / pred_counts.sum() * 100

    distribution_df = pd.DataFrame({"Category (mm)" if plot_type == "Precipitation" else "Category": categories, 
                                     "WRF Simulation": true_counts, 
                                     "WRF Simulation (%)": true_perc,
                                     "Predicted": pred_counts, 
                                     "Predicted (%)": pred_perc})

    st.write(f'Data distribution for {plot_type} plot')
    st.markdown(distribution_df.style.hide_index()
                      .format({"WRF Simulation (%)": "{:.2f}", "Predicted (%)": "{:.2f}"})
                      .set_table_styles([dict(selector="th", props=[("font-weight", "bold")])])
                      .render(), unsafe_allow_html=True)
    st.write("")
