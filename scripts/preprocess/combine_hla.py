"""Combine within country HLA frequences"""

import HLAfreq
from HLAfreq import HLAfreq_pymc as HLAhdi
import pandas as pd
from matplotlib import pyplot as plt

locus = "B"
regions = pd.read_csv("data/raw/countries.csv")

countries = regions.Country.tolist()

cafs = []
aftabs = []

for country in countries:
    try:
        aftab = pd.read_csv(f"data/external/{locus}/%s_raw.csv" %country)
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
aftabs.to_csv(f"data/interim/{locus}_aftab.csv", index=False)

# Save cafs
cafs = pd.concat(cafs)
# Give record for all alleles to all countries
cafs = HLAfreq.unmeasured_alleles(cafs, 'country')
cafs.to_csv(f"data/interim/{locus}.csv", index=False)

# Save just B*27
b27 = cafs[cafs.allele == "B*27"]
b27.to_csv(f"data/interim/B27.csv", index=False)
