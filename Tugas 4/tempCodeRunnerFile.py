import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ====== File gambar ======
try:
    imgA = mpimg.imread('trial5.png')
    imgB = mpimg.imread('trial6.png')
except FileNotFoundError:
    print("❌ File gambar tidak ditemukan!")
    raise SystemExit

# Samakan ukuran
height = min(len(imgA), len(imgB))
width = min(len(imgA[0]), len(imgB[0]))

# ====== Konversi ke grayscale ======
def to_gray(px):
    # Ambil RGB saja, abaikan alpha
    if hasattr(px, "__len__"):
        n = min(3, len(px))
        gray = sum(float(px[i]) for i in range(n)) / n
    else:
        gray = float(px)
    # Normalisasi jika masih 0–255
    if gray > 1:
        gray = gray / 255.0
    return gray

# ====== Binarisasi manual (tegas) ======
def binarize(img, h, w, threshold=0.75, invert=False):
    hasil = []
    for y in range(h):
        row = []
        for x in range(w):
            g = to_gray(img[y][x])
            bit = 1 if g < threshold else 0  # objek gelap jadi putih
            if invert:
                bit = 1 - bit
            row.append(bit)
        hasil.append(row)
    return hasil

# Uji beberapa ambang (0.7–0.8 biasanya bagus)
A_bin = binarize(imgA, height, width, threshold=0.75)
B_bin = binarize(imgB, height, width, threshold=0.75)

# ====== Operasi logika ======
def logic_and(a, b): return 1 if a == 1 and b == 1 else 0
def logic_or(a, b): return 1 if a == 1 or b == 1 else 0
def logic_xor(a, b): return 1 if a != b else 0
def logic_sub(a, b): return a - b if a >= b else 0

hasil_and, hasil_or, hasil_xor, hasil_sub = [], [], [], []

for y in range(height):
    row_and, row_or, row_xor, row_sub = [], [], [], []
    for x in range(width):
        a = A_bin[y][x]
        b = B_bin[y][x]
        row_and.append([logic_and(a, b)] * 3)
        row_or.append([logic_or(a, b)] * 3)
        row_xor.append([logic_xor(a, b)] * 3)
        row_sub.append([logic_sub(a, b)] * 3)
    hasil_and.append(row_and)
    hasil_or.append(row_or)
    hasil_xor.append(row_xor)
    hasil_sub.append(row_sub)

# ====== Visualisasi ======
fig, axes = plt.subplots(2, 3, figsize=(11, 7))
axes = axes.ravel()

axes[0].imshow(imgA, cmap='gray')
axes[0].set_title('Citra A (asli)')
axes[1].imshow(imgB, cmap='gray')
axes[1].set_title('Citra B (asli)')
axes[2].imshow(hasil_and, cmap='gray', vmin=0, vmax=1)
axes[2].set_title('A AND B')
axes[3].imshow(hasil_or, cmap='gray', vmin=0, vmax=1)
axes[3].set_title('A OR B')
axes[4].imshow(hasil_xor, cmap='gray', vmin=0, vmax=1)
axes[4].set_title('A XOR B')
axes[5].imshow(hasil_sub, cmap='gray', vmin=0, vmax=1)
axes[5].set_title('A SUB B')

for ax in axes:
    ax.axis('off')

plt.tight_layout()
plt.show()