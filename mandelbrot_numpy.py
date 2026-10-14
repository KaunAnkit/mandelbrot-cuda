import numpy as np
from PIL import Image

WIDTH = 800
HEIGHT = 600

X_MIN ,X_MAX = -2.5 ,1.0
Y_MIN, Y_MAX = -1.25 , 1.25

x = np.linspace(X_MIN,X_MAX,WIDTH)
y = np.linspace(Y_MIN,Y_MAX,HEIGHT)

X, Y = np.meshgrid(x, y) 

C = X + 1j * Y

MAX_ITER = 100
Z = np.zeros(C.shape, dtype=np.complex128)
iterations = np.full(C.shape, MAX_ITER, dtype=np.int32)

active = np.full(C.shape, True, dtype=bool)

for i in range(MAX_ITER):
    Z[active] = Z[active] * Z[active] + C[active]

    newly_escaped = active & (np.abs(Z) > 2)
    iterations[newly_escaped] = i
    active[newly_escaped] = False

    if not np.any(active):
        break


rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

escaped = iterations < MAX_ITER

brightness = (255 * iterations[escaped] / MAX_ITER).astype(np.uint8)

rgb[escaped, 0] = brightness
rgb[escaped, 1] = brightness
rgb[escaped, 2] = 255


image = Image.fromarray(rgb)
image.save("mandelbrot_numpy.png")
print("Saved mandelbrot_numpy.png")