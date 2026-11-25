# bhflow pilot study — plan

**Goal:** a cheap test of whether adding LISA to EM data improves constraints on black-hole seeding and growth.
**Base framework:** Lapi et al. 2026 (JCAP), [arXiv:2507.15436](https://arxiv.org/abs/2507.15436) — continuity + Smoluchowski equation, MCMC fit to EM data + PTA.
**New in the pilot:** explicit light and heavy seeds, start at $z \approx 20$, a merger delay time, and a LISA likelihood.

---

## 0. What is taken from Lapi+26 and what is new

| Part | Lapi+26 | Pilot (ours) |
|---|---|---|
| Evolution equation (continuity + Smoluchowski) | ✅ same | same |
| Accretion: log-normal $\lambda$, $\mu_\lambda(z)$, $\sigma_\lambda$, duty cycle | ✅ same | same ($\epsilon=0.1$ fixed; Lapi uses $\epsilon(\lambda)$) |
| Redshift range | $z \approx 7 \to 0$ | **new:** $z \approx 20 \to 0$ |
| Seeds | not modelled (initial condition only) | **new:** light + heavy seeds, free $n_L$, $n_H$ |
| Merger rate shape $f R_0 (1+z)^\omega e^{-\tau(1+z)} M^\eta$ | ✅ same | same |
| Merger delay $t_d$ | none (instant merger) | **new:** free $t_d$ |
| Mass ratio $p(q)$, $q\ge0.1$, $\delta_q=-1$ | ✅ same (fixed) | same (fixed in pilot; free later) |
| EM data: AGN LF, local BHMF | ✅ same | same |
| JWST data | validation only | **new:** one JWST LF bin in the likelihood |
| GW data | PTA amplitude | **new:** LISA Poisson likelihood with our $p_{\rm det}$ |
| Inference | emcee, 6 params | 9 params; **new:** EM-only vs EM + LISA comparison |

## 1. Evolution equation

We evolve the comoving black-hole mass function $n(M,t) = dN/(d\log M\, dV_c)$ from $z \approx 20$ to $z = 0$:

$$
\frac{\partial n}{\partial t} = -\frac{\partial}{\partial \log M}\left[\left\langle \frac{\dot M}{M\ln 10}\right\rangle n\right] + S_{\rm seed} + S_{\rm gain} - S_{\rm loss}
$$

## 2. Accretion (as in Lapi+26)

$$
\dot M = \frac{1-\epsilon}{\epsilon}\,\lambda\,\frac{M}{t_{\rm Edd}}, \qquad t_{\rm Edd}\approx 0.45\ {\rm Gyr}
$$

$$
\log\lambda \sim \mathcal{N}\big(\mu_0+\mu_1\log(1+z),\ \sigma_\lambda\big)
$$

- Duty cycle $\delta$: fraction of black holes that are active.
- Mean growth: $\langle \dot M \rangle = \delta\, \frac{1-\epsilon}{\epsilon}\, \langle\lambda\rangle\, M / t_{\rm Edd}$.
- Radiative efficiency fixed at $\epsilon = 0.1$ in the pilot (Lapi uses $\epsilon(\lambda)$).

## 3. Seeds (new)

$$
S_{\rm seed}(M,z) = \sum_{i=L,H} n_i\, G(\log M;\ \log M_i,\ 0.3)\, W_i(z)
$$

- Light seeds: $M_L \sim 10^2\,M_\odot$, formed at $z \approx 15$–$25$.
- Heavy seeds: $M_H \sim 10^5\,M_\odot$, formed at $z \approx 10$–$20$.
- $G$: log-normal mass spread (0.3 dex). $W_i(z)$: normalised redshift window, $\int W_i\, dt = 1$.
- Free: $n_L$, $n_H$. Seed masses and windows fixed in the pilot.

## 4. Mergers (Lapi+26 rate + delay)

$$
R(M,z) = f\, R_0 (1+z)^{\omega} e^{-\tau(1+z)} \left(\frac{M}{10^8 M_\odot}\right)^{\eta}
$$

- $R_0, \omega, \tau$ fixed to Lapi values (galaxy merger rate from JWST pair counts).
- **Delay (new):** $R$ is evaluated at $t - t_d$.
- Mass ratio (Lapi+26, Sec. 2.3):

$$
p(q) \propto q^{-\delta_q}\,\Theta_H(q - q_{\min}), \qquad \delta_q = -1,\quad q_{\min} = 0.1 \;\Rightarrow\; p(q)\propto q,\ q\in[0.1,1]
$$

  Fixed in Lapi (they say results depend weakly on it — true for PTA). For LISA, $q$ affects both $p_{\rm det}$ and the observed masses, so **free $\delta_q$ after the pilot**.
- Merger rate density:

$$
\frac{d^3N}{dt\,dM\,dq} = R(M,z)\;n(M,z)\;p(q)
$$
- Loss: $S_{\rm loss} = R\, n(M)$.
- Gain: $S_{\rm gain}(M) = \int dq\, p(q)\, R(M_1)\, n(M_1)\, \big|\partial \log M_1/\partial \log M\big|$, with $M_1 = M/(1+q)$.
- Each merger is assigned to its primary (no double counting). **Check Lapi Eqs. 2.10–2.14 before coding.**

## 5. Observables

AGN luminosity function:

$$
\Phi(\log L, z) = \delta \int d\log M\, n(M,z)\, P\big(\log\lambda = \log L - \log L_{\rm Edd}(M)\big)
$$

Black-hole mass function: $n(M, z=0)$.

LISA merger rate:

$$
\frac{dN}{dt_{\rm obs}\, dM_{\rm tot}\, dq\, dz} = R\, n(M_1)\, p(q)\, \frac{dV_c}{dz}\,\frac{1}{1+z}, \qquad M_{\rm tot} = M_1(1+q)
$$

Expected LISA detections:

$$
N_{\rm det} = T\int dz\,\frac{dV_c}{dz}\,\frac{1}{1+z}\int dM\int dq\;R\,n\,p(q)\;p_{\rm det}(M_{\rm tot},q,z)
$$

Use $p_{\rm det}(M_{\rm tot}, q, z)$, **not** a $p_{\rm det}$ already marginalised over $q$: otherwise detection assumes a different $p(q)$ from the model.

## 6. Free parameters (9)

| Group | Parameters |
|---|---|
| Accretion (Lapi) | $\mu_0,\ \mu_1,\ \sigma_\lambda,\ \delta$ |
| Mergers (Lapi + new) | $f,\ \eta,\ t_d$ |
| Seeds (new) | $\log n_L,\ \log n_H$ |

### What EM and GW are expected to measure (expectation, to be tested by the pilot)

**Lapi+26 results (context):** merger rate $\lesssim 0.1\times$ the JWST galaxy merger rate; binary mergers give at most ~30–50% of the PTA background (~3σ tension); accretion parameters depend strongly on the adopted local BHMF.

| Parameter | EM | GW (LISA) | Expected gain from GW |
|---|---|---|---|
| $\mu_0,\ \sigma_\lambda$ (Eddington ratio) | good | weak | stays EM-driven |
| $\mu_1$ ($z$-evolution of $\lambda$) | moderate (good at $z\lesssim3$, poor at high $z$) | some, via growth timing | small |
| $\delta$ (duty cycle) | good | weak | stays EM-driven |
| $f$ (merger efficiency) | poor (Lapi: upper limit only) | number of events | **large** |
| $\eta$ (mass slope of merger rate) | poor (Lapi: loose) | event mass distribution | **large** |
| $t_d$ (merger delay) | none | event $z$ distribution | **new constraint** |
| $n_L$ (light seeds) | poor (below EM mass limit) | low-mass, high-$z$ events | **large** |
| $n_H$ (heavy seeds) | weak (only via JWST bin) | $10^4$–$10^6\,M_\odot$ events at $z\gtrsim8$ | **large** |

**Degeneracies GW is expected to break**
1. $n_L, n_H \leftrightarrow \mu_0, \delta$: more seeds vs faster growth give a similar BHMF at $z\sim5$; LISA sees the seed population directly.
2. $f \leftrightarrow t_d$: both change how many mergers happen by a given $z$; the LISA event $z$ distribution separates them.
3. $f \leftrightarrow \eta$: normalisation vs mass slope; the LISA event mass distribution separates them.
4. $n_L \leftrightarrow n_H$: similar imprint at high mass, different imprint in the LISA mass spectrum (~$10^3$ vs ~$10^5\,M_\odot$).

## 7. Likelihoods

**EM:** Gaussian $\chi^2$ on
- Lapi's bolometric AGN luminosity function bins ($z \approx 0$–$7$),
- one local black-hole mass function (+0.3 dex systematic),
- one JWST luminosity-function bin at $z \sim 5$–$6$.
Exact data sets: to be decided.

**LISA:** inhomogeneous Poisson likelihood

$$
\ln\mathcal{L}_{\rm GW} = -N_{\rm exp}(\theta) + \sum_i \ln\!\big[T\, p_{\rm det}(M_i,z_i)\, r(M_i,z_i\,|\,\theta)\big]
$$

$T$ = mission time (4 yr). No measurement errors on $M, z$ in the pilot (known shortcut; $z$ errors may matter at high $z$).

## 8. Steps

1. **Reproduce Lapi+26:** rebuild the model, recover their $z=0$ mass function and luminosity-function fits.
2. **Add seeds, start at $z\approx20$:** check that results at $z<7$ barely change.
3. **LISA rate check:** apply our $p_{\rm det}$; expect tens of detections per year (Liu & Inayoshi 25, Cáceres-Burgos+25).
4. **Mock catalogue:** fiducial $\theta$, draw a 4-yr LISA event list.
5. **Fisher first, then MCMC:**
   - **5a. Fisher forecast** (EM-only vs EM + LISA): gives parameter errors and correlations quickly.
     - EM-only Fisher matrix will be singular (no information on $t_d$, little on $n_L$): use $F_{\rm total} = F_{\rm data} + F_{\rm prior}$ with Gaussian priors.
     - Check that numerical derivatives $\partial(\text{observable})/\partial\theta$ are stable against step size (solver noise can fake information).
     - Fisher assumes a Gaussian posterior; it may fail for $f$ (Lapi: upper limit only) and for $\log n_L$ near its prior edge.
   - **5b. MCMC** (emcee or nautilus, ~1 s per model run): confirm the Fisher results for the parameters that matter, and check for non-Gaussian posteriors.
6. **Decision:** go ahead if $n_L$, $n_H$, $f$ or $t_d$ tighten by a factor $\gtrsim 2$.

**Numerics:** grid $\log M = 1$–$11$, step 0.05 dex; explicit time stepping; merger term $O(N^2)$ per step. Expected ~1 s per run (to be checked).

## 9. Inputs needed

1. **Lapi+26 details:** exact equations, fixed values ($R_0, \omega, \tau$), fitted parameter values (fiducial $\theta$). Need a full read of the paper (no public code found).
2. **EM data tables:** bolometric AGN LF ($z\approx0$–$7$), one local BHMF (ideally Lapi's choices), one JWST LF bin at $z\sim5$–$6$.
3. **LISA $p_{\rm det}(M_{\rm tot}, q, z)$:** current grids are $q$-marginalised; need the $q$-resolved version.
4. **Choices to fix:** seed $z$ windows and masses, priors on all 9 parameters, $T = 4$ yr.
5. **Code:** continuity + Smoluchowski solver, mock event generator, Fisher module (derivatives), MCMC wrapper.
6. **Benchmarks:** Liu & Inayoshi 25 LISA rates (already computed in the group) for the rate sanity check.

## 10. Mock data: two stages

- **Pilot — own-model mocks:** model is exact by construction. Clean answer to *"does LISA add information?"*
- **Next — Barausse semi-analytic catalogues** (merger trees, popIII / Q3 seed models): our simple model is now imperfect, as with real data. Answers *"is the simple model good enough, or biased?"* Also gives priors on $t_d$ and $p(q)$ from the merger trees.

## 11. Known weak points

- Lapi's merger rate comes from JWST galaxy pair counts and is extrapolated above $z\approx7$. A halo-based rate may be needed later.
- Seed density and merger efficiency $f$ will likely be degenerate; the pilot should show how strongly.
