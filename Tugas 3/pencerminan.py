import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Baca citra
img = mpimg.imread(r"Tugas 3\trial.bmp")
  # ganti dengan nama file kamu

h, w = img.shape[0], img.shape[1]

# Buat array kosong untuk hasil
flip_h = np.zeros_like(img)   # horizontal
flip_v = np.zeros_like(img)   # vertical
flip_hv = np.zeros_like(img)  # kombinasi

for y in range(h):
    for x in range(w):
        # rumus dari gambar
        x_h = w - 1 - x
        y_h = y
        flip_h[y_h, x_h] = img[y, x]

        x_v = x
        y_v = h - 1 - y
        flip_v[y_v, x_v] = img[y, x]

        x_hv = w - 1 - x
        y_hv = h - 1 - y
        flip_hv[y_hv, x_hv] = img[y, x]

# Tampilkan hasil
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