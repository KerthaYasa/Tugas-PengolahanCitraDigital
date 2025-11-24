import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ============================
# 1. Baca Gambar
# ============================
img = mpimg.imread("Tugas 2/kucing8x8.bmp")  # Ganti dengan file kamu

# Ubah ke grayscale (jika RGB)
if len(img.shape) == 3:  # gambar RGB
    gray = []
    for row in img:
        gray_row = []
        for pixel in row:
            # pixel = [R, G, B]
            avg = sum(pixel) / len(pixel)
            gray_row.append(avg)
        gray.append(gray_row)
else:
    gray = img.tolist()

# Skala ke 0–255 jika gambar bernilai 0–1
max_val = max(max(row) for row in gray)
if max_val <= 1.0:
    gray = [[int(pixel * 255) for pixel in row] for row in gray]
else:
    gray = [[int(pixel) for pixel in row] for row in gray]

# ============================
# 2. Terapkan Rumus Negatif
# ============================
Kmax = 255
negative_gray = [[Kmax - pixel for pixel in row] for row in gray]

# ============================
# 3. Siapkan Data Histogram
# ============================
# Flatten gambar jadi satu list panjang
flat_before = [pixel for row in gray for pixel in row]
flat_after  = [pixel for row in negative_gray for pixel in row]

# Hitung frekuensi kemunculan tiap nilai 0–255
hist_before = [flat_before.count(i) for i in range(256)]
hist_after  = [flat_after.count(i) for i in range(256)]

# ============================
# 4. Tampilkan Semua Hasil
# ============================
fig, axes = plt.subplots(2, 2, figsize=(10,8))

# Gambar asli
axes[0,0].imshow(gray, cmap="gray", vmin=0, vmax=255)
axes[0,0].set_title("Gambar Asli (Grayscale)")
axes[0,0].axis("off")

# Histogram asli
axes[0,1].bar(range(256), hist_before, color="blue")
axes[0,1].set_title("Histogram Asli")
axes[0,1].set_xlabel("Tingkat Warna (0–255)")
axes[0,1].set_ylabel("Frekuensi")

# Gambar negatif
axes[1,0].imshow(negative_gray, cmap="gray", vmin=0, vmax=255)
axes[1,0].set_title("Gambar Negatif")
axes[1,0].axis("off")

# Histogram negatif
axes[1,1].bar(range(256), hist_after, color="orange")
axes[1,1].set_title("Histogram Negatif")
axes[1,1].set_xlabel("Tingkat Warna (0–255)")
axes[1,1].set_ylabel("Frekuensi")

plt.tight_layout()
plt.show()

# ============================
# 5. Cetak Nilai Grayscale
# ============================
print("Nilai Grayscale Asli:")
for row in gray:
    print(row)

print("\nNilai Grayscale Setelah Negatif:")
for row in negative_gray:
    print(row)
