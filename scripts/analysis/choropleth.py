"""Choropleth"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import geopandas as gpd

# aa = pd.read_csv("data/processed/allele_freq_disease_rate.csv")
known_pred_rates = pd.read_csv("data/processed/known_pred_rates.csv")

# Remove 2 countries with higher allele frequencies than Finland (an outlier)
known_pred_rates = known_pred_rates[known_pred_rates['allele_freq'] < 0.08]

url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file(url)

# Ankylosing Allele World data
aaw = world.merge(
    known_pred_rates,
    how="left",
    right_on="country",
    left_on="NAME_LONG"
)


norm = colors.Normalize(
    np.min(
        [np.log(aaw['Rate10.4']).min(),
        aaw['predrate'].min()]
    ),
    np.max(
        [np.log(aaw['Rate10.4']).max(),
        aaw['predrate'].max()]
    )
)

cmap="cividis"
fig,ax = plt.subplots()
aaw[aaw['type'].isna()].plot(
    color="lightgrey",
    ax=ax
)
aaw[aaw['type']=="known"].plot(
    norm(np.log(aaw[aaw['type']=="known"]["Rate10.4"])),
    cmap=cmap,
    edgecolor="black",
    # linewidth=2,
    ax=ax
)
aaw[aaw['type']=="predin"].plot(
    norm(aaw[aaw['type']=="predin"]["predrate"]),
    cmap=cmap,
    edgecolor="darkcyan",
    # linewidth=2,
    ax=ax
)
aaw[aaw['type']=="predout"].plot(
    norm(aaw[aaw['type']=="predout"]["predrate"]),
    cmap=cmap,
    edgecolor="orange",
    # linewidth=2,
    ax=ax
)
sm = cm.ScalarMappable(norm=norm, cmap=cm.cividis)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04, shrink=0.5)
# cbar.set_label('Log Rate per 10,000\n', rotation=270)
ax.axis('off')
plt.title("Log Rate per 10,000")
plt.tight_layout()
plt.show()


fig,ax = plt.subplots()
aaw[aaw['type'].isna()].plot(
    color="lightgrey",
    ax=ax
)
aaw[aaw['type']=="known"].plot(
    alpha=norm(np.log(aaw[aaw['type']=="known"]["Rate10.4"])),
    color="black",
    linewidth=2,
    ax=ax
)
aaw[aaw['type']=="predin"].plot(
    alpha=norm(aaw[aaw['type']=="predin"]["predrate"]),
    color="darkgreen",
    linewidth=2,
    ax=ax
)
aaw[aaw['type']=="predout"].plot(
    alpha=norm(aaw[aaw['type']=="predout"]["predrate"]),
    color="orange",
    linewidth=2,
    ax=ax
)
plt.show()
