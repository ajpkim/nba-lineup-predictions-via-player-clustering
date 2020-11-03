# Datasets

### Base datasets
- combo is the raw 4 stat tables combined 
- player_bio is height, weight, salary, nationality
- `master_nba_data` is raw combo 97-20 merged with player_bio
- clean is all missing values handled and datatypes for height and position percents corrected to floats

### Transformed datasets
- clean_rates_1997_2020 is clean dataset with play by play aggregated stats converted to per minute rates
- slim is data with some highly correlated columns removed (95%+) (not v necessary dataset)
- clipped3s_logged is slim with low volumne 3pt shooting outliers clipped to mean based on attempts peers and 22 cols log transformed
- scaled 1997-2020 is clipped3s_logged with several more columns removed e.g. 'nationality' and scaled with StandardScaler
- scaled_2000_to_2020 is same as scaled 1997-2020 with less years

### PCA
- pre_pca_2000_to_2020 is scaled_2000_to_2020 with more columns dropped e.g. "age"
- pre_pca_2000_to_2020_slim dropped fg % by locations (keeping aggrgate fg% on 2s) and some pbp stats e.g. shooting fouls per min (already have pf_per_poss)
- pca99_2000_to_2020 is pca transformed with capturing 99% variance in pre_pca_2000_to_2020
  - same is true for 'slim' version
- pre_pca_quality_weighted_2000_to_2020 is dataset without BPM stats or plus_minus stats (but still has per and defrtg)  so that I can do BPM weighted clusters for quality dimension
- pca99_quality_weighted_2000_to_2020 is pca done with the same pre pca quality weighted dataset (not using)


### Clustering 
- gmm_cluster12_slim is the hard label and cluster probabilities for 12 clusters on the pca data done with "slim" version
- clusters12_all_clean_data is the gmm cluster probs and hard label merged with clean_rates df for complete dataset for analysis that was made with the pre_pca_2000_to_2020_slim dataset
- bpm_clusters12 is the combined clean data and cluster info with columns that are the cluster probabilities weighted by bpm 
