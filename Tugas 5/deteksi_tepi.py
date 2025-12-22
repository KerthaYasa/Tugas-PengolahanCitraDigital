# deteksi_tepi_png_sobel.py
# Input: PNG (bitdepth 8, non-interlaced), tanpa PIL/OpenCV/NumPy.
# Hanya matplotlib untuk menampilkan gambar.
# Metode deteksi tepi: Sobel (sesuai permintaan).
#
# Penulis: disesuaikan untuk tugas Anda. Semua komentar dalam Bahasa Indonesia.

import sys
import zlib
import struct
import math
import matplotlib.pyplot as plt

# -----------------------------------------
# --- BAGIAN A: Pembaca PNG sederhana ---
# -----------------------------------------
# Mendukung: bitdepth=8, color_type 0 (grayscale), 2 (RGB), 6 (RGBA), no interlace.
# Jika file tidak memenuhi, akan raise ValueError.

def paeth_predict(a, b, c):
    # a = left, b = above, c = upper-left
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    else:
        return c

def unfilter_scanlines(raw, width, bpp):
    """
    raw: bytes hasil decompress (concatenated scanlines, tiap scanline diawali 1 byte filter)
    width: lebar piksel
    bpp: bytes per pixel (untuk filter Sub/Avg/Paeth)
    Mengembalikan daftar scanline tanpa byte filter.
    """
    stride = width * bpp
    pos = 0
    recon = []
    prev = bytearray(stride)
    while pos < len(raw):
        filter_type = raw[pos]
        pos += 1
        scan = bytearray(raw[pos:pos+stride])
        pos += stride
        if filter_type == 0:  # None
            cur = scan
        elif filter_type == 1:  # Sub
            cur = bytearray(stride)
            for i in range(stride):
                left = cur[i - bpp] if i >= bpp else 0
                cur[i] = (scan[i] + left) & 0xFF
        elif filter_type == 2:  # Up
            cur = bytearray(stride)
            for i in range(stride):
                up = prev[i]
                cur[i] = (scan[i] + up) & 0xFF
        elif filter_type == 3:  # Average
            cur = bytearray(stride)
            for i in range(stride):
                left = cur[i - bpp] if i >= bpp else 0
                up = prev[i]
                cur[i] = (scan[i] + ((left + up)//2)) & 0xFF
        elif filter_type == 4:  # Paeth
            cur = bytearray(stride)
            for i in range(stride):
                left = cur[i - bpp] if i >= bpp else 0
                up = prev[i]
                up_left = prev[i - bpp] if i >= bpp else 0
                cur[i] = (scan[i] + paeth_predict(left, up, up_left)) & 0xFF
        else:
            raise ValueError(f"Filter PNG tidak dikenal: {filter_type}")
        recon.append(bytes(cur))
        prev = cur
    return recon

def read_png_grayscale(path):
    """
    Baca PNG (pure Python) dan kembalikan citra grayscale sebagai list of lists integer 0..255.
    Membaca color types 0,2,6 dengan bitdepth 8; non-interlaced.
    """
    with open(path, 'rb') as f:
        sig = f.read(8)
        if sig != b'\x89PNG\r\n\x1a\n':
            raise ValueError("Bukan file PNG yang valid.")
        chunks = []
        width = height = None
        bitdepth = None
        color_type = None
        compression = None
        filter_method = None
        interlace = None
        idat_data = bytearray()
        while True:
            length_bytes = f.read(4)
            if not length_bytes:
                break
            length = struct.unpack(">I", length_bytes)[0]
            chunk_type = f.read(4)
            data = f.read(length)
            crc = f.read(4)
            if chunk_type == b'IHDR':
                width, height, bitdepth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", data)
            elif chunk_type == b'IDAT':
                idat_data.extend(data)
            elif chunk_type == b'IEND':
                break
            # else: ignore other chunks
        if bitdepth != 8:
            raise ValueError("PNG harus bitdepth 8 (skrip ini hanya mendukung 8-bit).")
        if interlace != 0:
            raise ValueError("Interlaced PNG tidak didukung oleh skrip ini.")
        # tentukan bytes per pixel (bpp)
        if color_type == 0:
            channels = 1
        elif color_type == 2:
            channels = 3
        elif color_type == 6:
            channels = 4
        else:
            raise ValueError(f"Color type {color_type} tidak didukung (hanya 0,2,6).")
        bpp = channels  # bytes per pixel untuk bitdepth=8
        # decompress
        raw = zlib.decompress(bytes(idat_data))
        # unfilter scanlines
        scanlines = unfilter_scanlines(raw, width, bpp)
        # build image; tiap scanline adalah width*bpp bytes
        img = []
        for row_bytes in scanlines:
            row = []
            # jika grayscale
            if channels == 1:
                for x in range(width):
                    row.append(row_bytes[x])
            elif channels == 3 or channels == 4:
                for x in range(width):
                    r = row_bytes[x*bpp]
                    g = row_bytes[x*bpp+1]
                    b = row_bytes[x*bpp+2]
                    if channels == 4:
                        a = row_bytes[x*bpp+3]
                        # pre-multiply alpha ke warna (simple composite di atas latar hitam)
                        alpha = a / 255.0
                        r = int(round(r * alpha))
                        g = int(round(g * alpha))
                        b = int(round(b * alpha))
                    # konversi ke grayscale luminance
                    y = int(round(0.299*r + 0.587*g + 0.114*b))
                    row.append(y)
            img.append(row)
        return img

# -----------------------------------------
# --- BAGIAN B: Konvolusi & Sobel (sebelumnya) ---
# -----------------------------------------
def konvolusi_3x3(img, kernel):
    h = len(img)
    w = len(img[0])
    hasil = [[0]*w for _ in range(h)]
    for y in range(1, h-1):
        for x in range(1, w-1):
            s = 0
            for ky in range(3):
                for kx in range(3):
                    py = y + (ky-1)
                    px = x + (kx-1)
                    s += kernel[ky][kx] * img[py][px]
            hasil[y][x] = s
    return hasil

def get_sobel_kernels():
    Kx = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]
    Ky = [
        [-1,-2,-1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ]
    return Kx, Ky

def combine_K(K1_img, K2_img, mode='mag'):
    h = len(K1_img)
    w = len(K1_img[0])
    out = [[0]*w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            a = int(round(K1_img[y][x]))
            b = int(round(K2_img[y][x]))
            if mode == 'sum':
                v = abs(a) + abs(b)
            elif mode == 'max':
                v = max(abs(a), abs(b))
            elif mode == 'avg':
                v = (abs(a) + abs(b)) // 2
            elif mode == 'mag':
                v = int(round(math.sqrt(a*a + b*b)))
            else:
                raise ValueError("Mode gabungan tidak dikenal")
            out[y][x] = v
    return out

def normalize_to_0_255(img):
    h = len(img)
    w = len(img[0])
    maxv = max(max(row) for row in img) if h>0 and w>0 else 1
    if maxv == 0:
        return img
    if maxv <= 255:
        # clip negatives and ensure int
        for y in range(h):
            for x in range(w):
                v = int(round(img[y][x]))
                img[y][x] = 0 if v<0 else v
        return img
    faktor = 255.0 / maxv
    for y in range(h):
        for x in range(w):
            v = int(round(img[y][x] * faktor))
            if v < 0: v = 0
            if v > 255: v = 255
            img[y][x] = v
    return img

# -----------------------------------------
# --- BAGIAN C: Potong diagonal dan util ---
# -----------------------------------------
def potong_diagonal(img, arah='utama'):
    h = len(img)
    w = len(img[0])
    out = [[0]*w for _ in range(h)]
    if arah == 'utama':
        ujung1 = img[0][0]
        ujung2 = img[h-1][w-1]
        for i in range(min(h,w)):
            out[i][i] = img[i][i]
        print(f"[INFO] Diagonal utama: nilai pojok atas-kiri (0,0) = {ujung1}, pojok bawah-kanan ({h-1},{w-1}) = {ujung2}")
        return out, (ujung1, ujung2)
    elif arah == 'sekunder':
        ujung1 = img[0][w-1]
        ujung2 = img[h-1][0]
        for i in range(min(h,w)):
            out[i][w-1-i] = img[i][w-1-i]
        print(f"[INFO] Diagonal sekunder: nilai pojok atas-kanan (0,{w-1}) = {ujung1}, pojok bawah-kiri ({h-1},0) = {ujung2}")
        return out, (ujung1, ujung2)
    else:
        raise ValueError("arah harus 'utama' atau 'sekunder'")

def tampilkan(img, judul=''):
    plt.figure(figsize=(6,6))
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.title(judul)
    plt.axis('off')
    plt.show()

# -----------------------------------------
# --- BAGIAN UTAMA: pipeline Sobel untuk PNG ---
# -----------------------------------------
def main(path):
    # 1) Baca PNG -> grayscale list-of-lists
    if path.lower().endswith('.png'):
        print("[INFO] Mendeteksi ekstensi .png — menggunakan pembaca PNG internal.")
        img = read_png_grayscale(path)
    else:
        raise ValueError("Input harus file PNG dengan ekstensi .png untuk skrip ini.")
    h = len(img); w = len(img[0])
    print(f"[INFO] Ukuran citra: {w} x {h}")

    # tampilkan citra asli
    tampilkan(img, "Citra Asli (grayscale dari PNG)")

    # 2) Sobel
    Kx, Ky = get_sobel_kernels()
    gx = konvolusi_3x3(img, Kx)
    gy = konvolusi_3x3(img, Ky)
    # sesuai permintaan: pakai Sobel → gabungkan magnitude (rumus umum di PDF)
    sobel_mag = combine_K(gx, gy, mode='mag')
    sobel_norm = normalize_to_0_255(sobel_mag)

    tampilkan(sobel_norm, "Hasil Deteksi Tepi: Sobel (magnitude)")

    # 3) Potong diagonal utama & sekunder, cetak pojok
    diag1, pojok1 = potong_diagonal(sobel_norm, arah='utama')
    tampilkan(diag1, "Potongan Diagonal Utama (hanya diagonal)")
    diag2, pojok2 = potong_diagonal(sobel_norm, arah='sekunder')
    tampilkan(diag2, "Potongan Diagonal Sekunder (hanya diagonal)")

    print("Nilai pojok diagonal utama (atas-kiri, bawah-kanan):", pojok1)
    print("Nilai pojok diagonal sekunder (atas-kanan, bawah-kiri):", pojok2)

# -----------------------------------------
# --- Eksekusi jika dipanggil dari CLI ---
# -----------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: deteksi_tepi.py gambar.png")
        sys.exit(1)
    path = sys.argv[1]
    try:
        main(path)
    except Exception as e:
        print("ERROR:", e)
        print("Catatan: skrip ini mendukung PNG 8-bit non-interlaced (grayscale, RGB, RGBA).")
        sys.exit(1)
