import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ============================
# Baca citra
# ============================
img = mpimg.imread(r"Tugas 3\trial.bmp")  # ganti sesuai lokasi gambar

# Pastikan gambar dalam bentuk list of list
img = img.tolist()

# Tentukan tinggi (h) dan lebar (w)
h = len(img)
w = len(img[0])

# ============================
# Siapkan array kosong manual
# ============================
# Struktur: list of list yang meniru array 2D
flip_h  = [[None for _ in range(w)] for _ in range(h)]  # horizontal
flip_v  = [[None for _ in range(w)] for _ in range(h)]  # vertical
flip_hv = [[None for _ in range(w)] for _ in range(h)]  # kombinasi

# ============================
# Proses pencerminan manual
# ============================
for y in range(h):
    for x in range(w):
        # --- Horizontal ---
        x_h = w - 1 - x
        y_h = y
        flip_h[y_h][x_h] = img[y][x]

        # --- Vertikal ---
        x_v = x
        y_v = h - 1 - y
        flip_v[y_v][x_v] = img[y][x]

        # --- Kombinasi ---
        x_hv = w - 1 - x
        y_hv = h - 1 - y
        flip_hv[y_hv][x_hv] = img[y][x]

# ============================
# Tampilkan hasil
# ============================
fig, axs = plt.subplots(1, 4, figsize=(16, 6))

axs[0].imshow(img)
axs[0].set_title("Citra Asli")
axs[0].axis("off")

axs[1].imshow(flip_h)
axs[1].set_title("Pencerminan Horizontal")
axs[1].axis("off")

axs[2].imshow(flip_v)
axs[2].set_title("Pencerminan Vertikal")
axs[2].axis("off")

axs[3].imshow(flip_hv)
axs[3].set_title("Pencerminan Kombinasi")
axs[3].axis("off")

plt.show()
