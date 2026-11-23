#!/usr/bin/env python
"""
plot_mass_range_check.py  --  bhflow

Mass-range check: the AGN / quasar black-hole population in the (log10 M, z) plane,
compared with
  * GW horizons: p_det = 0.1 contours of LISA, LGWA and XG (q-marginalised VTs;
    LISA and LGWA edge-corrected by vt_edge_extension.py),
  * one indicative box per EM facility (JWST, Rubin, Euclid, Roman, AXIS, Athena),
  * PTA (current, z < 1) and future PTA (hatched, z < 2).

GW mass = total source-frame binary mass; EM mass = single-BH mass.
EM boxes: minimum detectable BH mass for an unobscured type-1 AGN at lambda_Edd = 1,
evaluated at the box's mid-redshift (see EM dict below).

Inputs (paths relative to this file):
  highz_agn_quasar_compilation.npz             high-z AGN/quasar compilation
  rv15_tables_from_pdf.csv                     local AGN + dynamical BHs (Reines & Volonteri 2015)
  vt_lisa_popIII_qmarg_extended.npz            LISA p_det (from vt_edge_extension.py)
  vt_lgwa_popIII_qmarg_extended.npz            LGWA p_det (from vt_edge_extension.py)
  ../create_qmarginalised_VT_for_all_detectors/vt_xg_popIII_m80_z120_q_conditional.npz   XG p_det
  ../lowz_agn_data/dr16q_*extract*.npz         optional: SDSS DR16Q (z, logMBH)

Outputs:
  mass_range_check_mz_plane.{png,jpg,pdf}      full plane, z = 0-20
  mass_range_check_lowz_zoom.{png,jpg,pdf}     zoom on z < 2.2

Usage:  python plot_mass_range_check.py
"""

import os, glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from scipy.interpolate import RegularGridInterpolator
from astropy.cosmology import Planck18 as cosmo
import astropy.units as u
import astropy.constants as const

HERE     = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)   # all paths below are relative to this script
VT_DIR   = os.path.join('..', 'create_qmarginalised_VT_for_all_detectors')
LOWZ_DIR = next((p for p in (os.path.join('..', 'lowz_agn_data'), os.path.join('..', '..', 'lowz_agn_data')) if os.path.isdir(p)),
                os.path.join('..', 'lowz_agn_data'))   # codes/lowz_agn_data
LEDD = 1.26e38

plt.rcParams.update({'font.size': 17, 'axes.labelsize': 22, 'legend.fontsize': 15,
                     'xtick.labelsize': 18, 'ytick.labelsize': 18,
                     'xtick.major.size': 8, 'ytick.major.size': 8, 'xtick.minor.size': 4, 'ytick.minor.size': 4,
                     'xtick.major.width': 1.3, 'ytick.major.width': 1.3, 'axes.linewidth': 1.3,
                     'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.top': True, 'ytick.right': True})
# fixed categorical order (validated palette) + two neutrals; every box/region is also direct-labelled
INK = '#262626'
COL = dict(XG='#e87ba4', LGWA='#008300', LISA='#eda100',                       # GW: pink, green, gold
           JWST='#262626', Rubin='#7a7a7a', Euclid='#2a78d6', Roman='#eb6834',
           AXIS='#6250d6', Athena='#e34948', PTA='#1baf7a')


# ---------------------------------------------------------------- 1. AGN / quasar populations
em = dict(np.load('highz_agn_quasar_compilation.npz'))
hz = em['dup_of'] == ''
print('high-z compilation: %d unique objects, z = %.1f-%.1f' % (hz.sum(), em['z'][hz].min(), em['z'][hz].max()))

LOWZ = {}   # label -> (z, logM)
# SDSS DR16Q quasar properties (Wu & Shen 2022): small extract made from dr16q_prop_May01_2024.fits.gz
f16 = glob.glob(os.path.join(LOWZ_DIR, 'dr16q_*extract*.npz'))
if f16:
    d16 = np.load(f16[0]); ok = np.isfinite(d16['z']) & np.isfinite(d16['logMBH']) & (d16['logMBH'] > 0)
    LOWZ['SDSS DR16Q quasars (Wu & Shen 22)'] = (d16['z'][ok], d16['logMBH'][ok]); print('DR16Q:', ok.sum(), 'quasars')
