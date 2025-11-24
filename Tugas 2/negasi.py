import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ============================
# 1. Baca Gambar
# ============================
nama_file = "Tugas 2/kucing8x8.bmp"
img = mpimg.imread(nama_file)

# Ubah ke grayscale menggunakan rumus NTSC dari PDF (halaman 16)
# Ko = 0.299*R + 0.587*G + 0.114*B
if len(img.shape) == 3:  # gambar RGB
    gray = []
    for row in img:
        gray_row = []
        for pixel in row:
            r, g, b = pixel[0], pixel[1], pixel[2]
            
            # Jika nilai 0-1, ubah ke 0-255
            if r <= 1.0:
                r, g, b = r * 255, g * 255, b * 255
            
            # Rumus NTSC dari PDF
            Ki = int(0.299 * r + 0.587 * g + 0.114 * b)
            gray_row.append(Ki)
        gray.append(gray_row)
else:
    gray = img.tolist()
    # Pastikan nilainya 0-255
    max_val = max(max(row) for row in gray)
    if max_val <= 1.0:
        gray = [[int(pixel * 255) for pixel in row] for row in gray]
    else:
        gray = [[int(pixel) for pixel in row] for row in gray]

# ============================
# 2. Terapkan Rumus Negatif (PDF halaman 15)
# Ko = Kmax - Ki
# Untuk 8 bit: Ko = 255 - Ki
# ============================
Kmax = 255
negative_gray = []
for row in gray:
    negative_row = []
    for Ki in row:
        Ko = Kmax - Ki  # Rumus PDF: Ko = Kmax - Ki
        negative_row.append(Ko)
    negative_gray.append(negative_row)

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
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Gambar asli
axes[0,0].imshow(gray, cmap="gray", vmin=0, vmax=255)
axes[0,0].set_title("Gambar Asli (Ki)", fontweight='bold')
axes[0,0].axis("off")

# Histogram asli
axes[0,1].bar(range(256), hist_before, color="blue", alpha=0.7)
axes[0,1].set_title("Histogram Asli", fontweight='bold')
axes[0,1].set_xlabel("Nilai Keabuan (Ki)")
axes[0,1].set_ylabel("Frekuensi")
axes[0,1].set_xlim([0, 255])

# Gambar negatif
axes[1,0].imshow(negative_gray, cmap="gray", vmin=0, vmax=255)
axes[1,0].set_title("Gambar Negatif: Ko = 255 - Ki", fontweight='bold')
axes[1,0].axis("off")

# Histogram negatif
axes[1,1].bar(range(256), hist_after, color="orange", alpha=0.7)
axes[1,1].set_title("Histogram Negatif", fontweight='bold')
axes[1,1].set_xlabel("Nilai Keabuan (Ko)")
axes[1,1].set_ylabel("Frekuensi")
axes[1,1].set_xlim([0, 255])

plt.tight_layout()
plt.show()

# ============================
# 5. Cetak Nilai Grayscale
# ============================
print("="*60)
print("PROGRAM NEGASI CITRA".center(60))
print("Rumus PDF: Ko = Kmax - Ki = 255 - Ki".center(60))
print("="*60)

print("\n=== Matriks Nilai Asli (Ki) ===")
for row in gray:
    print(row)

print("\n=== Matriks Nilai Negatif (Ko = 255 - Ki) ===")
for row in negative_gray:
    print(row)

# ============================
# 6. Contoh Perhitungan Manual
# ============================
print(f"\n{'='*60}")
print("CONTOH PERHITUNGAN RUMUS Ko = 255 - Ki".center(60))
print(f"{'='*60}")

tinggi = len(gray)
lebar = len(gray[0])

# Ambil 5 contoh piksel
posisi_contoh = [
    (0, 0),
    (0, lebar-1),
    (tinggi//2, lebar//2),
    (tinggi-1, 0),
    (tinggi-1, lebar-1)
]

for y, x in posisi_contoh:
    Ki = gray[y][x]
    Ko = negative_gray[y][x]
    
    print(f"\nPiksel [{y},{x}]:")
    print(f"  Ki (asli)   = {Ki}")
    print(f"  Ko = 255 - Ki")
    print(f"  Ko = 255 - {Ki}")
    print(f"  Ko (negatif) = {Ko}")

print(f"\n{'='*60}")
print("✓ SELESAI".center(60))
print(f"{'='*60}\n")