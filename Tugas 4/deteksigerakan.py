"""
DETEKSI GERAKAN SESUAI BUKU
===========================

Rumus:
    C(x,y) = A(x,y) - B(x,y)
Atau menggunakan bobot:
    C(x,y) = wa * A(x,y) + wb * B(x,y)
    (wa = 1, wb = -1)

Interpretasi hasil:
- Nilai 0  → tidak ada perubahan / tidak bergerak
- Nilai < 0 (gelap) → posisi lama (objek di citra A)
- Nilai > 0 (terang) → posisi baru (objek di citra B)
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

# ===============================
# BAGIAN 4: TAMPILKAN HASIL
# ===============================
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.title("Citra A (Posisi Awal)")
plt.imshow(imgA, cmap="gray")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.title("Citra B (Posisi Akhir)")
plt.imshow(imgB, cmap="gray")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.title("Hasil Deteksi Gerakan\nHitam=Awal | Putih=Akhir")
plt.imshow(hasil, cmap="gray")
plt.axis("off")

plt.tight_layout()
plt.show()

# ====== Bagian 5: Informasi tambahan ======
print("Ukuran citra:", height, "x", width)
print("Contoh nilai piksel [0][0]:")
print("A =", imgA[0][0])
print("B =", imgB[0][0])
