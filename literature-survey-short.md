# Literature survey — short version (bhflow)

Three recent papers tackle the question bhflow is about, each from a different side. How did the first massive black holes form and grow? What does that mean for how many black holes there are of each mass (the black-hole mass function, **BHMF**)? And what does it mean for gravitational-wave (GW) signals? Below, each paper is explained in plain terms: what they did, what they found, how they used the data, and what helps or hurts our idea.

**A few terms used below**
- **Seeds**: the first black holes. *Light seeds* are ~100 M☉ (leftovers of the first stars). *Heavy seeds* are 10³–10⁵ M☉ (from gas clouds collapsing directly).
- **Eddington limit**: the usual maximum rate at which a black hole can swallow gas. *Super-Eddington* means faster than that, usually only in short bursts.
- **JWST AGN / LRDs**: actively feeding black holes that JWST found at z ≈ 4–11. *LRDs* ("little red dots") are compact red sources; many are thought to be AGN, but this is still debated.
- **Luminosity function (LF)**: how many AGN there are per unit volume at each brightness.
- **PTA**: pulsar timing arrays (e.g. NANOGrav). They pick up the combined "hum" of very heavy black-hole pairs (≳ 10⁸ M☉) at low redshift.
- **LISA, B-DECIGO, LGWA**: future GW detectors that can hear mergers of ~10³–10⁷ M☉ black holes out to very high redshift.

---

