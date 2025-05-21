import numpy as np
from astropy.io import fits
import pathlib

np.random.seed(42)
line_fraction_354 = 0.10      # 3.54 keV
line_fraction_280 = line_fraction_354 * 0.74

N  = 15_000
N54 = int(N*line_fraction_354)
N28 = int(N*line_fraction_280)

E_354 = 3.54 + 0.005*np.random.randn(N54)
E_280 = 2.80 + 0.005*np.random.randn(N28)
E_cont = 1.   + 9.0*np.random.rand(N - N54 - N28)

energies = np.concatenate([E_354, E_280, E_cont])

theta = np.random.uniform(0, 2*np.pi, N)
x54 = np.random.uniform(30, 80, len(E_354))
r28 = np.random.uniform(30, 80, len(E_280))
r_cont = np.random.uniform(0, 110, len(E_cont))
radii = np.concatenate([x54, r28, r_cont])

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