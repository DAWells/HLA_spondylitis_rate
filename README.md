# Undiagnosed ankylosing spondyloarthritis

The HLA immune genes are so important for triggering the immune system, that we can use these genes to predict a person’s immune response. Here I will demonstrate how to estimate disease rates just from immune gene frequencies. All the steps from getting the immune gene data, to identifying high risk countries, and assessing limitations of the model are discussed [here](https://towardsdatascience.com/estimating-disease-rates-without-diagnosis/).

# Download
## Download HLA
Download HLA frequency data for all available countries.

# Preprocess
## Combine HLA
Combine multistudy data for each single country using `HLAfreq`.

## Merge HLA disease
Pair HLA frequency estimates with disease rates.

# Analysis
## Correlation.R
Model correlation between HLA frequency and disease rate.

## Choropleth
Plot disease rates as a coloured map.

# Papers
- Dean, L. E., Jones, G. T., MacDonald, A. G., Downham, C., Sturrock, R. D., & Macfarlane, G. J. (2014). Global prevalence of ankylosing spondylitis. Rheumatology, 53(4), 650-657.
- Khan, M. A., & Ball, E. J. (2002). Genetic aspects of ankylosing spondylitis. Best practice & research Clinical rheumatology, 16(4), 675-690.
