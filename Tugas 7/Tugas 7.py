import matplotlib.pyplot as plt
import matplotlib.image as mpimg

print("=== MULAI PROSES ===")

# 1. BACA GAMBAR
img = mpimg.imread('trial3.jpg')
tinggi = img.shape[0]
lebar = img.shape[1]

print(f"Gambar dimuat: {lebar}x{tinggi} pixel")
print("Mohon tunggu, sedang memproses pixel satu per satu...")

# 2. SIAPKAN WADAH KOSONG (CANVAS)
# Kita buat 3 kanvas hitam kosong
# Caranya: copy gambar asli, lalu hitamkan semua pixelnya manual
canvas_segitiga_atas = img.copy()
canvas_segitiga_bawah = img.copy()
canvas_hasil_akhir = img.copy()

# Kosongkan kanvas (isi dengan warna hitam [0,0,0])
for y in range(tinggi):
    for x in range(lebar):
        canvas_segitiga_atas[y, x] = [0, 0, 0]
        canvas_segitiga_bawah[y, x] = [0, 0, 0]
        canvas_hasil_akhir[y, x] = [0, 0, 0]


# ========================================================
# LANGKAH 1: MEMOTONG (MENGISI SEGITIGA)
# ========================================================
for y in range(tinggi):
    for x in range(lebar):
        
        # --- RUMUS DIAGONAL SEDERHANA ---
        # Bayangkan garis miring dari Kiri-Bawah ke Kanan-Atas
        nilai_posisi = (x / lebar) + (y / tinggi)
        
        if nilai_posisi < 1.0:
            # Ini wilayah SEGITIGA ATAS-KIRI
            canvas_segitiga_atas[y, x] = img[y, x]
        else:
            # Ini wilayah SEGITIGA BAWAH-KANAN
            canvas_segitiga_bawah[y, x] = img[y, x]


# ========================================================
# LANGKAH 2: MEMUTAR & MENGGABUNGKAN (ROTASI 180)
# ========================================================
for y in range(tinggi):
    for x in range(lebar):
        
        # --- RUMUS PUTAR/BALIK (ROTASI 180) ---
        # Rumus: (Total Panjang - 1) - Posisi Lama
        y_baru = (tinggi - 1) - y
        x_baru = (lebar - 1) - x
        
        # Cek Pixel di Segitiga Atas
        pixel_atas = canvas_segitiga_atas[y, x]
        if sum(pixel_atas) > 0: # Jika tidak hitam
            # Pindahkan ke posisi BARU di hasil akhir
            canvas_hasil_akhir[y_baru, x_baru] = pixel_atas
            
        # Cek Pixel di Segitiga Bawah
        pixel_bawah = canvas_segitiga_bawah[y, x]
        if sum(pixel_bawah) > 0: # Jika tidak hitam
            # Pindahkan ke posisi BARU di hasil akhir
            canvas_hasil_akhir[y_baru, x_baru] = pixel_bawah


# ========================================================
# LANGKAH 3: TAMPILKAN HASIL
# ========================================================
print("Selesai! Menampilkan gambar...")
plt.figure(figsize=(12, 8))

# Tampilkan Proses 1: Segitiga Atas
plt.subplot(2, 2, 1)
plt.title("Langkah 1: Potong Segitiga Atas")
plt.imshow(canvas_segitiga_atas)
plt.axis('off')

# Tampilkan Proses 2: Segitiga Bawah
plt.subplot(2, 2, 2)
plt.title("Langkah 1: Potong Segitiga Bawah")
plt.imshow(canvas_segitiga_bawah)
plt.axis('off')

# Tampilkan Hasil Akhir
plt.subplot(2, 1, 2)
plt.title("Langkah 2: Gabung & Putar (Rotasi 180)")
plt.imshow(canvas_hasil_akhir)
plt.axis('off')

plt.tight_layout()
plt.show()