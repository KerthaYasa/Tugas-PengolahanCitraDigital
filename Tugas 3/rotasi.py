import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ======================
# BACA GAMBAR RGB
# ======================
def read_image(filename):
    img = mpimg.imread(filename)
    height, width = img.shape[0], img.shape[1]
    pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(list(img[y][x][:3]))  # ambil R,G,B
        pixels.append(row)
    return pixels, width, height

# ======================
# SIMPAN GAMBAR RGB
# ======================
def save_image(filename, pixels):
    plt.imsave(filename, pixels)

# ======================
# FUNGSI TRIGONOMETRI TANPA math
# ======================
def factorial(n):
    f = 1
    for i in range(1, n+1):
        f *= i
    return f

def cos(x, terms=10):
    result = 0
    for n in range(terms):
        result += ((-1)**n) * (x**(2*n)) / factorial(2*n)
    return result

def sin(x, terms=10):
    result = 0
    for n in range(terms):
        result += ((-1)**n) * (x**(2*n + 1)) / factorial(2*n + 1)
    return result

def radians(deg):
    return deg * 3.141592653589793 / 180

# ======================
# ROTASI 90° CW
# ======================
def rotate_90(pixels):
    h = len(pixels)
    w = len(pixels[0])
    new_pixels = [[ [0,0,0] for _ in range(h)] for _ in range(w)]
    for y in range(h):
        for x in range(w):
            new_x = h - 1 - y
            new_y = x
            new_pixels[new_y][new_x] = pixels[y][x]
    return new_pixels

# ======================
# ROTASI 180° CW
# ======================
def rotate_180(pixels):
    h = len(pixels)
    w = len(pixels[0])
    new_pixels = [[ [0,0,0] for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            new_x = w - 1 - x
            new_y = h - 1 - y
            new_pixels[new_y][new_x] = pixels[y][x]
    return new_pixels

# ======================
# ROTASI BEBAS CCW
# ======================
def rotate_free(pixels, theta_deg):
    theta = radians(theta_deg)
    cos_t = cos(theta)
    sin_t = sin(theta)

    h = len(pixels)
    w = len(pixels[0])
    new_w = int(abs(w*cos_t) + abs(h*sin_t))
    new_h = int(abs(w*sin_t) + abs(h*cos_t))

    # background putih
    new_pixels = [[[1,1,1] for _ in range(new_w)] for _ in range(new_h)]

    cx, cy = w // 2, h // 2
    ncx, ncy = new_w // 2, new_h // 2

    for y in range(new_h):
        for x in range(new_w):
            xt = x - ncx
            yt = y - ncy
            old_x = int(xt*cos_t + yt*sin_t + cx)
            old_y = int(-xt*sin_t + yt*cos_t + cy)
            if 0 <= old_x < w and 0 <= old_y < h:
                new_pixels[y][x] = pixels[old_y][old_x]
    return new_pixels

# ======================
# MAIN
# ======================
if __name__ == "__main__":
    input_file = "trial.bmp"
    pixels, width, height = read_image(input_file)

    rot90 = rotate_90(pixels)
    rot180 = rotate_180(pixels)
    rotfree = rotate_free(pixels, 25)  # contoh rotasi 25° CCW

    # tampilkan
    fig, axs = plt.subplots(1,4, figsize=(16,6))
    axs[0].imshow(pixels)
    axs[0].set_title("Asli")
    axs[0].axis("off")

    axs[1].imshow(rot90)
    axs[1].set_title("Rotasi 90° CW")
    axs[1].axis("off")

    axs[2].imshow(rot180)
    axs[2].set_title("Rotasi 180° CW")
    axs[2].axis("off")

    axs[3].imshow(rotfree)
    axs[3].set_title("Rotasi 25° CCW")
    axs[3].axis("off")

    plt.tight_layout()
    plt.show()

