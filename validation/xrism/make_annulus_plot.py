import numpy as np, astropy.io.fits as fits, matplotlib.pyplot as plt, pathlib

d = pathlib.Path(__file__).parent
x = fits.getdata(d/"sim_perseus.fits",1)['X']
y = fits.getdata(d/"sim_perseus.fits",1)['Y']

plt.figure(figsize=(4,4))
plt.scatter(x, y, s=1, alpha=0.6)
for r in (80,30):
    circle = plt.Circle((0,0), r, color='r', fill=False, lw=1)
    plt.gca().add_artist(circle)
plt.xlim(-120,120); plt.ylim(-120,120); plt.axis('off')
plt.tight_layout()
plt.savefig(d/"annulus.png", dpi=300) 