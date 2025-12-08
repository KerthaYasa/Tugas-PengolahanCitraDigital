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

# ===============================
# BAGIAN 1: BACA DUA CITRA
# ===============================
try:
    imgA = mpimg.imread("trial3.png")   # Citra posisi awal
    imgB = mpimg.imread("trial4.png")   # Citra posisi akhir
except:
    print("❌ File tidak ditemukan!")
    exit()

# Pastikan ukuran sama
h = min(len(imgA), len(imgB))
w = min(len(imgA[0]), len(imgB[0]))

# ===============================
# BAGIAN 2: BOBOT SESUAI BUKU
# ===============================
wa = 1
wb = -1

# ===============================
# BAGIAN 3: OPERASI PENGURANGAN C(x,y)
# ===============================
hasil = []

for y in range(h):
    baris = []
    for x in range(w):

        # Ambil piksel A dan B
        rA, gA, bA = imgA[y][x][:3]
        rB, gB, bB = imgB[y][x][:3]

        # Konversi ke grayscale (rata-rata 3 komponen)
        grayA = (float(rA) + float(gA) + float(bA)) / 3
        grayB = (float(rB) + float(gB) + float(bB)) / 3

        # Rumus utama!
        diff = wa * grayA + wb * grayB       # = grayA - grayB

        # NORMALISASI SEDERHANA 0..1 (agar bisa ditampilkan)
        # diff bisa negatif → geser ke rentang 0..1
        diff_norm = (diff + 1) / 2           # ubah dari -1..1 ke 0..1

        # simpan sebagai grayscale RGB
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
