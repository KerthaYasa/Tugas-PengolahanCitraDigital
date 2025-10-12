"""
PENGGABUNGAN CITRA (IMAGE BLENDING)
------------------------------------
Rumus dasar:
C(x,y) = wa * A(x,y) + wb * B(x,y)
dengan wa + wb = 1

Tujuan:
Menggabungkan dua citra menggunakan bobot berbeda pada masing-masing citra.

Library yang digunakan:
- matplotlib (untuk membaca & menampilkan gambar)
- math (untuk pembulatan nilai piksel)
Tanpa numpy.
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

# ====== Bagian 1: Membaca dua citra ======
# Gantilah path ini sesuai nama file kamu
try:
    imgA = mpimg.imread('trial.png')   # citra pertama
    imgB = mpimg.imread('trial1.png')  # citra kedua
except FileNotFoundError:
    print("❌ File gambar tidak ditemukan! Periksa kembali nama atau lokasinya.")
    exit()

# Pastikan ukuran citra sama (ambil ukuran minimum)
height = min(len(imgA), len(imgB))
width = min(len(imgA[0]), len(imgB[0]))

# ====== Bagian 2: Menentukan bobot ======
wa = 0.4   # bobot citra A
wb = 0.6   # bobot citra B
# Pastikan total bobot = 1
if round(wa + wb, 2) != 1.0:
    print("⚠️ Peringatan: total bobot tidak sama dengan 1")

# ====== Bagian 3: Penggabungan pixel per pixel ======
# RUMUS: C(x,y) = wa*A(x,y) + wb*B(x,y)
hasil = []  # hasil penggabungan disimpan di sini
for y in range(height):
    baris = []
    for x in range(width):
        pixelA = imgA[y][x]
        pixelB = imgB[y][x]
        # gabungkan tiap kanal RGB
        pixelC = [
            wa * float(pixelA[0]) + wb * float(pixelB[0]),
            wa * float(pixelA[1]) + wb * float(pixelB[1]),
            wa * float(pixelA[2]) + wb * float(pixelB[2])
        ]
        # Batasi nilai agar tidak melebihi 1.0
        pixelC = [min(1.0, max(0.0, v)) for v in pixelC]
        baris.append(pixelC)
    hasil.append(baris)

# ====== Bagian 4: Visualisasi menggunakan Matplotlib ======
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(imgA)
axes[0].set_title('Citra A (wa=0.4)')
axes[0].axis('off')

axes[1].imshow(imgB)
axes[1].set_title('Citra B (wb=0.6)')
axes[1].axis('off')

axes[2].imshow(hasil)
axes[2].set_title('Hasil Penggabungan')
axes[2].axis('off')

plt.tight_layout()
plt.show()

# ====== Bagian 5: Informasi tambahan ======
print("Ukuran citra:", height, "x", width)
print("Contoh nilai piksel [0][0]:")
print("A =", imgA[0][0])
print("B =", imgB[0][0])
print("C =", hasil[0][0])

# ====== Bagian 6: Penjelasan F(x,y) ======
"""
f(x,y) dimulai dari koordinat (0,0) yaitu piksel di pojok kiri atas gambar.
Urutan pembacaan: baris demi baris (row-major order),
dari atas ke bawah, dan di setiap baris dari kiri ke kanan.
Jadi f(0,0) = piksel kiri atas,
f(width-1,0) = piksel kanan atas,
f(0,height-1) = piksel kiri bawah.
"""
