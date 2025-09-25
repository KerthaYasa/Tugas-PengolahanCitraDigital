import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ========================
# 1. BACA GAMBAR
# ========================
img = mpimg.imread("Tugas 3/trial.bmp")

# ========================
# 2. TENTUKAN KOORDINAT CROPPING
# ========================
xL, yT = 50, 50   # kiri-atas
xR, yB = 200, 200 # kanan-bawah

# ========================
# 3. RUMUS CROPPING (transformasi koordinat)
# ========================
w_prime = xR - xL
h_prime = yB - yT

# Buat array kosong sesuai ukuran hasil crop
cropped = np.zeros((h_prime, w_prime, img.shape[2]), dtype=img.dtype)

# Terapkan rumus: x' = x - xL, y' = y - yT
for y in range(yT, yB):
    for x in range(xL, xR):
        x_prime = x - xL
        y_prime = y - yT
        cropped[y_prime, x_prime] = img[y, x]

# ========================
# 4. TAMPILKAN HASIL
# ========================
fig, axs = plt.subplots(1, 2, figsize=(8, 4))

# Gambar asli + kotak merah
axs[0].imshow(img, cmap="gray")
axs[0].set_title("Citra Asli")
axs[0].add_patch(plt.Rectangle((xL, yT), w_prime, h_prime,
                               edgecolor="red", facecolor="none", lw=2))
axs[0].axis("off")

# Hasil cropping
axs[1].imshow(cropped, cmap="gray")
axs[1].set_title(f"Citra Hasil Cropping\nUkuran: {w_prime}x{h_prime}")
axs[1].axis("off")

plt.show()
