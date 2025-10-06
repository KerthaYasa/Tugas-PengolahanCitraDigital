import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ====================================
# 1. BACA GAMBAR
# ====================================
img = mpimg.imread("trial.bmp")  # Baca gambar dari file

# Ukuran gambar asli (baris x kolom)
h, w = img.shape[0], img.shape[1]
print(f"Ukuran gambar asli: {w} x {h} (lebar x tinggi)")

# ====================================
# 2. TENTUKAN KOORDINAT CROPPING
# ====================================
# x = horizontal (kolom)
# y = vertikal (baris)
xL, yT = 50, 50    # titik kiri-atas area crop
xR, yB = 200, 200  # titik kanan-bawah area crop

# Hitung lebar (w') dan tinggi (h') hasil crop
w_prime = xR - xL
h_prime = yB - yT

print(f"Koordinat crop:")
print(f"  Titik kiri-atas (xL, yT) = ({xL}, {yT})")
print(f"  Titik kanan-bawah (xR, yB) = ({xR}, {yB})")
print(f"Ukuran crop (w' x h') = {w_prime} x {h_prime}")

# ====================================
# 3. PROSES CROPPING (SLICING ARRAY)
# ====================================
# Ambil sebagian array dari img berdasarkan batas koordinat
cropped = img[yT:yB, xL:xR]

# ====================================
# 4. VISUALISASI HASIL
# ====================================
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# ----- Gambar Asli -----
axs[0].imshow(img)
axs[0].set_title("Citra Asli (dengan area crop)")
axs[0].axis("off")

# Tambahkan kotak merah menunjukkan area crop
rect = plt.Rectangle((xL, yT), w_prime, h_prime, 
                     edgecolor="red", facecolor="none", lw=2)
axs[0].add_patch(rect)

# Tambahkan label titik koordinat
axs[0].text(xL, yT - 5, f"({xL},{yT})", color="yellow", fontsize=8, backgroundcolor="black")
axs[0].text(xR, yB + 10, f"({xR},{yB})", color="yellow", fontsize=8, backgroundcolor="black")

# ----- Gambar Hasil Crop -----
axs[1].imshow(cropped)
axs[1].set_title(f"Hasil Crop\nUkuran: {w_prime}x{h_prime}")
axs[1].axis("off")

plt.tight_layout()
plt.show()
