def read_bmp_info(kucing8x8):
    with open("Tugas 1/kucing8x8.bmp", "rb") as f:
        # Resolusi
        f.seek(18)
        width = int.from_bytes(f.read(4), "little")
        height = int.from_bytes(f.read(4), "little")

        # Kedalaman warna
        f.seek(28)
        bit_depth = int.from_bytes(f.read(2), "little")

        # Offset data piksel posisi awal data pixel
        f.seek(10)
        data_offset = int.from_bytes(f.read(4), "little")

        print(f"Resolusi: {width} x {height} piksel")
        print(f"Kedalaman warna: {bit_depth} bpp")

        if bit_depth != 24:
            raise ValueError("Kode ini hanya mendukung BMP 24-bit")

        # Hitung row dengan padding (harus kelipatan 4 byte)
        row_padded = (width * 3 + 3) & ~3

        # Pindah ke data pixel
        f.seek(data_offset)

        # Baca semua baris
        for y in range(height):
            row = f.read(row_padded)
            for x in range(width):
                b, g, r = row[x*3:x*3+3]
                # Karena BMP dari bawah ke atas:
                real_y = height - 1 - y
                print(f"f({x},{real_y}) = R:{r} G:{g} B:{b}")

# Contoh pemanggilan
read_bmp_info("kucing8x8.bmp")
