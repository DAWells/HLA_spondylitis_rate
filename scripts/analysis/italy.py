"""Plot India allele frequency"""

import HLAfreq
from HLAfreq import HLAfreq_pymc as HLAhdi
import pandas as pd
from matplotlib import pyplot as plt

locus = "B"

country = "Italy"

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
aftab['country'] = country

HLAfreq.plotAF(caf, aftab, hdi=hdi, compound_mean=hdi)
HLAfreq.plotAF(caf, aftab)
