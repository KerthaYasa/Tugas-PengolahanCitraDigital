import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# ============================
# Input gambar dari folder
# ============================
# Ganti dengan nama file gambarmu (misal: "gambar.png")
img = mpimg.imread("Tugas 2/kucing8x8.bmp")

# Jika gambar RGB, ubah ke grayscale dengan rata-rata channel
if img.ndim == 3:
    gray = img.mean(axis=2)
else:
    gray = img  # kalau sudah grayscale

# Skala ke 0–255 jika perlu (matplotlib sering baca float 0–1)
if gray.max() <= 1.0:
    gray = gray * 255

gray = gray.astype(int)

# ============================
# Konstanta brightness (C)
# ============================
C = 50

# ============================
# Fungsi clip agar tetap 0–255
# ============================
def clip(value):
    return max(0, min(255, value))

# ============================
# Terapkan rumus Ko = Ki + C
# ============================
bright_gray = np.vectorize(lambda v: clip(v + C))(gray)

# ============================
# Flatten untuk histogram
# ============================
flat_before = gray.flatten()
flat_after  = bright_gray.flatten()

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
axes[0,1].set_title("Histogram Sebelum Brightness")
axes[0,1].set_xlabel("Tingkat Warna (0–255)")
axes[0,1].set_ylabel("Frekuensi")

# Gambar sesudah brightness
axes[1,0].imshow(bright_gray, cmap="gray", vmin=0, vmax=255)
axes[1,0].set_title("Gambar Sesudah Brightness")
axes[1,0].axis("off")

# Histogram sesudah brightness
axes[1,1].bar(range(256), [np.count_nonzero(flat_after == i) for i in range(256)], color="orange")
axes[1,1].set_title("Histogram Sesudah Brightness")
axes[1,1].set_xlabel("Tingkat Warna (0–255)")
axes[1,1].set_ylabel("Frekuensi")

plt.tight_layout()
plt.show()

# ============================
# Cetak nilai grayscale
# ============================
print("Nilai Grayscale Asli:")
print(gray)

print("\nNilai Grayscale Setelah Brightness +C:")
print(bright_gray)
