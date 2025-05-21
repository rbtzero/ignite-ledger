import numpy as np
from astropy.io import fits
import pathlib

np.random.seed(42)
N = 15_000  # ~30 ks dummy file
E_line = 3.54 + 0.005*np.random.randn(N//10)   # 3.54 keV line
E_cont = 1. + 9.0*np.random.rand(N - len(E_line))
energies = np.concatenate([E_line, E_cont])

theta = np.random.uniform(0, 2*np.pi, N)
r_line = np.random.uniform(30, 80, len(E_line))
r_cont = np.random.uniform(0, 110, len(E_cont))
radii = np.concatenate([r_line, r_cont])

x = radii*np.cos(theta)
y = radii*np.sin(theta)

d = pathlib.Path(__file__).resolve().parents[2] / "validation" / "xrism"
d.mkdir(parents=True, exist_ok=True)

hdu = fits.BinTableHDU.from_columns([
    fits.Column(name='PI', array=(energies*1000).astype('int32'), format='J'),
    fits.Column(name='X',  array=x.astype('float32'),             format='E'),
    fits.Column(name='Y',  array=y.astype('float32'),             format='E')
])
outfile = d / 'sim_perseus.fits'
hdu.writeto(outfile, overwrite=True)
print(f"\u2714  {outfile} written") 