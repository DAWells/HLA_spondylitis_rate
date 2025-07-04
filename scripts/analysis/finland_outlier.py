"""Finland?"""

import HLAfreq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

locus = "B"
regions = pd.read_csv("data/raw/countries.csv")

countries = regions.Country.tolist()

cafs = []
aftabs = []

for country in countries:
    try:
        aftab = pd.read_csv(f"data/external/{locus}/%s_raw.csv" %country)
        aftab = HLAfreq.only_complete(aftab)
        aftab = HLAfreq.decrease_resolution(aftab, 2)
        caf = HLAfreq.combineAF(aftab)
        caf['country'] = country
        cafs.append(caf)
        aftab['country'] = country
        aftabs.append(aftab)
    except:
        pass

aftabs = pd.concat(aftabs)
cafs = pd.concat(cafs)
cafs = HLAfreq.unmeasured_alleles(cafs, 'country')

b27mask = cafs.allele.str.contains("B*27", regex=False)
gt0mask = cafs.allele_freq > 0
mask = b27mask & gt0mask

df = cafs[mask][['allele','allele_freq','country']]
pivot_df = df.pivot(
    index='country',
    columns='allele',
    values='allele_freq'
).fillna(0)

pivot_df.plot(kind='barh', stacked=True)
plt.xlabel('Allele freq')
plt.ylabel('Country')
plt.legend(title='Allele')
plt.tight_layout()
plt.show()
