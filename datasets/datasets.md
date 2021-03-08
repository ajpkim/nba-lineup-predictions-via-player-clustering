# Datasets
** Some datasets were renamed and notebooks may contain references to old dataset names **

### Base datasets
- raw_1997_to_2020_stats
  - The raw scrapped statistics combined into single dataset
- player_bio
  - player height, weight, salary, nationality
- combined_raw_stats_and_player_bio
  - Raw statistics and play bio data combined into single dataset

### Preprocessing
- clean_1997_to_2020_aggregate_pbp
  - clean dataset with play by play aggregated stats
- clean_1997_to_2020_rate_pbp
  - clean dataset with play by play stats converted to per/min rate states
- removed_highly_correlated_1997_to_2020
  - data with some highly correlated columns removed (95%+) (not v necessary dataset)
- clipped3s_logged_1997_2020
  - slim with low volumne 3pt shooting outliers clipped to mean based on attempts peers and 22 cols log transformed
- preprocessed_1997_2020
  - clipped3s_logged with several more columns removed e.g. 'nationality' and scaled with StandardScaler
- preprocessed_2000_to_2020
  - same as scaled 1997-2020 with less years

<!-- ### Pre PCA
- datasets that were used to generate the PCA datasets below
- pre_pca_2000_to_2020
  - scaled_2000_to_2020 with more columns dropped e.g. "age"
- pre_pca_2000_to_2020_slim 
  - dropped fg % by locations (keeping aggrgate fg% on 2s) and some pbp stats e.g. shooting fouls per min (already have pf_per_poss)
- pre_pca_quality_weighted_2000_to_2020
  - dataset without BPM stats or plus_minus stats (but still has per and defrtg)  so that I can do BPM weighted clusters for quality dimension
 -->
 
### PCA
- pre_pca_2000_to_2020
  - dropped fg % by locations (keeping aggrgate fg% on 2s) and some pbp stats e.g. shooting fouls per min (already have pf_per_poss)
- pca_99var_2000_to_2020
  - pca transformed with capturing 99% variance in pre_pca_2000_to_2020

### Clustering
- gmm_12cluster_labels
  - hard label and cluster probabilities for 12 clusters from the pca data
- stats_with_cluster_labels_2000_to_2020
  - gmm cluster probs and hard label merged with preprocessed_2000_to_2020 for complete dataset

### Lineups
- master datasets are combined stats and cluster labels and cleaned (e.g. minutes threshold and verified all players in player dataset)
- processing datasets are stepping stones to master datasets
- master_4_man_lineups_bpm_clusters_1997_2020
  - summed player cluster profiles merged with lineup stats for bpm and non-bpm weighted clusters
- master_5_man_lineups_bpm_clusters_1997_2020
  - summed player cluster profiles merged with lineup stats for bpm and non-bpm weighted clusters

### Master Dataset
- master_players_stats_bio_bpm_clusters
  - the combined clean data and cluster info with cluster probabilities (incl. bpm-weighted cluster labels)