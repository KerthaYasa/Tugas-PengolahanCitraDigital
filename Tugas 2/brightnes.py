import matplotlib.pyplot as plt

def batas_nilai(nilai):
    """Batasi nilai 0-255"""
    if nilai < 0:
        return 0
    elif nilai > 255:
        return 255
    else:
        return int(nilai)

def konversi_ke_grayscale(gambar):
    """Konversi RGB ke grayscale"""
    if len(gambar.shape) == 2:
        return gambar.tolist()

    tinggi, lebar, _ = gambar.shape
    hasil = []
    
    for y in range(tinggi):
        baris = []
        for x in range(lebar):
            r, g, b = gambar[y][x][:3]
            
            if r <= 1 and g <= 1 and b <= 1:
                r, g, b = r * 255, g * 255, b * 255
            
            # Rumus PDF: Ko = 0.299*R + 0.587*G + 0.114*B
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            baris.append(gray)
        hasil.append(baris)
    return hasil

def tambah_brightness(gambar, C):
    """
    Rumus PDF: Ko = Ki + C
    """
    tinggi = len(gambar)
    lebar = len(gambar[0])
    hasil = []

    for y in range(tinggi):
        baris = []
        for x in range(lebar):
            Ki = gambar[y][x]
            Ko = Ki + C  # Rumus PDF
            Ko = batas_nilai(Ko)
            baris.append(Ko)
        hasil.append(baris)
    return hasil

def hitung_histogram(gambar):
    histogram = [0] * 256
    for baris in gambar:
        for piksel in baris:
            histogram[int(piksel)] += 1
    return histogram

def tampilkan_hasil(gambar_asli, gambar_baru, hist_asli, hist_baru, C):
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 2, 1)
    plt.imshow(gambar_asli, cmap="gray", vmin=0, vmax=255)
    plt.title("Gambar Asli")
    plt.axis("off")

    plt.subplot(2, 2, 2)
    plt.imshow(gambar_baru, cmap="gray", vmin=0, vmax=255)
    plt.title(f"Brightness (C = {C})")
    plt.axis("off")

    plt.subplot(2, 2, 3)
    plt.bar(range(256), hist_asli, color="gray")
    plt.title("Histogram Asli")

    plt.subplot(2, 2, 4)
    plt.bar(range(256), hist_baru, color="gray")
    plt.title("Histogram Hasil")

    plt.tight_layout()
    plt.show()

# Program utama
def main():
    # Baca gambar
    nama_file = "kucing8x8.bmp"
    gambar_asli_rgb = plt.imread(nama_file)

    # Ubah ke grayscale
    gambar_asli = konversi_ke_grayscale(gambar_asli_rgb)

    # Input nilai C
    try:
        C = int(input("Masukkan nilai C (+terang / -gelap): "))
    except:
        C = 50
        print("Input tidak valid, pakai C = 50")

    # Rumus: Ko = Ki + C
    gambar_baru = tambah_brightness(gambar_asli, C)

    # Histogram
    hist_asli = hitung_histogram(gambar_asli)
    hist_baru = hitung_histogram(gambar_baru)

    # Tampilkan
    tampilkan_hasil(gambar_asli, gambar_baru, hist_asli, hist_baru, C)

    # Cetak matriks
    print("\n=== Matriks Asli (Ki) ===")
    for baris in gambar_asli:
        print(baris)

    print(f"\n=== Matriks Hasil (Ko = Ki + {C}) ===")
    for baris in gambar_baru:
        print(baris)

if __name__ == "__main__":
    main()