else:
    print('DR16Q extract not found in', LOWZ_DIR)
# Reines & Volonteri 2015: rows printed in the PDF (Table 1: 5 of 244 BL AGN; Table 3: dwarf, RM, dynamical)
if os.path.exists('rv15_tables_from_pdf.csv'):
    import pandas as pd
    rv = pd.read_csv('rv15_tables_from_pdf.csv')
    zrv = rv['z'].fillna(0.03).values          # Table 3 has no z column; sample is z < 0.055
    LOWZ['local AGN + dyn. BHs (RV15 PDF tables)'] = (zrv, rv['logMBH'].values)
    print('RV15 (PDF):', rv.groupby('group').size().to_dict())


# ---------------------------------------------------------------- 2. GW horizons (p_det = 0.1)
# LISA/LGWA: q-marginalised VTs with the artificial p(q|m,z) interpolation edges removed (vt_edge_extension.py)
VT_FILES = {'LISA': 'vt_lisa_popIII_qmarg_extended.npz',
            'LGWA': 'vt_lgwa_popIII_qmarg_extended.npz',
            'XG'  : os.path.join(VT_DIR, 'vt_xg_popIII_m80_z120_q_conditional.npz')}
VT = {}
for det, fn in VT_FILES.items():
    d = np.load(fn)
    VT[det] = dict(M=d['mass'], Z=d['redshift'], p=d['vt'],
                   f=RegularGridInterpolator((d['mass'][:, 0], d['redshift'][0, :]), d['vt'], bounds_error=False, fill_value=0.))
pdet = lambda det, logm, z: VT[det]['f'](np.column_stack([np.atleast_1d(logm), np.atleast_1d(z)]))
for det in VT:
    s = VT[det]['p'] >= 0.1
    print('%-4s p_det>=0.1 : logM %.2f-%.2f' % (det, VT[det]['M'][s].min(), VT[det]['M'][s].max()))


# ---------------------------------------------------------------- 3. EM facilities as boxes (indicative)
# NIR/optical: m_lim -> nuLnu(1450) (flat f_nu) -> L_bol = 4.4 nuLnu -> M = L_bol / L_Edd; Lya drop-out cut.
# X-ray: F(0.5-2 keV) -> L(2-10 keV) (Gamma = 1.9) -> L_bol = 20 L_X.
# Depths: JWST 29.8 AB (JADES deep), Rubin LSST z = 25.6, Euclid Wide H = 24.5, Roman HLWAS 26.5,
#         AXIS deep 2e-18, Athena WFI deep 2e-17 erg/s/cm2.  PTA: M >~ 1e8, z <~ 1 (Bonoli+2025).
def mbh_min_nir(z, m_lim, edge_um, lam=1.0, bc=4.4):
    z = np.asarray(z, float); dl = cosmo.luminosity_distance(z).to(u.cm).value
    nuLnu = 4*np.pi*dl**2 * 10**(-0.4*(m_lim+48.6)) / (1+z) * (const.c.cgs.value/1450e-8)
    return np.where(0.1216*(1+z) > edge_um, np.nan, np.log10(bc*nuLnu/(lam*LEDD)))

def mbh_min_xray(z, f_soft, lam=1.0, kx=20.0, gamma=1.9):
    z = np.asarray(z, float); dl = cosmo.luminosity_distance(z).to(u.cm).value; a = 2-gamma
    L210 = 4*np.pi*dl**2*f_soft*(1+z)**(gamma-2) * (10**a-2**a)/(2**a-0.5**a)
    return np.log10(kx*L210/(lam*LEDD))

