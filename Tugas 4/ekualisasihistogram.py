import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ====================================
# 1. BACA GAMBAR
# ====================================
img = mpimg.imread("trial7.png")

# Jika float [0,1], ubah ke 0-255
if img.dtype == float or img[0][0][0] <= 1:
    img = (img * 255).astype(int)

# ====================================
# 2. KONVERSI KE GRAYSCALE
# ====================================
def rgb_to_grayscale(img):
    """Konversi RGB ke grayscale (weighted NTSC)"""
    tinggi = len(img)
    lebar = len(img[0])
    gray = []
    
    for y in range(tinggi):
        baris = []
        for x in range(lebar):
            Ri = int(img[y][x][0])
            Gi = int(img[y][x][1])
            Bi = int(img[y][x][2])
            Ko = int(0.299*Ri + 0.587*Gi + 0.144*Bi)
            Ko = max(0, min(255, Ko))
            baris.append(Ko)
        gray.append(baris)
    return gray

gray = rgb_to_grayscale(img)
h = len(gray)
w = len(gray[0])

# ====================================
# 3. HITUNG HISTOGRAM ASLI
# ====================================
def hitung_histogram(gambar):
    """Hitung histogram dari gambar grayscale"""
    hist = [0] * 256
    for baris in gambar:
        for piksel in baris:
            hist[piksel] += 1
    return hist

hist_asli = hitung_histogram(gray)

# ====================================
# 4. EKUALISASI HISTOGRAM
# ====================================
def ekualisasi_histogram(gambar, k=8):
    """
    Ekualisasi histogram sesuai rumus PDF halaman 23.

    Rumus:
    Ko = round((2^k - 1) * Ci / (h * w))

    Keterangan:
    Ci = distribusi kumulatif nilai keabuan ke-i
    k  = jumlah bit (8 bit = 256 warna)
    h  = tinggi citra
    w  = lebar citra
    """
    tinggi = len(gambar)
    lebar = len(gambar[0])

    # Hitung frekuensi
    frekuensi = [0] * 256
    for y in range(tinggi):
        for x in range(lebar):
            Ki = gambar[y][x]
            frekuensi[Ki] += 1

    # Distribusi kumulatif
    distribusi_kumulatif = [0] * 256
    distribusi_kumulatif[0] = frekuensi[0]
    for i in range(1, 256):
        distribusi_kumulatif[i] = distribusi_kumulatif[i-1] + frekuensi[i]

    # Lookup table
    lookup = []
    for i in range(256):
        Ci = distribusi_kumulatif[i]
        Ko = round(((2**k - 1) * Ci) / (tinggi * lebar))
        lookup.append(Ko)

    # Terapkan transformasi
    hasil = []
    for y in range(tinggi):
        baris = []
        for x in range(lebar):
            Ki = gambar[y][x]
            Ko = lookup[Ki]
            baris.append(Ko)
        hasil.append(baris)

    return hasil, lookup, distribusi_kumulatif

# Proses ekualisasi
gray_equalized, lookup_table, dist_kumulatif = ekualisasi_histogram(gray, k=8)

# Histogram hasil
hist_equalized = hitung_histogram(gray_equalized)

# ====================================
# 5. CETAK TABEL
# ====================================
print("=" * 70)
print("TABEL EKUALISASI HISTOGRAM (Sesuai PDF Halaman 23)")
print("=" * 70)
print(f"{'Ki':<5} {'Frekuensi':<12} {'Ci (Kumulatif)':<18} {'Ko (Hasil)':<12}")
print("-" * 70)

frekuensi_tabel = [0] * 256
for baris in gray:
    for piksel in baris:
        frekuensi_tabel[piksel] += 1

for i in range(256):
    if frekuensi_tabel[i] > 0:
        print(f"{i:<5} {frekuensi_tabel[i]:<12} {dist_kumulatif[i]:<18} {lookup_table[i]:<12}")

print("=" * 70)
print(f"Rumus: Ko = round((2^8 - 1) * Ci / ({h} * {w}))")
print(f"       Ko = round(255 * Ci / {h*w})")
print("=" * 70)

# ====================================
# 6. VISUALISASI
# ====================================
fig, axs = plt.subplots(2, 3, figsize=(15, 8))

axs[0, 0].imshow(img)
axs[0, 0].set_title("Citra Asli (RGB)")
axs[0, 0].axis("off")

axs[0, 1].imshow(gray, cmap="gray", vmin=0, vmax=255)
axs[0, 1].set_title("Citra Grayscale")
axs[0, 1].axis("off")

axs[0, 2].imshow(gray_equalized, cmap="gray", vmin=0, vmax=255)
axs[0, 2].set_title("Hasil Ekualisasi")
axs[0, 2].axis("off")

axs[1, 0].bar(range(256), hist_asli, width=1)
axs[1, 0].set_title("Histogram Asli")
axs[1, 0].set_xlim([0, 255])

axs[1, 1].plot(range(256), dist_kumulatif)
axs[1, 1].set_title("Distribusi Kumulatif")
axs[1, 1].set_xlim([0, 255])

axs[1, 2].bar(range(256), hist_equalized, width=1)
axs[1, 2].set_title("Histogram Setelah Ekualisasi")
axs[1, 2].set_xlim([0, 255])

plt.tight_layout()
plt.show()
