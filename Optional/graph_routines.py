import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import json

def bar_price_graph(
    dataframe: pd.DataFrame,
    title: str,
    y_label: str,
    x: list = [],
    y: dict = {},
    size: tuple = None):
    """ draw a bar plot with multiple series

    Args:
        dataframe (pd.DataFrame): data
        title (str): title of the graph
        y_label (str): label of the Y axis
        x (list, optional): X values. Defaults to [].
        y (dict, optional): Y values. Defaults to {}.
        size (tuple, optional): graph size in inches. Defaults to None.
    """
    columns = len(x)
    lines = len(y)
    show_labels = columns < 15

    x_coords = list(range(columns))
    width = 1 / (len(y) + 1)

    fig, ax = plt.subplots(layout='constrained')
    if size != None:
        fig.set_size_inches(size)

    for attr, measurement in y.items():
        rects = ax.bar(x_coords, measurement, width, label = attr)
        if show_labels:
            ax.bar_label(rects, padding = 3)

        for idx, val in enumerate(x_coords):
            x_coords[idx] = val + width

    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks([ width + val for val in range(len(x))], x)
    ax.legend(loc='upper right', ncols = lines)
    ax.set_ylim(0, 9)
    ax.tick_params(axis='x', labelrotation=45)

    plt.show()

def line_price_graph(
    dataframe: pd.DataFrame,
    title: str,
    y_label: str,
    x: list,
    y: dict,
    x_label: str = '',
    size: tuple = None):
    """ draw lines graph with multiple series

    Args:
        dataframe (pd.DataFrame): data
        title (str): title of teh graph
        y_label (str): label of the Y axis
        x (list, optional): X values. Defaults to [].
        y (dict, optional): Y values. Defaults to {}.
        x_label (str, optional): X axis label. Defaults to ''.
        size (tuple, optional): graph size in inches. Defaults to None.
    """
    show_labels = len(x) < 15

    fig, ax = plt.subplots(layout='constrained')
    if size != None:
        fig.set_size_inches(size)

    for lbl, values in y.items():
        ax.plot(x, values, label=lbl)

    ax.set_title(title)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if not show_labels:
        ax.tick_params(axis="x", labelbottom=False)

    ax.legend()
    plt.show()

def geo_price_graph(
    dataframe: pd.DataFrame,
    geodata: json,
    title : str,
    y_label : str,
    y: str,
    x: str,
    x_label: str = '',
    size: tuple = (7,6)):
    """ draw geo hot map graph

    Args:
        dataframe (pd.DataFrame): data
        title (str): title of the graph
        y_label (str): label of the Y axis
        x (str, optional): X values column name
        y (str, optional): Y values column name
        x_label (str, optional): X axis label. Defaults to ''.
        size (tuple, optional): graph size in inches. Defaults to None.
    """
    fig = px.choropleth_map(
        data_frame = dataframe,
        geojson = geodata,
        locations = 'zipcode',
        color = y,
        range_color = (dataframe[y].min(), dataframe[y].max()),
        featureidkey="properties.ZCTA5CE10",
        labels={ y : y_label },
        title=title,
        width = size[0] * 96,
        height = size[1] * 96,
        center = { 'lat': 47.35, 'lon': -122 }
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={
            'r' : 0,
            't' : 40,
            'l' : 10,
            'b' : 20,
            'pad': 4,
            'autoexpand': True
        })
    fig.show()
