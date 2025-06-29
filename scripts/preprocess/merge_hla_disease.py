import pandas as pd
import matplotlib.pyplot as plt

allele = pd.read_csv("data/interim/B27.csv")
ankyspon = pd.read_csv("data/raw/Dean2014_population.csv")


ankyspon.country[~ankyspon.country.isin(allele.country)].unique()

aa = pd.merge(
    allele,
    ankyspon,
    on="country",
    how="left"
)

aa.to_csv("data/processed/allele_freq_disease_rate.csv", index=False)

