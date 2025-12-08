import matplotlib.pyplot as plt

# ============================================================
# HISTOGRAM EQUALIZATION (RUMUS BUKU)
# Ko = round( Ci / (h*w) * (2^k - 1) )
# ============================================================

# Data dari soal
data = [2, 4, 3, 1, 3, 6, 4, 3, 1, 0, 3, 2]

# ------------------------------------------------------------
# 1. Hitung histogram (tanpa library)
# ------------------------------------------------------------
hist = {}
for v in data:
    hist[v] = hist.get(v, 0) + 1

sorted_vals = sorted(hist.keys())
N = len(data)                  # total piksel
max_gray = max(sorted_vals)

# ------------------------------------------------------------
# 2. Tentukan k (jumlah bit) berdasarkan nilai maksimum 
#    dilakukan tanpa library
# ------------------------------------------------------------
k = 0
while (2 ** k) <= max_gray:
    k += 1

L_minus_1 = (2 ** k) - 1       # nilai keabuan maksimum

# ------------------------------------------------------------
# 3. Hitung distribusi kumulatif (CDF)
# ------------------------------------------------------------
cdf = {}
running = 0
for v in sorted_vals:
    running += hist[v]
    cdf[v] = running

# ------------------------------------------------------------
# 4. Hitung nilai Ko menggunakan rumus buku
# ------------------------------------------------------------
mapping = {}
for v in sorted_vals:
    Ci = cdf[v]
    Ko = round(Ci / N * L_minus_1)
    mapping[v] = Ko

# ------------------------------------------------------------
# 5. Buat data baru setelah ekualisasi
# ------------------------------------------------------------
equalized_data = [mapping[v] for v in data]

# ------------------------------------------------------------
# 6. Tampilkan histogram menggunakan matplotlib
# ------------------------------------------------------------
plt.figure(figsize=(12, 5))

# Histogram sebelum
plt.subplot(1, 2, 1)
plt.hist(data, bins=range(max_gray+2), edgecolor='black')
plt.title("Histogram Asli")
plt.xlabel("Nilai Keabuan")
plt.ylabel("Frekuensi")

# Histogram sesudah
plt.subplot(1, 2, 2)
plt.hist(equalized_data, bins=range(max(mapping.values())+2), edgecolor='black')
plt.title("Histogram Setelah Histogram Equalization")
plt.xlabel("Nilai Keabuan")
plt.ylabel("Frekuensi")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 7. Tampilkan semua hasil perhitungan
# ------------------------------------------------------------
print("DATA ASLI:")
print(data)

print("\nHISTOGRAM:")
for v in sorted_vals:
    print(f"{v} = {hist[v]}")

print("\nCDF (Distribusi Kumulatif):")
for v in sorted_vals:
    print(f"{v}: {cdf[v]}")

print("\nMapping Ko (Rumus Buku):")
for v in sorted_vals:
    print(f"{v} → {mapping[v]}")

print("\nDATA SETELAH EKUALISASI:")
print(equalized_data)
