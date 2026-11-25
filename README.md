# bhflow

Joint reconstruction of the massive black hole mass function (BHMF) by combining
gravitational-wave (GW) and electromagnetic (EM) observations.

## Idea
- **GW side:** LISA massive black hole binaries (and EMRIs) constrain the merging/binary population.
- **EM side:** AGN/quasar luminosity functions (including JWST high-z AGN) and local BHMF estimates
  constrain the population of single black holes.
- **Joint fit:** a common population model with shared hyperparameters (seeding, occupation fraction,
  BH–halo relation, accretion) fitted to both datasets, each with its own selection function,
  to infer one BHMF for binaries + singles.

## Key references
- Bonoli et al., *Constraints on the early growth of massive black holes from PTA and JWST with L-Galaxies BH* — [arXiv:2509.12325](https://arxiv.org/abs/2509.12325)
- *Gravitational Wave Forecasts Constrained by JWST AGN Observations for Early Massive Black Hole Mergers* — [arXiv:2409.18194](https://arxiv.org/abs/2409.18194)
- Cáceres-Burgos et al., *Black Hole merger rates in the first billion years in light of JWST data* — [arXiv:2511.20414](https://arxiv.org/abs/2511.20414)
- Lapi et al. 2026 (JCAP), *Semi-empirical framework of supermassive black hole evolution: highlighting a possible tension between demographics and gravitational wave background* — [arXiv:2507.15436](https://arxiv.org/abs/2507.15436)
  Closest prior work: continuity + Smoluchowski equation, MCMC fit to EM data + PTA amplitude (z ≲ 7). No explicit seeds, no LISA. Base framework for bhflow.
- Roberts et al. 2026, *Too many or too massive? Investigating the high-z demography of active SMBHs from JWST* — [arXiv:2601.23250](https://arxiv.org/abs/2601.23250)
  Continuity-equation view of JWST AGN at z ≳ 5 (EM only). Useful for high-z M_BH–M★ relation and EM-side inputs.

## Status
Work in progress.
