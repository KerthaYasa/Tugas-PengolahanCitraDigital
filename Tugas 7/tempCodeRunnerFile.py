import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ==========================================
# 1. PERSIAPAN
# ==========================================
nama_file = 'C:/Users/Bintang/Downloads/trial4.jpg' # Ganti sesuai path file kamu

img_data = mpimg.imread(nama_file)
img_list = img_data.tolist()

tinggi_asli = len(img_list)
lebar_asli  = len(img_list[0])
channel     = len(img_list[0][0])

# ==========================================
# 2. KONFIGURASI MANUAL
# ==========================================
GESER_KE_KANAN = 80 

# Deteksi background putih
nilai_putih_max = 1.0 if isinstance(img_list[0][0][0], float) else 255
batas_putih = nilai_putih_max - (0.1 if isinstance(nilai_putih_max, float) else 20)

# ==========================================
# 3. DETEKSI UKURAN GEDUNG (DIPERBARUI)
# ==========================================
# Area scan (Kiri-Atas)
batas_scan_y = tinggi_asli // 2
batas_scan_x = (lebar_asli // 2) - 5 

max_x_ditemukan = 0
max_y_ditemukan = 0

print("Sedang memindai pixel gambar...")

for y in range(batas_scan_y):
    for x in range(batas_scan_x):
        pixel = img_list[y][x]
        
        # Cek apakah pixel ini WARNA (Bukan putih background)
        is_colored = (pixel[0] < batas_putih) or (pixel[1] < batas_putih) or (pixel[2] < batas_putih)
        
        if is_colored:
            # Jika pixel berwarna, catat koordinat terjauhnya
            if y > max_y_ditemukan:
                max_y_ditemukan = y
            if x > max_x_ditemukan:
                max_x_ditemukan = x

# Hitung dimensi gedung
tinggi_gedung = max_y_ditemukan + 1
lebar_gedung  = max_x_ditemukan + 1

# --- BAGIAN INI YANG DITAMBAHKAN UNTUK MELIHAT HASIL DETEKSI ---
print("\n" + "="*40)
print("       HASIL DETEKSI PIXEL")
print("="*40)
print(f"1. Ukuran KANVAS (Total) : {lebar_asli} px (Lebar) x {tinggi_asli} px (Tinggi)")
print(f"2. Ukuran GEDUNG (Objek) : {lebar_gedung} px (Lebar) x {tinggi_gedung} px (Tinggi)")
print("="*40 + "\n")
# ---------------------------------------------------------------

# ==========================================
# 4. BUAT KANVAS PUTIH
# ==========================================
gambar_hasil = []
pixel_putih = [nilai_putih_max] * channel

for y in range(tinggi_asli):
    baris = []
    for x in range(lebar_asli):
        baris.append(pixel_putih)
    gambar_hasil.append(baris)

# ==========================================
# 5. PINDAHKAN LAUT (KE ATAS)
# ==========================================
tinggi_laut = tinggi_asli - batas_scan_y

for y in range(tinggi_laut):
    for x in range(lebar_asli):
        y_sumber = y + batas_scan_y
        if y_sumber < tinggi_asli:
            gambar_hasil[y][x] = img_list[y_sumber][x]

# ==========================================
# 6. PINDAHKAN KOTA 
# ==========================================
start_x = (lebar_asli - lebar_gedung) + GESER_KE_KANAN
start_y = tinggi_laut 

print(f"Menempel gedung di koordinat: ({start_x}, {start_y})")

for y in range(tinggi_gedung):
    for x in range(lebar_gedung):
        
        # Flip Vertikal (Bawah ke Atas)
        y_sumber_flip = (tinggi_gedung - 1) - y
        
        pixel = img_list[y_sumber_flip][x]
        
        y_tujuan = start_y + y
        x_tujuan = start_x + x
        
        if 0 <= y_tujuan < tinggi_asli and 0 <= x_tujuan < lebar_asli:
            gambar_hasil[y_tujuan][x_tujuan] = pixel

# ==========================================
# 7. TAMPILKAN
# ==========================================
plt.figure(figsize=(10, 8))

plt.subplot(2, 1, 1)
plt.title(f"Asli: {lebar_asli}x{tinggi_asli} px")
plt.imshow(img_list)
plt.axis('on') # Saya ubah jadi 'on' biar kelihatan angka koordinatnya

plt.subplot(2, 1, 2)
plt.title(f"Hasil: Gedung {lebar_gedung}x{tinggi_gedung} px")
plt.imshow(gambar_hasil)
plt.axis('off')

plt.tight_layout()
plt.show()