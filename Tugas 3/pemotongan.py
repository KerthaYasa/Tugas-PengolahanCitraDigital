import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ========================
# 1. BACA GAMBAR
# ========================
# Ganti "trial.bmp" dengan file gambar yang ingin digunakan
img = mpimg.imread("trial.bmp")  

# ========================
# 2. TENTUKAN KOORDINAT CROPPING
# ========================
# (xL, yT) = titik kiri-atas
# (xR, yB) = titik kanan-bawah
xL, yT = 50, 50   # kiri-atas
xR, yB = 200, 200 # kanan-bawah

# ========================
# 3. RUMUS CROPPING
# ========================
# Sesuai teori: 
# w' = xR - xL
# h' = yB - yT
w_prime = xR - xL
h_prime = yB - yT

# Ambil bagian citra dari koordinat (yT:yB, xL:xR)
cropped = img[yT:yB, xL:xR]

# ========================
# 4. TAMPILKAN HASIL
# ========================
fig, axs = plt.subplots(1, 2, figsize=(8, 4))

# Citra asli dengan kotak merah crop
axs[0].imshow(img, cmap="gray")
axs[0].set_title("Citra Asli")
# tambahkan rectangle sesuai koordinat crop
axs[0].add_patch(plt.Rectangle((xL, yT), w_prime, h_prime, 
                               edgecolor="red", facecolor="none", lw=2))
axs[0].axis("off")

# Citra hasil cropping
axs[1].imshow(cropped, cmap="gray")
axs[1].set_title(f"Citra Hasil Cropping\nUkuran: {w_prime}x{h_prime}")
axs[1].axis("off")

plt.show()