EM = {  # name: (limit function, z_lo, z_hi, logM_hi)
    'JWST':   (lambda z: mbh_min_nir(z, 29.8, 5.0),   3.0, 12.0, 9.0),
    'Rubin':  (lambda z: mbh_min_nir(z, 25.6, 0.922), 0.0,  6.5, 10.3),
    'Euclid': (lambda z: mbh_min_nir(z, 24.5, 2.0),   6.0,  9.0, 10.3),
    'Roman':  (lambda z: mbh_min_nir(z, 26.5, 1.77),  7.0, 13.5, 10.3),
    'AXIS':   (lambda z: mbh_min_xray(z, 2e-18),      0.0, 10.0, 9.0),
    'Athena': (lambda z: mbh_min_xray(z, 2e-17),      0.0,  8.0, 9.5),
}
BOXES = {}
print('%-7s %-10s %-26s' % ('', 'z range', 'logM_min at z = max(lo,0.1) / mid / hi'))
for k, (f, z0, z1, mhi) in EM.items():
    lo, mid, hi = (float(f(z)) for z in (max(z0, 0.1), 0.5*(z0+z1), z1))
    BOXES[k] = dict(m=(round(mid, 1), mhi), z=(z0, z1))
    print('%-7s %4.1f-%4.1f   %.1f / %.1f / %.1f' % (k, z0, z1, lo, mid, hi))
BOXES['PTA'] = dict(m=(8.0, 10.3), z=(0.0, 1.0))
PTA_FUTURE_Z = 2.0   # indicative reach of future PTAs (SKA era); hatched in the plot

# neat, consistent markers (neutral inks; identity by shape)
MSTY = {'local':            dict(marker='v', s=195, c='#3a3a3a', edgecolors='white', linewidths=0.8),
        'quasar_ground':    dict(marker='o', s=39,  c='#6e6e6e', edgecolors='white', linewidths=0.5),
        'quasar_jwst_host': dict(marker='D', s=90,  c=INK,       edgecolors='white', linewidths=0.7),
        'jwst_blagn':       dict(marker='s', s=82,  c=INK,       edgecolors='white', linewidths=0.7),
        'jwst_lrd':         dict(marker='o', s=90,  c='#d0021b',     edgecolors='white', linewidths=0.7),
        'jwst_stack':       dict(marker='P', s=135,  c=INK,       edgecolors='white', linewidths=0.7),
        'jwst_xray_z10':    dict(marker='*', s=390, c=INK,       edgecolors='white', linewidths=0.7)}
LBL = {'quasar_ground': r'$z\geq6$ quasars (Inayoshi+20, Fan+23)', 'quasar_jwst_host': 'quasars w/ JWST hosts (Yue+24)',
       'jwst_blagn': 'JWST broad-line AGN', 'jwst_lrd': 'JWST LRDs', 'jwst_stack': 'JADES stacks (Geris+25)',
       'jwst_xray_z10': r'$z\gtrsim10$ AGN (UHZ1, GHZ9, GHZ2)'}


