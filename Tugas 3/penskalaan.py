from PIL import Image

# ======================
# BACA GAMBAR
# ======================
def read_image(filename):
    """
    Membaca gambar RGB dan mengubah ke list 2D of tuple (R,G,B).
    """
    img = Image.open(filename)  # biarkan tetap warna
    w, h = img.size
    pixels = list(img.getdata())
    pixels_2d = [pixels[i * w:(i + 1) * w] for i in range(h)]
    return pixels_2d, w, h

# ======================
# SIMPAN GAMBAR
# ======================
def save_image(filename, pixels_2d):
    """
    Menyimpan list 2D RGB menjadi file gambar warna.
    """
    h = len(pixels_2d)
    w = len(pixels_2d[0])
    flat_pixels = [val for row in pixels_2d for val in row]

    # Mode RGB karena data-nya tuple (r, g, b)
    img = Image.new("RGB", (w, h))
    img.putdata(flat_pixels)
    img.save(filename)

# ======================
# FUNGSI PENSKALAAN
# ======================
def scale_image(pixels_2d, Sh, Sv):
    """
    Scaling gambar warna RGB tanpa numpy.
    Rumus:
        x' = Sh * x
        y' = Sv * y
    """
    h = len(pixels_2d)
    w = len(pixels_2d[0])
    new_w = int(w * Sh)
    new_h = int(h * Sv)

    new_pixels = [[(0, 0, 0) for _ in range(new_w)] for _ in range(new_h)]

    for y in range(new_h):
        for x in range(new_w):
            old_x = int(x / Sh)
            old_y = int(y / Sv)

            if old_x >= w:
                old_x = w - 1
            if old_y >= h:
                old_y = h - 1

            new_pixels[y][x] = pixels_2d[old_y][old_x]

    return new_pixels

# ======================
# MAIN PROGRAM
# ======================
if __name__ == "__main__":
    input_file = "trial.bmp"
    pixels, w, h = read_image(input_file)

    scaled_up = scale_image(pixels, Sh=1, Sv=2)
    scaled_down = scale_image(pixels, Sh=0.5, Sv=0.2)

    save_image("scaled_up_trial.bmp", scaled_up)
    save_image("scaled_down_trial.bmp", scaled_down)

    print("Penskalaan selesai")
