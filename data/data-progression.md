data 1: original data pipeline
data 2: changed starting stats. added value and holsitics measures: +/-, offrtg, defrtg, pie. Removed redundant % stats e.g. drop '2fgm %ast' and keep '2fgm %uast'.
  - data2_tr: log transformed some cols, clipped 3pt shooting outliers, standardized with standardscaler
  - pca2
  - re-dropped +/-
data 3: re-dropped OFFRTG, DEFRTG

data 4 stats: