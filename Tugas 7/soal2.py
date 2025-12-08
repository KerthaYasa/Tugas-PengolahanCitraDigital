import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# =================================================================
# 1. FUNGSI BANTUAN
# =================================================================

def rgb_ke_grayscale(gambar):
    """ Mengubah citra warna ke grayscale """
    tinggi = len(gambar)
    lebar = len(gambar[0])
    img_gray = []
    for y in range(tinggi):
        baris = []
        for x in range(lebar):
            pixel = gambar[y][x]
            if hasattr(pixel, '__len__'):
                r, g, b = pixel[0], pixel[1], pixel[2]
                gray = (0.299 * r) + (0.587 * g) + (0.144 * b)
            else:
                gray = pixel
            baris.append(gray)
        img_gray.append(baris)
    return img_gray

def konvolusi(citra, mask):
    """ Melakukan operasi Konvolusi """
    tinggi = len(citra)
    lebar = len(citra[0])
    mask_size = len(mask)
    offset = mask_size // 2
    hasil = []
    
    for y in range(offset, tinggi - offset):
        baris_baru = []
        for x in range(offset, lebar - offset):
            total = 0
            for i in range(mask_size):
                for j in range(mask_size):
                    pixel_val = citra[y + i - offset][x + j - offset]
                    mask_val = mask[i][j]
                    total += pixel_val * mask_val
            if total < 0: total = 0
            if total > 1: total = 1
            baris_baru.append(total)
        hasil.append(baris_baru)
    return hasil

# === [BARU] FUNGSI MENGAMBIL NILAI DIAGONAL ===
def ekstrak_nilai_diagonal(gambar, nama_file="nilai_diagonal.txt"):
    """
    Mengambil nilai pixel yang dilalui garis diagonal (Kiri Bawah -> Kanan Atas)
    """
    tinggi = len(gambar)
    lebar = len(gambar[0])
    
    nilai_diagonal = []
    
    print(f"\n--- MENGEKSTRAK NILAI DIAGONAL ---")
    print(f"Dimensi: {lebar} x {tinggi}")
    
    # Loop dari kiri ke kanan (x = 0 sampai lebar-1)
    for x in range(lebar):
        
        # 1. Hitung posisi Y garis di kolom X ini
        # Rumus: y = Tinggi - (Gradient * x)
        y_float = tinggi - (tinggi / lebar) * x
        
        # 2. Konversi ke Integer (Koordinat Array)
        y_int = int(y_float)
        
        # 3. Koreksi jika y_int keluar batas (misal y=Tinggi, padahal max index=Tinggi-1)
        if y_int >= tinggi:
            y_int = tinggi - 1
        if y_int < 0:
            y_int = 0
            
        # 4. Ambil Nilai Pixel
        nilai = gambar[y_int][x]
        
        # Simpan data: (x, y, nilai)
        nilai_diagonal.append((x, y_int, nilai))

    # --- TAMPILKAN SAMPEL (5 Pertama & 5 Terakhir) ---
    print("\n[SAMPEL DATA] (Format: x, y -> nilai)")
    for i in range(5):
        d = nilai_diagonal[i]
        print(f"Pixel ({d[0]}, {d[1]}) -> {d[2]:.4f}")
    
    print("...") 
    
    for i in range(len(nilai_diagonal)-5, len(nilai_diagonal)):
        d = nilai_diagonal[i]
        print(f"Pixel ({d[0]}, {d[1]}) -> {d[2]:.4f}")

    # --- SIMPAN KE FILE ---
    try:
        with open(nama_file, "w") as f:
            f.write("X\tY\tNILAI\n")
            f.write("-" * 20 + "\n")
            for item in nilai_diagonal:
                f.write(f"{item[0]}\t{item[1]}\t{item[2]:.4f}\n")
        print(f"\nSUKSES: Seluruh data diagonal disimpan di '{nama_file}'")
    except Exception as e:
        print(f"Gagal menyimpan file: {e}")

# =================================================================
# 2. DEFINISI MASK SOBEL
# =================================================================
mask_sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
mask_sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

# =================================================================
# 3. PROGRAM UTAMA
# =================================================================

nama_file = 'C:/Users/Bintang/Downloads/trial5.png' 
try:
    img_asli = mpimg.imread(nama_file)
    img_list = img_asli.tolist()
except Exception as e:
    print(f"Error: {e}")
    exit()

print("Sedang memproses...")

# 1. Grayscale
img_gray = rgb_ke_grayscale(img_list)

# 2. Sobel (Deteksi Tepi)
tepi_x = konvolusi(img_gray, mask_sobel_x)
tepi_y = konvolusi(img_gray, mask_sobel_y)

img_sobel = []
for y in range(len(tepi_x)):
    baris = []
    for x in range(len(tepi_x[0])):
        val = abs(tepi_x[y][x]) + abs(tepi_y[y][x])
        if val > 1: val = 1
        baris.append(val)
    img_sobel.append(baris)

# 3. Ekstrak Nilai Diagonal dari Gambar SOBEL
ekstrak_nilai_diagonal(img_sobel, "data_diagonal_sobel.txt")

# =================================================================
# 4. TAMPILKAN GAMBAR UNTUK KONFIRMASI VISUAL
# =================================================================
plt.figure(figsize=(8, 6))
plt.imshow(img_sobel, cmap='gray')
plt.title("Gambar Sobel (Data Diagonal Diambil dari Sini)")
plt.axis('off')

# Opsional: Gambar garis merah tipis untuk menunjukkan jalur yang diambil
# plt.plot([0, len(img_sobel[0])], [len(img_sobel), 0], color='red', linewidth=1)

plt.show()