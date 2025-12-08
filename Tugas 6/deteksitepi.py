import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# =================================================================
# 1. FUNGSI BANTUAN (UTILITIES)
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
            # Cek format pixel (RGB atau Grayscale)
            if hasattr(pixel, '__len__'):
                r, g, b = pixel[0], pixel[1], pixel[2]
                # Rumus Luminance NTSC
                gray = (0.299 * r) + (0.587 * g) + (0.144 * b)
            else:
                gray = pixel
            baris.append(gray)
        img_gray.append(baris)
    return img_gray

def konvolusi(citra, mask):
    """ Melakukan operasi Konvolusi (untuk Sobel, dll) """
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
            
            # Clipping nilai agar tetap di rentang 0-1
            if total < 0: total = 0
            if total > 1: total = 1
            baris_baru.append(total)
        hasil.append(baris_baru)
    return hasil

# === FUNGSI UTAMA: POTONG DIAGONAL & CARI TITIK TENGAH ===
def potong_diagonal(gambar):
    """
    Memisahkan gambar, mencari titik tengah, dan mengembalikan koordinatnya.
    """
    tinggi = len(gambar)
    lebar = len(gambar[0])
    
    # 1. Hitung Titik Tengah (Integer Division)
    mid_x = lebar // 2
    mid_y = tinggi // 2
    
    # 2. Siapkan Pixel Hitam untuk Background
    contoh_pixel = gambar[0][0]
    if hasattr(contoh_pixel, '__len__'): 
        pixel_hitam = [0.0] * len(contoh_pixel)
    else:
        pixel_hitam = 0.0

    segitiga_atas = []
    segitiga_bawah = []
    
    # 3. Proses Pemotongan (Looping Pixel)
    for y in range(tinggi):
        baris_atas = []
        baris_bawah = []
        for x in range(lebar):
            
            # Rumus Garis Diagonal (Kiri Bawah -> Kanan Atas)
            batas_y = tinggi - (tinggi / lebar) * x
            
            if y < batas_y:
                baris_atas.append(gambar[y][x])
                baris_bawah.append(pixel_hitam)
            else:
                baris_atas.append(pixel_hitam)
                baris_bawah.append(gambar[y][x])
                
        segitiga_atas.append(baris_atas)
        segitiga_bawah.append(baris_bawah)
        
    return segitiga_atas, segitiga_bawah, (mid_x, mid_y)

# =================================================================
# 2. DEFINISI MASK SOBEL
# =================================================================
mask_sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
mask_sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

# =================================================================
# 3. PROGRAM UTAMA (EKSEKUSI)
# =================================================================

nama_file = 'C:/Users/Bintang/Downloads/trial5.png' 
try:
    img_asli = mpimg.imread(nama_file)
    img_list = img_asli.tolist()
except Exception as e:
    print(f"Error: {e}")
    exit()

print("Sedang memproses gambar...")

# 1. Ubah ke Grayscale
img_gray = rgb_ke_grayscale(img_list)

# 2. Proses Deteksi Tepi (Sobel)
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

# 3. Potong Diagonal & Dapatkan Koordinat Tengah
sobel_atas, sobel_bawah, titik_tengah = potong_diagonal(img_sobel)
mid_x, mid_y = titik_tengah

# 4. AMBIL NILAI PIXEL DI TITIK TENGAH
# Pastikan koordinat aman (tidak di luar batas array)
if 0 <= mid_y < len(img_sobel) and 0 <= mid_x < len(img_sobel[0]):
    nilai_pixel_tengah = img_sobel[mid_y][mid_x]
else:
    nilai_pixel_tengah = 0.0 # Default jika error

# 5. TAMPILKAN INFORMASI DI TERMINAL
print("\n" + "="*50)
print("      INFO TITIK TENGAH & NILAI WARNA")
print("="*50)
print(f"Ukuran Gambar : {len(img_sobel[0])} x {len(img_sobel)}")
print(f"Koordinat Tengah : x = {mid_x}, y = {mid_y}")
print("-" * 50)
print(f"NILAI INTENSITAS (WARNA) DI TITIK TENGAH : {nilai_pixel_tengah:.4f}")
print("(Rentang nilai: 0.0 = Hitam Gelap, 1.0 = Putih Terang)")
print("="*50 + "\n")

# =================================================================
# 4. VISUALISASI GAMBAR
# =================================================================
plt.figure(figsize=(14, 8))

# Gambar Asli
plt.subplot(2, 3, 1)
plt.imshow(img_list)
plt.title("Asli")
plt.axis('off')

# Sobel Utuh + Titik Merah
plt.subplot(2, 3, 4)
plt.imshow(img_sobel, cmap='gray')
plt.title(f"Sobel & Titik ({mid_x},{mid_y})")
plt.plot(mid_x, mid_y, 'ro', markersize=10, label='Center') # Plot Titik Merah
plt.axis('off')

# Potongan Atas
plt.subplot(2, 3, 2)
plt.imshow(sobel_atas, cmap='gray')
plt.title("Sobel Atas")
plt.axis('off')

# Potongan Bawah
plt.subplot(2, 3, 5)
plt.imshow(sobel_bawah, cmap='gray')
plt.title("Sobel Bawah")
plt.axis('off')

plt.tight_layout()
plt.show()