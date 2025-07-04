""" Make figures """
import HLAfreq
from HLAfreq import HLAfreq_pymc as HLAhdi
import pandas as pd
from matplotlib import pyplot as plt

aftabs = pd.read_csv("data/interim/B_aftab.csv")
b27 = pd.read_csv("data/interim/B27.csv")

fig,ax = plt.subplots()
ax.scatter(
    aftabs[aftabs.allele == "B*27"].allele_freq,
    aftabs[aftabs.allele == "B*27"].country,
    alpha=0.3
)
ax.scatter(
    b27.allele_freq,
    b27.country,
)
plt.show()

fig,ax = plt.subplots()
ax.scatter(
    aftabs[aftabs.allele == "B*27"].allele_freq,
    aftabs[aftabs.allele == "B*27"].country,
    alpha=0.3
)
ax.scatter(
    b27.post_mean,
    # b27.allele_freq,
    b27.country,
)
for i,row in b27.iterrows():
    # .iterrows returns a index and data as a tuple for each row
    plt.hlines(
        y=row["country"],
        xmin=row["lo"],
        xmax=row["hi"],
        color="black",
    )
plt.show()