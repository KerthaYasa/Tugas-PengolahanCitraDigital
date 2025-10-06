import numpy as np
from PIL import Image

# ======================
# BACA GAMBAR GRAYSCALE
# ======================
def read_image(filename):
    """
    Membaca file gambar dan mengubahnya menjadi array numpy grayscale.
    """
    img = Image.open(filename).convert("L")  # konversi ke grayscale
    return np.array(img, dtype=np.uint8)

# ======================
# SIMPAN GAMBAR
# ======================
def save_image(filename, pixels):
    """
    Menyimpan array numpy menjadi file gambar.
    """
    img = Image.fromarray(pixels.astype(np.uint8), mode="L")
    img.save(filename)

# ======================
# FUNGSI PENSKALAAN
# ======================
def scale_image(pixels, Sh, Sv):
    """
    Melakukan penskalaan (scaling) citra dengan faktor Sh (horizontal) dan Sv (vertical).
    Rumus:
        x' = Sh * x
        y' = Sv * y
    Ukuran baru:
        w' = Sh * w
        h' = Sv * h
    """
    h, w = pixels.shape
    new_w, new_h = int(w * Sh), int(h * Sv)

    new_pixels = np.zeros((new_h, new_w), dtype=np.uint8)

    for y in range(new_h):
        for x in range(new_w):
            old_x = min(int(x / Sh), w - 1)
            old_y = min(int(y / Sv), h - 1)
            new_pixels[y, x] = pixels[old_y, old_x]

    return new_pixels

# ======================
# MAIN PROGRAM
# ======================
if __name__ == "__main__":
    input_file = "Tugas 3/trial.bmp"   # ganti sesuai nama file
    pixels = read_image(input_file)

    # scaling
    scaled_up = scale_image(pixels, Sh=1, Sv=2)        # zoom in 2x
    scaled_down = scale_image(pixels, Sh=1, Sv=0.5)  # zoom out 0.5x

    # simpan hasil
    save_image("Tugas 3/scaled_up_trial.bmp", scaled_up)
    save_image("Tugas 3/scaled_down_trial.bmp", scaled_down)

    print("Penskalaan selesai. File hasil disimpan.")
