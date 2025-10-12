"""
DETEKSI GERAKAN (MOTION DETECTION)
-----------------------------------
Rumus dasar:
C(x,y) = wa * A(x,y) + wb * B(x,y)
dengan wa = 1 dan wb = -1

Tujuan:
Menampilkan posisi awal dan posisi akhir dari objek yang bergerak.
- Warna gelap menunjukkan posisi awal (objek lama)
- Warna terang menunjukkan posisi akhir (objek baru)

Library yang digunakan:
- matplotlib (untuk membaca & menampilkan gambar)
Tanpa numpy.
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ====== Bagian 1: Membaca dua citra ======
try:
    imgA = mpimg.imread('trial3.png')    # frame pertama
    imgB = mpimg.imread('trial4.png')   # frame kedua
except FileNotFoundError:
    print("❌ File gambar tidak ditemukan! Periksa nama atau lokasinya.")
    exit()

# Pastikan ukuran sama (ambil ukuran minimum)
height = min(len(imgA), len(imgB))
width = min(len(imgA[0]), len(imgB[0]))

# ====== Bagian 2: Bobot ======
wa = 1
wb = -1

# ====== Bagian 3: Pengurangan antar citra ======
hasil = []
for y in range(height):
    baris = []
    for x in range(width):
        pixelA = imgA[y][x]
        pixelB = imgB[y][x]

        # konversi grayscale sederhana (rata-rata RGB)
        grayA = (float(pixelA[0]) + float(pixelA[1]) + float(pixelA[2])) / 3
        grayB = (float(pixelB[0]) + float(pixelB[1]) + float(pixelB[2])) / 3

        # rumus utama: C(x,y) = wa*A(x,y) + wb*B(x,y)
        diff = wa * grayA + wb * grayB

        # normalisasi agar terlihat jelas dalam rentang 0–1
        diff_norm = (diff + 1) / 2   # geser dari -1..1 ke 0..1

        # ubah ke RGB grayscale
        baris.append([diff_norm, diff_norm, diff_norm])
    hasil.append(baris)

# ====== Bagian 4: Visualisasi ======
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(imgA, cmap='gray')
axes[0].set_title('Citra A (posisi awal)')
axes[0].axis('off')

axes[1].imshow(imgB, cmap='gray')
axes[1].set_title('Citra B (posisi akhir)')
axes[1].axis('off')

axes[2].imshow(hasil, cmap='gray')
axes[2].set_title('Hasil Deteksi Gerakan\nHitam=Posisi Awal | Putih=Posisi Akhir')
axes[2].axis('off')

plt.tight_layout()
plt.show()

# ====== Bagian 5: Informasi tambahan ======
print("Ukuran citra:", height, "x", width)
print("Contoh nilai piksel [0][0]:")
print("A =", imgA[0][0])
print("B =", imgB[0][0])
