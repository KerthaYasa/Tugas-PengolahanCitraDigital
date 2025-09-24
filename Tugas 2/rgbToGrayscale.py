import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ===============================
# 1. BACA GAMBAR
# ===============================
# Ganti dengan file gambar BMP/PNG/JPG yang kamu punya
img = mpimg.imread("trial.bmp")  

# Pastikan gambar dalam range 0-255 (jika float [0,1], kalikan 255)
if img.dtype == np.float32 or img.dtype == np.float64:
    img = (img * 255).astype(np.uint8)

# ===============================
# 2. KONVERSI GRAYSCALE
# ===============================
def rgb_to_grayscale(img, method="weighted"):
    """
    Konversi citra RGB ke grayscale.
    - method="average": (R+G+B)/3
    - method="weighted": NTSC (0.299R + 0.587G + 0.114B)
    """
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    if method == "average":
        gray = ((R + G + B) / 3).astype(np.uint8)
    elif method == "weighted":
        gray = (0.299 * R + 0.587 * G + 0.114 * B).astype(np.uint8)
    else:
        raise ValueError("Pilih method 'average' atau 'weighted'")
    return gray

# Pilih metode
gray_avg = rgb_to_grayscale(img, method="average")
gray_weighted = rgb_to_grayscale(img, method="weighted")

# ===============================
# 3. TAMPILKAN HASIL
# ===============================
fig, axs = plt.subplots(2, 3, figsize=(12, 6))

# Citra asli
axs[0,0].imshow(img)
axs[0,0].set_title("Citra Asli")
axs[0,0].axis("off")

# Grayscale Average
axs[0,1].imshow(gray_avg, cmap="gray")
axs[0,1].set_title("Grayscale Average")
axs[0,1].axis("off")

# Grayscale Weighted
axs[0,2].imshow(gray_weighted, cmap="gray")
axs[0,2].set_title("Grayscale Weighted (NTSC)")
axs[0,2].axis("off")

# Histogram RGB asli
colors = ('r', 'g', 'b')
for i, col in enumerate(colors):
    axs[1,0].hist(img[:,:,i].ravel(), bins=256, color=col, alpha=0.5)
axs[1,0].set_title("Histogram RGB")

# Histogram Average
axs[1,1].hist(gray_avg.ravel(), bins=256, color='gray')
axs[1,1].set_title("Histogram Grayscale Average")

# Histogram Weighted
axs[1,2].hist(gray_weighted.ravel(), bins=256, color='gray')
axs[1,2].set_title("Histogram Grayscale Weighted")

plt.tight_layout()
plt.show()
