import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math

# ======================
# BACA GAMBAR BMP
# ======================
def read_bmp_numpy(trial):
    img = Image.open(trial).convert("RGB")
    return np.array(img, dtype=np.uint8)


# ======================
# SIMPAN GAMBAR
# ======================
def write_bmp_numpy(filename, pixels):
    img = Image.fromarray(pixels.astype(np.uint8), mode="RGB")
    img.save(filename)

# ======================
# ROTASI 90° CW
# Rumus: w’ = h, h’ = w
# x’ = w’ – 1 – y
# y’ = x
# ======================
def rotate_90(pixels):
    h, w, _ = pixels.shape
    new_w, new_h = h, w
    new_pixels = np.zeros((new_h, new_w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            new_x = new_w - 1 - y
            new_y = x
            new_pixels[new_y, new_x] = pixels[y, x]
    return new_pixels

# ======================
# ROTASI 180° CW
# Rumus: x’ = w’ – 1 – x
#        y’ = h’ – 1 – y
# ======================
def rotate_180(pixels):
    h, w, _ = pixels.shape
    new_pixels = np.zeros_like(pixels)
    for y in range(h):
        for x in range(w):
            new_x = w - 1 - x
            new_y = h - 1 - y
            new_pixels[new_y, new_x] = pixels[y, x]
    return new_pixels

# ======================
# ROTASI BEBAS (θ derajat CCW)
# x’ = x cosθ + y sinθ
# y’ = -x sinθ + y cosθ
# ======================
def rotate_free(pixels, theta_deg):
    theta = math.radians(theta_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)

    h, w, _ = pixels.shape
    new_w = int(abs(w*cos_t) + abs(h*sin_t))
    new_h = int(abs(w*sin_t) + abs(h*cos_t))

    # background putih
    new_pixels = np.ones((new_h, new_w, 3), dtype=np.uint8) * 255  

    cx, cy = w // 2, h // 2
    ncx, ncy = new_w // 2, new_h // 2

    for y in range(new_h):
        for x in range(new_w):
            xt = x - ncx
            yt = y - ncy
            old_x = int(xt*cos_t + yt*sin_t + cx)
            old_y = int(-xt*sin_t + yt*cos_t + cy)

            if 0 <= old_x < w and 0 <= old_y < h:
                new_pixels[y, x] = pixels[old_y, old_x]

    return new_pixels


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    input_file = "trial.bmp"   # ganti nama file sesuai
    pixels = read_bmp_numpy(input_file)

    rot90 = rotate_90(pixels)
    rot180 = rotate_180(pixels)
    rotfree = rotate_free(pixels, 25)  # contoh rotasi 25° CCW

    # tampilkan hasil
    fig, axs = plt.subplots(1,4, figsize=(16,6))
    axs[0].imshow(pixels)
    axs[0].set_title("Asli")
    axs[0].axis("off")

    axs[1].imshow(rot90)
    axs[1].set_title("Rotasi 90° CW")
    axs[1].axis("off")

    axs[2].imshow(rot180)
    axs[2].set_title("Rotasi 180° CW")
    axs[2].axis("off")

    axs[3].imshow(rotfree)
    axs[3].set_title("Rotasi 25° CCW")
    axs[3].axis("off")

    plt.tight_layout()
    plt.show()

    # simpan hasil
    write_bmp_numpy("rotasi90_" + input_file, rot90)
    write_bmp_numpy("rotasi180_" + input_file, rot180)
    write_bmp_numpy("rotasi25_" + input_file, rotfree)
    print("Rotasi selesai. File hasil disimpan.")

