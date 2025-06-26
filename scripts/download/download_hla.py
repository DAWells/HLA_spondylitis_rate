"""Download HLAfrequency data"""

import os
import HLAfreq
from HLAfreq import HLAfreq_pymc as HLAhdi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

# Download countries in regions as defined on 
# http://www.allelefrequencies.net/datasets.asp#tag_4
r = requests.get("https://raw.githubusercontent.com/BarinthusBio/HLAfreq/main/data/example/countries.csv")
with open("data/raw/countries.csv", "w") as f:
    f.write(r.text)

regions = pd.read_csv("data/raw/countries.csv")

countries = regions.Country.tolist()

############
# Download data
############
# Download HLA allele frequencies
# Not all countries have data
# those without will print "Failed to get data for..."
for country in countries:
    print()
    print(country)
    if not os.path.exists("data/external/DQB1/%s_raw.csv" %country):
        base_url = HLAfreq.makeURL(country, standard="g", locus="DQB1")
        try:
            aftab = HLAfreq.getAFdata(base_url)
            aftab.to_csv("data/external/DQB1/%s_raw.csv" %country, index=False)
        except:
            pass