## 1. Bonoli et al. 2025 — PTA + JWST
*Constraints on the early growth of massive black holes from PTA and JWST with L-GalaxiesBH* — [arXiv:2509.12325](https://arxiv.org/abs/2509.12325)

**What they did**
They used a large galaxy-formation model (L-Galaxies, built on the Millennium dark-matter simulations). It follows how galaxies and their central black holes form, feed and merge over cosmic time. They ran four versions of the early black-hole story:
1. **SuperEdd**: light seeds that are allowed short bursts of super-Eddington growth.
2. **EddLim**: light seeds that never grow faster than the Eddington limit.
3. **HeavyMax**: Eddington-limited growth plus many heavy seeds.
4. **HeavyMin**: Eddington-limited growth plus few heavy seeds.

They then checked each version against two very different observations:
- **JWST**: how many feeding black holes there are at z ≈ 4–10, and how heavy they are;
- **PTA**: how loud the low-frequency GW background is.

**What they found**
- **EddLim fails JWST**: it makes too few black holes early on. To match JWST you need either lots of heavy seeds (≳ 0.01 per Mpc³ at z ~ 10) or light seeds that sometimes grow faster than Eddington.
- **HeavyMin fails PTA**: the GW background comes out too quiet. To match PTA, almost every galaxy with more than 10⁹ M☉ in stars must host a black hole today.
- **SuperEdd and HeavyMax survive.** The authors prefer SuperEdd, because HeavyMax needs an unrealistically large number of heavy seeds.
- The two survivors predict merger rates that differ by up to a few hundred times at z ~ 4 for 10⁷–10⁸ M☉ black holes. The authors note that **LISA could tell them apart**, especially combined with EM data.
- They also estimate how many PTA-band binaries would show up as bright AGN: about 20–30% at z ~ 2, and under 5% at z ~ 0.25.

**How they used the data**
- There is no statistical fit. Models are judged by comparing curves with data by eye.
- A black hole counts as "active" if it feeds at more than 1% of the Eddington rate or is brighter than 10⁴⁴ erg/s.
- They do not model what JWST can and cannot detect (no selection function).
- They treat all LRDs as AGN.

**Good for us**
- It is truly multi-messenger: JWST (single, feeding black holes at high z) and PTA (binaries at low z) rule out *different* versions of the same model. That is exactly the logic of bhflow.
- It points directly to LISA + EM as the way to separate the surviving scenarios.

**Limits**
- Only four fixed scenarios are compared, and no joint likelihood is built.
- The paper makes no actual LISA predictions.
- The JWST data at z ≳ 7 rest on very few objects.
- The model overshoots the number of very massive (> 10⁹ M☉) black holes today, and that excess helps it match PTA.

---

## 2. Liu & Inayoshi 2025 — JWST → LISA / B-DECIGO forecast
*Gravitational Wave Forecasts Constrained by JWST AGN Observations for Early Massive Black Hole Mergers* (PRD 111, 043012) — [arXiv:2409.18194](https://arxiv.org/abs/2409.18194)

**What they did**
They built a simpler, equation-based model (no full galaxy simulation) that tracks the BHMF from z = 20 down to z = 5. Black holes grow in two ways:
- **feeding in bursts**, with a random accretion rate in each burst;
- **merging with each other**.

The model starts from two seed populations:
- heavy seeds, with a fixed number density of 10⁻³ or 10⁻² per Mpc³;
- light seeds of ~260 M☉, with 1 or 10 per Mpc³.

The growth parameters are fitted with MCMC to the z ~ 5 AGN luminosity function. That combines ground-based quasars for the bright end with faint JWST AGN for the faint end. The fitted model then gives a merger rate, which they pass through the LISA and B-DECIGO sensitivity curves.

**What they found**
- **Heavy seeds alone cannot match both** the bright quasars and the faint JWST AGN, so light seeds are needed.
- With heavy seeds only, there are fewer than about 0.1 major mergers per year at z ≥ 5. That is far too few for GW detectors.
- In the main model (with light seeds):
  - about **32 mergers per year** happen at z ≥ 5 across the whole Universe, mostly involving ~2000 M☉ black holes at z ≈ 5–10;
  - LISA would detect about **12 major mergers per year**, and B-DECIGO about **20**;
  - if mergers are delayed after galaxies merge, LISA drops to about 9 per year.
- Ten times more light seeds pushes the rates to **thousands per year**. The GW rate is therefore very sensitive to how many light seeds there are.
- Matching a GW event at z ≥ 5 to its host galaxy will be hard: a typical LISA sky region contains many AGN.

**How they used the data**
- They used only one redshift (z ~ 5) and one type of measurement: the brightness distribution of unobscured AGN in the UV.
- The JWST points are photometric candidates and act essentially as upper limits.
- There is no selection function beyond what is already folded into the published luminosity functions. Very faint, incomplete data are simply dropped.
- Their results are public, and we have copied them into `codes/mass_range_check/external/`.

**Our quick check**
Combining their merger rates with our own LISA detection probability gives **9.3 detected major mergers per year**, against their 11.6. The two set-ups agree well.

**Good for us**
- This is the closest thing to bhflow so far: one model that runs from EM data to GW predictions.
- Most GW events come from small light-seed black holes that EM telescopes cannot see. GW and EM therefore look at **different parts of the same BHMF**, which is the main reason to fit them together.
- The rates are encouraging: tens per year, or more.

**Limits**
- It is one-way only: fit EM, then forecast GW. GW and EM data are not combined.
- The seed numbers are fixed by hand (a 2 × 2 grid), not fitted.
- There is only one redshift, one observable, and no LRDs or BH-mass data.
- The model stops at z = 5, so PTA cannot be included without extending it to z = 0.

---

## 3. Cáceres-Burgos et al. 2025 — heavy seeds calibrated on JWST
*Black Hole merger rates in the first billion years in light of JWST data* (A&A) — [arXiv:2511.20414](https://arxiv.org/abs/2511.20414)

**What they did**
They used the Delphi model, which follows dark-matter halos and the galaxies and black holes inside them through the first billion years (z ≥ 5). It uses **only heavy seeds** (10³–10⁵ M☉), placed in pristine gas halos down to z ≈ 13. They tested about 6200 parameter combinations and kept the one that best matched four data sets at once:
1. the galaxy UV luminosity function;
2. the galaxy stellar-mass function;
3. the JWST black-hole mass function at z ~ 5–6;
4. the JWST AGN luminosity function at z ~ 5–8.

They ran it under two merger assumptions: black holes merge as soon as their halos merge, or only after a delay while they sink to the centre.

**What they found**
- To match the JWST AGN numbers, black holes must swallow **10–100 times more gas** than the older (pre-JWST) version of the model allowed.
- Even then the match is only partial:
  - there are too few very bright AGN at z = 7 (by a factor of 10–1000);
  - there are too many AGN at z = 5.
- Merger rates at z ≥ 5 come out at about **28 per year** (merge immediately) or **20 per year** (with delay). That is similar to the Liu & Inayoshi total, **but the masses peak at ~10⁶ M☉ instead of ~2000 M☉**.
- Many of the mergers are very unequal. The typical mass ratio drops from about 1:3 at z ~ 16 to about 1:10 at z ~ 5.

**How they used the data**
- They used a simple χ² over a parameter grid, with no uncertainty estimates on the parameters.
- They do not model selection effects, and they treat LRDs as AGN.
- The rates are "raw": they are not passed through any detector sensitivity.

**Good for us**
- Two different models give a similar total number of mergers but a **very different mass distribution**. The GW mass spectrum can therefore tell seeding scenarios apart where EM luminosity functions cannot. This is a strong argument for the GW side of a joint fit.
- Fitting several data sets at once is already a step towards a joint likelihood.

**Limits**
- The model uses heavy seeds only, and reproduces JWST only partly.
- The rates are optimistic, because the small-scale physics of how black holes actually reach each other is not modelled.
- It covers the first billion years only, with no PTA and no detectability.

---

## Bottom line

| | Bonoli+25 | Liu & Inayoshi 25 | Cáceres-Burgos+25 |
|---|---|---|---|
| Model | full galaxy simulation | equation-based BHMF model | halo merger-tree model |
| Seeds | light and/or heavy (4 scenarios) | light + heavy | heavy only |
| EM data | JWST AGN counts, masses | z ~ 5 AGN UV luminosity function | JWST BHMF + LF, galaxy data |
| GW side | PTA amplitude | LISA, B-DECIGO rates | raw merger rates |
| Statistical fit? | no (by eye) | MCMC on EM only | grid χ² on EM only |
| GW + EM fitted jointly? | **no** | **no** | **no** |

- **Nobody has done the joint fit yet.** All three either compare by eye, or fit the EM data and then predict GW.
- **Nobody models JWST selection effects.**
- **The rates look promising**: tens of mergers per year at z ≥ 5, with LISA detecting roughly half of the major ones.
- **GW and EM see different masses.** EM sees black holes of ≳ 10⁶ M☉; LISA and deci-Hz detectors reach down to ~10³ M☉ seeds. The region where both overlap is **10⁶–10⁸ M☉ at z ≈ 4–10**, where most JWST AGN sit inside LISA's reach. PTA connects only through the model, at > 10⁸ M☉ and low redshift.

That gap, a single fit that uses GW and EM data together to recover the full BHMF, is what bhflow is meant to fill.
