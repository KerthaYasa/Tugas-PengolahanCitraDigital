import matplotlib.pyplot as plt

# =========================
# Fungsi bantu
# =========================
def batas_nilai(nilai):
    """Membatasi nilai piksel agar tetap antara 0 dan 255."""
    if nilai < 0:
        return 0
    elif nilai > 255:
        return 255
    else:
        return int(nilai)

def konversi_ke_grayscale(gambar):
    # Jika gambar sudah grayscale (2 dimensi)
    if len(gambar.shape) == 2:
        return gambar.tolist()

    tinggi, lebar, _ = gambar.shape
    hasil = []
    for y in range(tinggi):
        baris = []
        for x in range(lebar):
            r, g, b = gambar[y][x][:3]
            # Jika gambar dalam rentang 0–1 (float), ubah ke 0–255
            if r <= 1 and g <= 1 and b <= 1:
                gray = int((r + g + b) / 3 * 255)
            else:
                gray = int((r + g + b) / 3)
            baris.append(gray)
        hasil.append(baris)
    return hasil

def tambah_brightness(gambar, nilai_tambah):
    tinggi = len(gambar)
    lebar = len(gambar[0])
    hasil = []

    for y in range(tinggi):
        baris = []
        for x in range(lebar):
            nilai_baru = batas_nilai(gambar[y][x] + nilai_tambah)
            baris.append(nilai_baru)
        hasil.append(baris)
    return hasil

def hitung_histogram(gambar):
    histogram = [0] * 256
    for baris in gambar:
        for piksel in baris:
            histogram[int(piksel)] += 1
    return histogram

def tampilkan_hasil(gambar_asli, gambar_baru, hist_asli, hist_baru, nilai_tambah):
    plt.figure(figsize=(10, 6))

    # Gambar asli
    plt.subplot(2, 2, 1)
    plt.imshow(gambar_asli, cmap="gray", vmin=0, vmax=255)
    plt.title("Gambar Asli")
    plt.axis("off")

    # Gambar setelah ditambah brightness
    plt.subplot(2, 2, 2)
    plt.imshow(gambar_baru, cmap="gray", vmin=0, vmax=255)
    plt.title(f"Gambar + Brightness ({nilai_tambah})")
    plt.axis("off")

    # Histogram asli
    plt.subplot(2, 2, 3)
    plt.bar(range(256), hist_asli, color="gray")
    plt.title("Histogram Asli")

    # Histogram baru
    plt.subplot(2, 2, 4)
    plt.bar(range(256), hist_baru, color="gray")
    plt.title("Histogram Setelah Brightness")

    plt.tight_layout()
    plt.show()

# =========================
# Program utama
# =========================
def main():
    # 1. Baca gambar dari direktori lokal
    nama_file = "kucing8x8.bmp"
    gambar_asli_rgb = plt.imread(nama_file)

    # 2. Ubah ke grayscale
    gambar_asli = konversi_ke_grayscale(gambar_asli_rgb)

    # 3. Input nilai brightness dari pengguna
    try:
        nilai_tambah = int(input("Masukkan nilai brightness (+terang / -gelap): "))
    except:
        nilai_tambah = 50  # default jika input tidak valid
        print("Input tidak valid, gunakan nilai default +50")

    # 4. Tambah brightness
    gambar_baru = tambah_brightness(gambar_asli, nilai_tambah)

    # 5. Hitung histogram
    hist_asli = hitung_histogram(gambar_asli)
    hist_baru = hitung_histogram(gambar_baru)

    # 6. Tampilkan hasil visual
    tampilkan_hasil(gambar_asli, gambar_baru, hist_asli, hist_baru, nilai_tambah)

    # 7. Tampilkan matriks nilai piksel
    print("\n=== Matriks Nilai Piksel Sebelum (Ki) ===")
    for baris in gambar_asli:
        print(baris)

    print("\n=== Matriks Nilai Piksel Sesudah (Ko = Ki + C) ===")
    for baris in gambar_baru:
        print(baris)

if __name__ == "__main__":
    main()
