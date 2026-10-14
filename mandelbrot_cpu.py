from PIL import Image

import time

WIDTH = 800
HEIGHT = 600
MAX_ITER = 100

image = Image.new("RGB", (WIDTH, HEIGHT))
print(f"Image size: {image.size}")

X_MIN = -2.5
X_MAX = 1.0
Y_MIN = -1.25
Y_MAX = 1.25    


def mandelbrot(c):
    z = 0j

    for iteration in range(MAX_ITER):
        z = z * z + c

        if abs(z) > 2:
            return iteration

    return MAX_ITER

start = time.perf_counter()

for y in range(HEIGHT):
    for x in range(WIDTH):
        real = X_MIN + x * (X_MAX - X_MIN) / (WIDTH - 1)
        imag = Y_MIN + y * (Y_MAX - Y_MIN) / (HEIGHT - 1)
        c = complex(real, imag)

        iterations = mandelbrot(c)

        if iterations == MAX_ITER:
            color = (0, 0, 0)
        else:
            brightness = int(255 * iterations / MAX_ITER)
            color = (brightness, brightness, 255)

        image.putpixel((x, y), color)


image.save("mandelbrot_cpu.png")

end = time.perf_counter()
print(f"CPU render time: {end - start:.3f} seconds")

print("Saved mandelbrot_cpu.png")