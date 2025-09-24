import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# ================================
# BACA BMP GRAYSCALE 8-BIT
# ================================
def read_bmp_numpy(filename):
    img = Image.open(filename).convert("L")  # konversi ke grayscale (L = 8-bit)
    pixels = np.array(img, dtype=np.uint8)
    return img, pixels

# ================================
# TULIS BMP GRAYSCALE 8-BIT
# ================================
def write_bmp_numpy(filename, pixels):
    img = Image.fromarray(pixels.astype(np.uint8), mode="L")
    img.save(filename)

# ================================
# NEGASI GRAYSCALE
# ================================
def negate_grayscale_numpy(pixels, Kmax=255):
    """Ko = Kmax - Ki"""
    return Kmax - pixels

# ================================
# HISTOGRAM
# ================================
def plot_histogram_numpy(ax, pixels, title="Histogram", color='gray'):
    ax.hist(pixels.ravel(), bins=256, range=(0,255), color=color, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel("Nilai Intensitas (0-255)")
    ax.set_ylabel("Frekuensi")

# ================================
# MAIN
# ================================
input_file = "gray_kucing8x8.bmp"   # ganti dengan file kamu
output_file = "negatif_" + input_file

# baca gambar
img, pixels = read_bmp_numpy(input_file)

# tampilkan nilai awal f(x,y)
print("Nilai f(x,y) awal:")
print(pixels)

# negasi dengan rumus Ko = 255 - Ki
neg_pixels = negate_grayscale_numpy(pixels, Kmax=255)

# tampilkan nilai akhir f(x,y)
print("\nNilai f(x,y) akhir setelah negasi:")
print(neg_pixels)

# ================================
# TAMPILKAN GAMBAR ASLI & NEGATIF
# ================================
fig, axs = plt.subplots(1,2, figsize=(10,5))
axs[0].imshow(pixels, cmap='gray', vmin=0, vmax=255)
axs[0].set_title("Gambar Asli")
axs[0].axis("off")

axs[1].imshow(neg_pixels, cmap='gray', vmin=0, vmax=255)
axs[1].set_title("Gambar Negatif")
axs[1].axis("off")

plt.show()

# ================================
# TAMPILKAN HISTOGRAM ASLI & NEGATIF
# ================================
fig, axs = plt.subplots(1,2, figsize=(12,4))
plot_histogram_numpy(axs[0], pixels, "Histogram Asli", color="blue")
plot_histogram_numpy(axs[1], neg_pixels, "Histogram Negatif", color="red")
plt.tight_layout()
plt.show()

# simpan gambar negatif
write_bmp_numpy(output_file, neg_pixels)
print(f"\nGambar negatif disimpan sebagai: {output_file}")
