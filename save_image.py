import numpy as np
from PIL import Image

WIDTH = 800
HEIGHT = 600
MAX_ITER = 500

iterations = np.fromfile("iterations.bin", dtype=np.int32)
iterations = iterations.reshape((HEIGHT, WIDTH))

rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

escaped = iterations < MAX_ITER
t = iterations.astype(np.float32) / MAX_ITER

# Strong, repeating color bands
rgb[..., 0] = (255 * (0.5 + 0.5 * np.sin(0.15 * iterations))).astype(np.uint8)
rgb[..., 1] = (255 * (0.5 + 0.5 * np.sin(0.15 * iterations + 2.0))).astype(np.uint8)
rgb[..., 2] = (255 * (0.5 + 0.5 * np.sin(0.15 * iterations + 4.0))).astype(np.uint8)

# Keep the interior black
rgb[~escaped] = 0

Image.fromarray(rgb).save("mandelbrot_cuda_new2.png")
print("Saved mandelbrot_cuda.png")