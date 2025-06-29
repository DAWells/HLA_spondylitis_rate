"""Correlation"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

aa = pd.read_csv("data/processed/allele_freq_disease_rate.csv")

namask = aa['Rate10-4'].isna()
outliermask = aa.country == "Finland"

mask = ~namask & ~outliermask
# mask = [True] * aa.shape[0]

x = aa[mask].allele_freq.values
X = sm.add_constant(x)
y =  aa[mask]['Rate10-4'].values

aa[mask]['Rate10-4'].hist()
plt.show()

np.log(aa[mask]['Rate10-4']).hist()
plt.show()

# Fit Gamma GLM with identity link
model = sm.GLM(
    y,
    x,
    family=sm.families.Gamma(sm.families.links.identity())
).fit()
print(model.summary())
plt.scatter(x, y)
pred = model.get_prediction(x).summary_frame()
plt.plot(x, pred['mean'])
# plt.fill_between(x, pred.mean_ci_lower, pred.mean_ci_upper)
plt.plot(x, pred.mean_ci_lower, linestyle="--")
plt.plot(x, pred.mean_ci_upper, linestyle="--")
plt.show()



# Fit Gamma GLM with log link
model = sm.GLM(
    y,
    x,
    family=sm.families.Gamma(sm.families.links.log())
).fit()
print(model.summary())
plt.scatter(x, y)
pred = model.get_prediction(x).summary_frame()
plt.scatter(x, pred['mean'])
# plt.errorbar(x, y, yerr=pred[['mean_ci_lower','mean_ci_upper']].T.values)
# plt.fill_between(x, pred.mean_ci_lower, pred.mean_ci_upper)
# plt.plot(x, pred.mean_ci_lower, linestyle="--")
# plt.plot(x, pred.mean_ci_upper, linestyle="--")
plt.scatter(x, pred.mean_ci_lower)
plt.scatter(x, pred.mean_ci_upper)
plt.show()

# Poisson model with offset to account for rate
exposure = [10000] * len(x)
offset = np.log(exposure)
model = sm.GLM(
    y,
    x,
    family=sm.families.Poisson(),
    offset=offset
).fit()
print(model.summary())
plt.scatter(x, y)
pred = model.get_prediction(x).summary_frame()
plt.scatter(x, pred['mean'])
# plt.errorbar(x, y, yerr=pred[['mean_ci_lower','mean_ci_upper']].T.values)
# plt.fill_between(x, pred.mean_ci_lower, pred.mean_ci_upper)
# plt.plot(x, pred.mean_ci_lower, linestyle="--")
# plt.plot(x, pred.mean_ci_upper, linestyle="--")
plt.scatter(x, pred.mean_ci_lower)
plt.scatter(x, pred.mean_ci_upper)
plt.show()

trials = [10000] * len(x)
model = sm.GLM(
    y,
    X,
    family=sm.families.Binomial(),
    freq_weights=trials
).fit()
print(model.summary())
plt.scatter(x, y)
pred = model.get_prediction(X).summary_frame()
plt.scatter(x, pred['mean'])
# plt.errorbar(x, y, yerr=pred[['mean_ci_lower','mean_ci_upper']].T.values)
# plt.fill_between(x, pred.mean_ci_lower, pred.mean_ci_upper)
# plt.plot(x, pred.mean_ci_lower, linestyle="--")
# plt.plot(x, pred.mean_ci_upper, linestyle="--")
plt.scatter(x, pred.mean_ci_lower)
plt.scatter(x, pred.mean_ci_upper)
plt.show()



# successes: number of cases
# trials: number of people
# X: predictors

model = sm.GLM(successes, X, family=sm.families.Binomial(), freq_weights=trials).fit()

model = sm.OLS(
    np.log(y),
    X
).fit()
print(model.summary())
plt.scatter(x, np.log(y))
pred = model.get_prediction(X).summary_frame()
plt.scatter(x, np.exp(pred['mean']))
# plt.errorbar(x, y, yerr=pred[['mean_ci_lower','mean_ci_upper']].T.values)
# plt.fill_between(x, pred.mean_ci_lower, pred.mean_ci_upper)
# plt.plot(x, pred.mean_ci_lower, linestyle="--")
# plt.plot(x, pred.mean_ci_upper, linestyle="--")
plt.scatter(x, pred.mean_ci_lower)
plt.scatter(x, pred.mean_ci_upper)
plt.show()



gmod0 = sm.GLM(
    aa[mask]['Rate10-4'],
    aa[mask].allele_freq,
    family=sm.families.Gamma()
).fit()
print(gmod0.summary())

gmod1 = sm.GLM(
    aa[mask]['Rate10-4'],
    sm.add_constant(aa[mask].allele_freq),
    family=sm.families.Gamma()
).fit()
print(gmod1.summary())

mod0 = sm.OLS(
    aa[mask]['Rate10-4'],
    aa[mask].allele_freq
).fit()
print(mod0.summary())

fig,ax = plt.subplots()
sm.graphics.plot_fit(mod0, 0, ax=ax)  # 1 is the index of the predictor
fig= sm.graphics.abline_plot(
    0,
    mod0.params,
    ax=ax
)
ax.margins(.1)
plt.show()


mod1 = sm.OLS(
    aa[mask]['Rate10-4'],
    sm.add_constant(aa[mask].allele_freq)
).fit()
print(mod1.summary())

fig,ax = plt.subplots()
sm.graphics.plot_fit(mod1, 1, ax=ax)  # 1 is the index of the predictor
sm.graphics.abline_plot(model_results=mod1, ax=ax)
ax.margins(.1)
plt.show()

model = mod1
fig,ax = plt.subplots()
ax.scatter(
    aa[mask].allele_freq,
    aa[mask]['Rate10-4']
)
pred = model.predict(
    sm.add_constant(aa[namask].allele_freq)
)
ax.scatter(
    aa[namask].allele_freq,
    pred
)
sm.graphics.abline_plot(model_results=model, ax=ax)
ax.margins(.1)
plt.show()


aa.loc[namask,'pred'] = model.predict(
    sm.add_constant(
        aa[namask]["allele_freq"]
    )
)

weights = 1 / aa[mask]['Rate10-4']**2  # inverse of variance
model = sm.WLS(
    aa[mask]['Rate10-4'],
    sm.add_constant(aa[mask].allele_freq),
    weights=weights
).fit()
sm.graphics.plot_fit(model, 1)
print(model.summary())
plt.show()