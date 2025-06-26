"""Combine within country HLA frequences"""

import HLAfreq
from HLAfreq import HLAfreq_pymc as HLAhdi
import pandas as pd
from matplotlib import pyplot as plt

regions = pd.read_csv("data/raw/countries.csv")

countries = regions.Country.tolist()

cafs = []
aftabs = []

for country in countries:
    try:
        aftab = pd.read_csv("data/external/DQB1/%s_raw.csv" %country)
        aftab = HLAfreq.only_complete(aftab)
        aftab = HLAfreq.decrease_resolution(aftab, 1)
        caf = HLAfreq.combineAF(aftab)
        # Calculate High Density interval
        # This takes a few seconds and can be skipped if not needed
        hdi = HLAhdi.AFhdi(aftab, credible_interval=0.95)
        # Add credible intervals and posterior mean to caf
        caf = pd.merge(caf, hdi, how="left", on="allele")
        caf['country'] = country
        cafs.append(caf)
        aftab['country'] = country
        aftabs.append(aftab)
    except:
        pass

aftabs = pd.concat(aftabs)
aftabs.to_csv("data/interim/DQB1_aftab.csv", index=False)

# Save cafs
cafs = pd.concat(cafs)
cafs.to_csv("data/interim/DQB1.csv", index=False)

# Save just DQB1*02
dqb102 = cafs[cafs.allele == "DQB1*02"]


# Plot DQB1*02 frequencies with error bars?
fig,ax = plt.subplots()
ax.scatter(
    aftabs[aftabs.allele == "DQB1*02"].allele_freq,
    aftabs[aftabs.allele == "DQB1*02"].country,
    alpha=0.3
)
ax.scatter(
    dqb102.post_mean,
    dqb102.country,
)
for i,row in dqb102.iterrows():
    # .iterrows returns a index and data as a tuple for each row
    plt.hlines(
        y=row["country"],
        xmin=row["lo"],
        xmax=row["hi"],
        color="black",
    )
plt.show()

# Plot DQB1*02 frequencies as choropleth
