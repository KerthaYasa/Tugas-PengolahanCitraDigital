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
# Konstanta peningkatan kontras
# ============================
G = 3   # koefisien penguatan kontras, >1 untuk kontras lebih tinggi
P = 180   # pusat pengontrasan

# ============================
# Fungsi clip agar tetap 0–255
# ============================
def clip(value):
    return max(0, min(255, value))

# ============================
# Terapkan rumus kontras: Ko = G*(Ki-P)+P
# ============================
contrast_gray = np.vectorize(lambda v: clip(G * (v - P) + P))(gray)

# ============================
# Flatten untuk histogram
# ============================
flat_before = gray.flatten()
flat_after  = contrast_gray.flatten()

# ============================
# Tampilkan gambar & histogram
# ============================
fig, axes = plt.subplots(2, 2, figsize=(10,8))

# Gambar asli
axes[0,0].imshow(gray, cmap="gray", vmin=0, vmax=255)
axes[0,0].set_title("Gambar Asli")
axes[0,0].axis("off")

# Histogram asli
axes[0,1].bar(range(256), [np.count_nonzero(flat_before == i) for i in range(256)], color="blue")
axes[0,1].set_title("Histogram Sebelum Kontras")
axes[0,1].set_xlabel("Tingkat Warna (0–255)")
axes[0,1].set_ylabel("Frekuensi")

# Gambar sesudah kontras
axes[1,0].imshow(contrast_gray, cmap="gray", vmin=0, vmax=255)
axes[1,0].set_title("Gambar Sesudah Kontras")
axes[1,0].axis("off")

# Histogram sesudah kontras
axes[1,1].bar(range(256), [np.count_nonzero(flat_after == i) for i in range(256)], color="orange")
axes[1,1].set_title("Histogram Sesudah Kontras")
axes[1,1].set_xlabel("Tingkat Warna (0–255)")
axes[1,1].set_ylabel("Frekuensi")

plt.tight_layout()
plt.show()

# ============================
# Cetak nilai grayscale
# ============================
print("Nilai Grayscale Asli:")
print(gray)

print("\nNilai Grayscale Setelah Peningkatan Kontras:")
print(contrast_gray)