# ---------------------------------------------------------------- 4. the plot
def mz_plot(zmax=20, mrange=(0.5, 10.5), ax=None, show_lowz=True, legend=True, det_labels=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(13, 10))
    # GW horizons: light fill + p_det = 0.1 line
    for det in ('XG', 'LGWA', 'LISA'):
        V = VT[det]
        ax.contourf(V['M'], V['Z'], V['p'], levels=[0.1, 1.01], colors=[COL[det]], alpha=0.10, zorder=1)
        ax.contour(V['M'], V['Z'], V['p'], levels=[0.1], colors=COL[det], linewidths=3.0, zorder=2)
    det_labels = det_labels or {'XG': (1.5, 15.0), 'LGWA': (3.9, 15.0), 'LISA': (5.6, 17.5)}
    for det, (x, y) in det_labels.items():
        ax.text(x, y, det, color=COL[det], fontsize=24, fontweight='bold', ha='center', va='center', zorder=6,
                clip_on=True)
    # EM + PTA boxes (outline), labelled at the top-left of their visible part
    for k, b in BOXES.items():
        (m0, m1), (z0, z1) = b['m'], b['z']
        if z0 >= zmax: continue
        if k == 'PTA':
            ax.add_patch(Rectangle((m0, z0), m1-m0, z1-z0, fc=COL[k], alpha=0.22, ec='none', zorder=3))
        ax.add_patch(Rectangle((m0, z0), m1-m0, z1-z0, fill=False, ec=COL[k], lw=3.0,
                               ls=('-.' if k == 'Rubin' else '-'), zorder=3))
        ztop = min(z1, zmax)
        ty, va = (z0 + 0.0075*zmax, 'bottom') if (k == 'Rubin' and z1 <= zmax) else (ztop - 0.006*zmax, 'top')
        ax.text(m0+0.07, ty, k, color=COL[k], fontsize=17, fontweight='bold', va=va, ha='left', zorder=7,
                clip_on=True, bbox=dict(fc='white', ec='none', alpha=0.85, pad=0.8))
    # future PTA (indicative): hatched extension above the current PTA box
    (pm0, pm1), (pz0, pz1) = BOXES['PTA']['m'], BOXES['PTA']['z']
    if PTA_FUTURE_Z > pz1:
        ax.add_patch(Rectangle((pm0, pz1), pm1-pm0, PTA_FUTURE_Z-pz1, fill=False, ec=COL['PTA'], lw=2.2,
                               ls='--', hatch='///', zorder=3))
        if PTA_FUTURE_Z <= zmax:
            ax.text(pm0+0.07, PTA_FUTURE_Z - 0.006*zmax, 'PTA future', color=COL['PTA'], fontsize=14, fontweight='bold',
                    va='top', ha='left', zorder=7, clip_on=True, bbox=dict(fc='white', ec='none', alpha=0.85, pad=0.8))
    # AGN / quasar data: neutral inks, identity by marker, thin white edge
    for lab, (zz, mm) in (LOWZ.items() if show_lowz else []):
        if lab.startswith('SDSS'):
            ax.scatter(mm, zz, marker='.', s=2, c='#b0b0b0', alpha=0.25, lw=0, rasterized=True, zorder=4)
        else:
            ax.scatter(mm, zz, **MSTY['local'], zorder=5)
    for cat, st in MSTY.items():
        if cat == 'local': continue
        sel = hz & (em['category'] == cat)
        ax.scatter(em['logMBH'][sel], em['z'][sel], **st, zorder=5)
    ax.set_xlim(*mrange); ax.set_ylim(0, zmax)
    ax.set_xlabel(r'$\log_{10}(M/M_\odot)$'); ax.set_ylabel(r'$z$')
    ax.minorticks_on(); ax.grid(color='0.9', lw=0.7, zorder=0)
    if legend:
        h = [Line2D([], [], ls='none', marker='o', ms=7, mfc='#b0b0b0', mec='none', label=k) for k in LOWZ if k.startswith('SDSS')]
        h += [Line2D([], [], ls='none', marker=MSTY['local']['marker'], ms=16, mfc=MSTY['local']['c'], mec='white',
                     label=k.replace(' (RV15 PDF tables)', ' (RV15)') + r', $z<0.06$') for k in LOWZ if not k.startswith('SDSS')]
        h += [Line2D([], [], ls='none', marker=st['marker'], ms=np.sqrt(st['s'])*1.15, mfc=st['c'], mec='white', mew=0.8,
                     label=LBL[cat]) for cat, st in MSTY.items() if cat != 'local']
        ax.legend(handles=h, loc='upper left', bbox_to_anchor=(1.01, 1.0), frameon=True, fancybox=True, framealpha=0.95, edgecolor='0.6', fontsize=19, borderpad=0.8,
                  handletextpad=0.4, labelspacing=0.7)
    return ax


def save(fig, stem):
    for ext, dpi in (('png', 160), ('jpg', 200), ('pdf', 200)):
        fig.savefig('%s.%s' % (stem, ext), bbox_inches='tight', dpi=dpi)
    print('saved', stem + '.{png,jpg,pdf}')


if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(13, 10))
    mz_plot(ax=ax)
    save(fig, 'mass_range_check_mz_plane')

    fig, ax = plt.subplots(figsize=(13, 7.5))
    mz_plot(ax=ax, zmax=2.2, mrange=(3.5, 10.5),
            det_labels={'XG': (3.78, 0.55), 'LGWA': (4.7, 1.95), 'LISA': (7.45, 1.95)})
    ax.set_ylim(-0.05, 2.2)
    save(fig, 'mass_range_check_lowz_zoom')
