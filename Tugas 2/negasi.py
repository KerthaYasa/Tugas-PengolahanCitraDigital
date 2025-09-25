import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# ============================
# Input gambar dari folder
# ============================
img = mpimg.imread("Tugas 2/kucing8x8.bmp")  # ganti sesuai nama file

# Jika gambar RGB, ambil rata-rata channel
if img.ndim == 3:
    gray = img.mean(axis=2)
else:
    gray = img

# Skala ke 0–255 jika perlu
if gray.max() <= 1.0:
    gray = gray * 255

gray = gray.astype(int)

# ============================
# Konstanta untuk negatif
# ============================
Kmax = 255

# ============================
# Terapkan rumus negatif: Ko = Kmax - Ki
# ============================
negative_gray = Kmax - gray

# ============================
# Flatten untuk histogram
# ============================
flat_before = gray.flatten()
flat_after  = negative_gray.flatten()

# ============================
# Tampilkan gambar & histogram
# ============================
fig, axes = plt.subplots(2, 2, figsize=(10,8))

# Gambar asli
axes[0,0].imshow(gray, cmap="gray", vmin=0, vmax=255)
axes[0,0].set_title("Gambar Asli (Grayscale)")
axes[0,0].axis("off")

# Histogram asli
axes[0,1].bar(range(256), [np.count_nonzero(flat_before == i) for i in range(256)], color="blue")
axes[0,1].set_title("Histogram Asli")
axes[0,1].set_xlabel("Tingkat Warna (0–255)")
axes[0,1].set_ylabel("Frekuensi")

# Gambar negatif
axes[1,0].imshow(negative_gray, cmap="gray", vmin=0, vmax=255)
axes[1,0].set_title("Gambar Negatif")
axes[1,0].axis("off")

# Histogram negatif
axes[1,1].bar(range(256), [np.count_nonzero(flat_after == i) for i in range(256)], color="orange")
axes[1,1].set_title("Histogram Negatif")
axes[1,1].set_xlabel("Tingkat Warna (0–255)")
axes[1,1].set_ylabel("Frekuensi")

plt.tight_layout()
plt.show()

# ============================
# Cetak nilai grayscale
# ============================
print("Nilai Grayscale Asli:")
print(gray)

print("\nNilai Grayscale Setelah Negatif:")
print(negative_gray)
