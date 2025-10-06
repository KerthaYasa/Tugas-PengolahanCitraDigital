import matplotlib.pyplot as plt

# =========================
# Fungsi bantu
# =========================
def batas_nilai(nilai):
    """Pastikan nilai tetap dalam rentang 0–255."""
    if nilai < 0:
        return 0
    elif nilai > 255:
        return 255
    else:
        return int(nilai)

def konversi_ke_grayscale(gambar):
    """Ubah gambar RGB menjadi grayscale tanpa numpy."""
    if len(gambar.shape) == 2:
        return gambar.tolist()

    tinggi, lebar, _ = gambar.shape
    hasil = []
    for y in range(tinggi):
        baris = []
        for x in range(lebar):
            r, g, b = gambar[y][x][:3]
            if r <= 1 and g <= 1 and b <= 1:
                gray = int((r + g + b) / 3 * 255)
            else:
                gray = int((r + g + b) / 3)
            baris.append(gray)
        hasil.append(baris)
    return hasil

def ubah_kontras(gambar, G, P):
    """Menerapkan rumus kontras: Ko = G * (Ki - P) + P"""
    tinggi = len(gambar)
    lebar = len(gambar[0])
    hasil = []

    for y in range(tinggi):
        baris = []
        for x in range(lebar):
            Ki = gambar[y][x]
            Ko = G * (Ki - P) + P
            Ko = batas_nilai(Ko)
            baris.append(Ko)
        hasil.append(baris)
    return hasil

def hitung_histogram(gambar):
    """Hitung frekuensi kemunculan tiap intensitas (0–255)."""
    histogram = [0] * 256
    for baris in gambar:
        for piksel in baris:
            histogram[int(piksel)] += 1
    return histogram

def tampilkan(gambar_asli, gambar_kontras, hist_asli, hist_kontras, G, P):
    """Tampilkan hasil gambar dan histogram."""
    plt.figure(figsize=(10, 6))

    # Gambar asli
    plt.subplot(2, 2, 1)
    plt.imshow(gambar_asli, cmap="gray", vmin=0, vmax=255)
    plt.title("Gambar Asli")
    plt.axis("off")

    # Gambar setelah kontras
    plt.subplot(2, 2, 2)
    plt.imshow(gambar_kontras, cmap="gray", vmin=0, vmax=255)
    plt.title(f"Setelah Kontras (G={G}, P={P})")
    plt.axis("off")

    # Histogram sebelum
    plt.subplot(2, 2, 3)
    plt.bar(range(256), hist_asli, color="gray")
    plt.title("Histogram Sebelum")

    # Histogram sesudah
    plt.subplot(2, 2, 4)
    plt.bar(range(256), hist_kontras, color="gray")
    plt.title("Histogram Sesudah")

    plt.tight_layout()
    plt.show()

# =========================
# Program utama
# =========================
def main():
    # 1. Baca gambar
    nama_file = "kucing8x8.bmp"
    gambar_rgb = plt.imread(nama_file)

    # 2. Konversi ke grayscale
    gambar_asli = konversi_ke_grayscale(gambar_rgb)

    # 3. Input nilai G dan P
    try:
        G = float(input("Masukkan koefisien kontras (G, contoh: 1.5): "))
    except:
        G = 1.5
        print("Input tidak valid, gunakan G=1.5")

    try:
        P = int(input("Masukkan pusat kontras (P, contoh: 128): "))
    except:
        P = 128
        print("Input tidak valid, gunakan P=128")

    # 4. Ubah kontras
    gambar_kontras = ubah_kontras(gambar_asli, G, P)

    # 5. Hitung histogram
    hist_asli = hitung_histogram(gambar_asli)
    hist_kontras = hitung_histogram(gambar_kontras)

    # 6. Tampilkan hasil visual
    tampilkan(gambar_asli, gambar_kontras, hist_asli, hist_kontras, G, P)

    # 7. Tampilkan matriks nilai
    print("\n=== Matriks Nilai Piksel Sebelum (Ki) ===")
    for baris in gambar_asli:
        print(baris)

    print(f"\n=== Matriks Nilai Piksel Sesudah (Ko = {G}(Ki - {P}) + {P}) ===")
    for baris in gambar_kontras:
        print(baris)

if __name__ == "__main__":
    main()
