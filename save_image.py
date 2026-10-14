import numpy as np
from PIL import Image

WIDTH = 800
HEIGHT = 600
MAX_ITER = 100

iterations = np.fromfile("iterations.bin", dtype=np.int32)
iterations = iterations.reshape((HEIGHT, WIDTH))

rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
escaped = iterations < MAX_ITER

brightness = (
    255 * iterations[escaped] / MAX_ITER
).astype(np.uint8)

rgb[escaped, 2] = 255
rgb[escaped, 0] = brightness
rgb[escaped, 1] = brightness

Image.fromarray(rgb).save("mandelbrot_cuda.png")
print("Saved mandelbrot_cuda.png")