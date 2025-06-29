"""Choropleth"""
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

aa = pd.read_csv("data/processed/allele_freq_disease_rate.csv")

url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file(url)
world.plot()
plt.show()

aaw = world.merge(
    aa,
    how="left",
    right_on="country",
    left_on="NAME_LONG"
)

fig,ax = plt.subplots()
aaw.plot(
    "allele_freq",
    edgecolor="black",
    missing_kwds={
        "color": "lightgrey",
        "label": "Missing values",
    },
    legend=True,
    legend_kwds={"orientation": "horizontal"}
    # ax=ax
)
plt.show()

fig,ax = plt.subplots()
aaw.plot(
    "Rate10-4",
    edgecolor="black",
    missing_kwds={
        "color": "lightgrey",
        "label": "Missing values",
    },
    legend=True,
    legend_kwds={"orientation": "horizontal"}
    # ax=ax
)
plt.show()

fig,ax = plt.subplots()
aaw.plot(
    "pred",
    edgecolor="black",
    missing_kwds={
        "color": "lightgrey",
        "label": "Missing values",
    },
    legend=True,
    legend_kwds={"orientation": "horizontal"}
    # ax=ax
)
plt.show()

fig,ax = plt.subplots()
aaw[~aaw['Rate10-4'].isna()].plot(
    "Rate10-4",
    ax=ax
)
aaw[~aaw['pred'].isna()].plot(
    "pred",
    edgecolor="red",
    ax=ax
)
aaw[(aaw['Rate10-4'].isna()) & aaw['pred'].isna()].plot(
    color="lightgrey",
    ax=ax
)
plt.show()