import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ===============================
# 1. BACA GAMBAR
# ===============================
nama_file = "trial.bmp"
img = mpimg.imread(nama_file)

# Jika float [0,1], ubah ke 0-255
if img[0][0][0] <= 1:
    tinggi = len(img)
    lebar = len(img[0])
    for y in range(tinggi):
        for x in range(lebar):
            img[y][x] = [int(channel*255) for channel in img[y][x]]

# ===============================
# 2. KONVERSI GRAYSCALE (SESUAI PDF)
# ===============================
def rgb_to_grayscale(img, method="weighted"):
    """
    Konversi RGB ke grayscale sesuai PDF halaman 15
    method="average": (Ri + Gi + Bi)/3
    method="weighted": 0.299*Ri + 0.587*Gi + 0.144*Bi (SESUAI PDF)
    """
    tinggi = len(img)
    lebar = len(img[0])
    gray = []

    for y in range(tinggi):
        baris = []
        for x in range(lebar):
            pixel = img[y][x]
            Ri, Gi, Bi = pixel[:3]
            
            if method == "average":
                # Rumus PDF: Ko = (Ri + Gi + Bi) / 3
                Ko = int((Ri + Gi + Bi) / 3)
            elif method == "weighted":
                # Rumus PDF: Ko = 0.299*Ri + 0.587*Gi + 0.144*Bi
                Ko = int(0.299*Ri + 0.587*Gi + 0.144*Bi)
            else:
                raise ValueError("Pilih method 'average' atau 'weighted'")
            
            baris.append(Ko)
        gray.append(baris)
    return gray

# Konversi
gray_avg = rgb_to_grayscale(img, method="average")
gray_weighted = rgb_to_grayscale(img, method="weighted")

# ===============================
# 3. HITUNG HISTOGRAM
# ===============================
def hitung_histogram(gambar):
    hist = [0]*256
    for baris in gambar:
        for piksel in baris:
            hist[piksel] += 1
    return hist

# Histogram RGB
hist_r = [0]*256
hist_g = [0]*256
hist_b = [0]*256
tinggi = len(img)
lebar = len(img[0])
for y in range(tinggi):
    for x in range(lebar):
        r, g, b = img[y][x][:3]
        hist_r[r] += 1
        hist_g[g] += 1
        hist_b[b] += 1

hist_avg = hitung_histogram(gray_avg)
hist_weighted = hitung_histogram(gray_weighted)

# ===============================
# 4. TAMPILKAN HASIL
# ===============================
fig, axs = plt.subplots(2,3, figsize=(12,6))

# Citra asli
axs[0,0].imshow(img)
axs[0,0].set_title("Citra Asli")
axs[0,0].axis("off")

# Grayscale Average
axs[0,1].imshow(gray_avg, cmap="gray", vmin=0, vmax=255)
axs[0,1].set_title("Grayscale Average")
axs[0,1].axis("off")

# Grayscale Weighted
axs[0,2].imshow(gray_weighted, cmap="gray", vmin=0, vmax=255)
axs[0,2].set_title("Grayscale Weighted (PDF)")
axs[0,2].axis("off")

# Histogram RGB
axs[1,0].bar(range(256), hist_r, color='r', alpha=0.5)
axs[1,0].bar(range(256), hist_g, color='g', alpha=0.5)
axs[1,0].bar(range(256), hist_b, color='b', alpha=0.5)
axs[1,0].set_title("Histogram RGB")

# Histogram Average
axs[1,1].bar(range(256), hist_avg, color='gray')
axs[1,1].set_title("Histogram Grayscale Average")

# Histogram Weighted
axs[1,2].bar(range(256), hist_weighted, color='gray')
axs[1,2].set_title("Histogram Grayscale Weighted")

plt.tight_layout()
plt.show()