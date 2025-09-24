# TULIS BMP GRAYSCALE 8-BIT
# ================================
def write_bmp_numpy(filename, pixels):
    img = Image.fromarray(pixels.astype(np.uint8), mode="L")
    img.save(filename)