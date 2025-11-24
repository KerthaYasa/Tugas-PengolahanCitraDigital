"""
DETEKSI GERAKAN (MOTION DETECTION)
Rumus PDF (Halaman 21-22):
    C(x,y) = wa * A(x,y) + wb * B(x,y)
    dengan wa = 1 dan wb = -1
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ========================================
# 1. BACA GAMBAR
# ========================================
imgA = mpimg.imread('trial3.png')
imgB = mpimg.imread('trial4.png')

h = min(len(imgA), len(imgB))
w = min(len(imgA[0]), len(imgB[0]))

# ========================================
# 2. BOBOT (SESUAI PDF)
# ========================================
wa = 1
wb = -1

# ========================================
# 3. DETEKSI GERAKAN
# ========================================
hasil = []

for y in range(h):
    baris = []
    for x in range(w):
        # Ambil piksel
        pA = imgA[y][x]
        pB = imgB[y][x]
        
        # Konversi ke grayscale
        grayA = (float(pA[0]) + float(pA[1]) + float(pA[2])) / 3.0
        grayB = (float(pB[0]) + float(pB[1]) + float(pB[2])) / 3.0
        
        # RUMUS UTAMA: C(x,y) = wa * A(x,y) + wb * B(x,y)
        C = wa * grayA + wb * grayB
        
        # Normalisasi untuk ditampilkan (0-1)
        C_norm = (C + 1.0) / 2.0
        C_norm = max(0.0, min(1.0, C_norm))
        
        baris.append([C_norm, C_norm, C_norm])
    hasil.append(baris)

# ========================================
# 4. TAMPILKAN HASIL
# ========================================
fig, ax = plt.subplots(1, 3, figsize=(15, 5))

ax[0].imshow(imgA)
ax[0].set_title('Citra A (Posisi Awal)')
ax[0].axis('off')

ax[1].imshow(imgB)
ax[1].set_title('Citra B (Posisi Akhir)')
ax[1].axis('off')

ax[2].imshow(hasil, cmap='gray')
ax[2].set_title(f'Hasil: C(x,y) = {wa}*A(x,y) + ({wb})*B(x,y)\nHitam=Awal | Putih=Akhir')
ax[2].axis('off')

plt.tight_layout()
plt.show()

# ========================================
# 5. INFO
# ========================================
print("="*50)
print("DETEKSI GERAKAN")
print("="*50)
print(f"Rumus : C(x,y) = wa * A(x,y) + wb * B(x,y)")
print(f"Bobot : wa = {wa}, wb = {wb}")
print(f"Ukuran: {w} x {h}")
print("="*50)