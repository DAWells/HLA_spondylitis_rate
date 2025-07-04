"""Download HLAfrequency data"""

import os
import HLAfreq
from HLAfreq import HLAfreq_pymc as HLAhdi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

locus = "B"

# Download countries in regions as defined on 
# http://www.allelefrequencies.net/datasets.asp#tag_4
r = requests.get("https://raw.githubusercontent.com/BarinthusBio/HLAfreq/main/data/example/countries.csv")
with open("data/raw/countries.csv", "w") as f:
    f.write(r.text)

regions = pd.read_csv("data/raw/countries.csv")

countries = regions.Country.tolist()

os.system(f"mkdir -p data/external/{locus}")

############
# Download data
############
# Download HLA allele frequencies
# Not all countries have data
# those without will print "Failed to get data for..."
for country in countries:
    print()
    print(country)
    if not os.path.exists(f"data/external/{locus}/{country}_raw.csv"):
        base_url = HLAfreq.makeURL(country, standard="g", locus=f"{locus}")
        try:
            aftab = HLAfreq.getAFdata(base_url)
            aftab.to_csv(f"data/external/{locus}/{country}_raw.csv", index=False)
        except:
            pass
