import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Node:
    def __init__(self, prob, symbol=None, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''

def get_huffman_codes(node, current_code='', codes=None):
    if codes is None:
        codes = {}
    new_code = current_code + str(node.code)
    
    if node.left:
        get_huffman_codes(node.left, new_code, codes)
    if node.right:
        get_huffman_codes(node.right, new_code, codes)
    
    if not node.left and not node.right:
        codes[node.symbol] = new_code
    return codes

def manual_grayscale(image_data):
    height = len(image_data)
    width = len(image_data[0])
    gray_pixels = []
    
    check_val = image_data[0][0][0]
    is_float = isinstance(check_val, float) or (1.0 >= check_val >= 0.0 and type(check_val) != int)

    for y in range(height):
        row = []
        for x in range(width):
            r = image_data[y][x][0]
            g = image_data[y][x][1]
            b = image_data[y][x][2]
            
            if is_float:
                r = int(r * 255)
                g = int(g * 255)
                b = int(b * 255)
            
            val = int((r + g + b) / 3)
            row.append(val)
        gray_pixels.append(row)
    
    return gray_pixels, width, height

def flatten_pixels(matrix):
    flat = []
    for row in matrix:
        for val in row:
            flat.append(val)
    return flat

def calculate_bits_needed(n):
    if n <= 1: return 1
    bits = 0
    val = 1
    while val < n:
        val *= 2 
        bits += 1
    return bits

def compress_huffman(flat_pixels):
    print("1. STATISTICAL COMPRESSION (HUFFMAN)")
    total_pixels = len(flat_pixels)
    counts = {}
    for p in flat_pixels:
        if p in counts:
            counts[p] += 1
        else:
            counts[p] = 1
    
    nodes = []
    for symbol, count in counts.items():
        nodes.append(Node(count / total_pixels, symbol))
    
    nodes.sort(key=lambda x: x.prob)
    
    while len(nodes) > 1:
        left = nodes.pop(0)
        right = nodes.pop(0)
        left.code = '0'
        right.code = '1'
        new_node = Node(left.prob + right.prob, left=left, right=right)
        nodes.append(new_node)
        nodes.sort(key=lambda x: x.prob)
        
    codes = get_huffman_codes(nodes[0])
    
    compressed_bits = 0
    for p in flat_pixels:
        compressed_bits += len(codes[p]) 
        
    original_bits = total_pixels * 8 
    ratio = 100 - ((compressed_bits / original_bits) * 100)
    
    print(f"Ukuran Asli: {original_bits} bit")
    print(f"Ukuran Huffman: {compressed_bits} bit")
    print(f"Ratio Kompresi: {ratio:.2f} %")
    print("-" * 30)

def compress_rle(flat_pixels):
    print("2. SPATIAL COMPRESSION (RLE)")
    encoded = []
    if not flat_pixels:
        return

    prev = flat_pixels[0]
    count = 1
    
    for i in range(1, len(flat_pixels)):
        curr = flat_pixels[i]
        if curr == prev:
            count += 1
        else:
            encoded.append((prev, count))
            prev = curr
            count = 1
    encoded.append((prev, count))
    
    original_size = len(flat_pixels)
    compressed_size = len(encoded) * 2 
    ratio = 100 - ((compressed_size / original_size) * 100)
    
    print(f"Ukuran Asli (piksel): {original_size}")
    print(f"Ukuran RLE (data): {compressed_size}")
    print(f"Ratio Kompresi: {ratio:.2f} %")
    print(f"Sampel Data RLE: {encoded[:5]} ...") 
    print("-" * 30)

def compress_quantizing(matrix_pixels, width, height, target_levels=16):
    print("3. QUANTIZING COMPRESSION")
    flat = flatten_pixels(matrix_pixels)
    total_pixels = len(flat)
    
    histogram = [0] * 256
    for p in flat:
        histogram[p] += 1
        
    pixels_per_cluster = total_pixels / target_levels
    print(f"Target piksel per kelompok (P/n): {pixels_per_cluster:.2f}")
    
    mapping = {}
    current_cluster = 0
    current_count = 0
    
    for val in range(256):
        count = histogram[val]
        if count == 0:
            continue
            
        mapping[val] = current_cluster
        current_count += count
        
        if current_count >= pixels_per_cluster:
            if current_cluster < target_levels - 1:
                current_cluster += 1
                current_count = 0

    cluster_representatives = {}
    step = 255 / (target_levels - 1)
    for i in range(target_levels):
        cluster_representatives[i] = int(i * step)
                
    new_matrix = []
    for r in range(height):
        new_row = []
        for c in range(width):
            old_val = matrix_pixels[r][c]
            cluster_val = mapping.get(old_val, target_levels - 1) 
            visual_val = cluster_representatives[cluster_val]     
            new_row.append(visual_val)
        new_matrix.append(new_row)
        
    original_bits = total_pixels * 8
    new_bit_depth = calculate_bits_needed(target_levels)
    compressed_bits = total_pixels * new_bit_depth
    ratio = 100 - ((compressed_bits / original_bits) * 100)
    
    print(f"Bit depth baru: {new_bit_depth}")
    print(f"Ratio Kompresi (teoretis): {ratio:.2f} %")
    print("-" * 30)
    
    return new_matrix, compressed_bits

def main():
    filename = 'soal1.jpg'
    
    try:
        img_data = mpimg.imread(filename)
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan.")
        return

    if len(img_data.shape) == 3:
        pixels, width, height = manual_grayscale(img_data)
    else:
        height, width = img_data.shape
        pixels = []
        for r in range(height):
            row = []
            for c in range(width):
                val = img_data[r][c]
                if isinstance(val, float):
                    val = int(val * 255)
                row.append(int(val))
            pixels.append(row)

    flat_pixels = flatten_pixels(pixels)
    
    # ========== INFO DIMENSI DAN UKURAN GAMBAR ==========
    total_pixels = width * height
    original_bits = total_pixels * 8  # 8 bit per pixel untuk grayscale
    original_bytes = original_bits / 8
    original_size_kb = original_bytes / 1024
    
    print("=" * 50)
    print("INFORMASI GAMBAR ASLI")
    print("=" * 50)
    print(f"Dimensi Pixel: {width} x {height}")
    print(f"Total Pixel: {total_pixels} pixel")
    print(f"Bit per Pixel: 8 bit (Grayscale)")
    print(f"Total Bit Gambar: {original_bits} bit")
    print(f"Total Bytes: {original_bytes:.0f} bytes")
    print(f"Ukuran Data: {original_size_kb:.2f} KB")
    print("=" * 50)
    print()
    
    # Proses Kompresi
    compress_huffman(flat_pixels)
    compress_rle(flat_pixels)
    result_quant, quant_bits = compress_quantizing(pixels, width, height, target_levels=16)

    # Info hasil kompresi quantizing
    quant_bytes = quant_bits / 8
    quant_size_kb = quant_bytes / 1024
    
    print()
    print("=" * 50)
    print("INFORMASI GAMBAR HASIL QUANTIZING")
    print("=" * 50)
    print(f"Dimensi Pixel: {width} x {height}")
    print(f"Total Pixel: {total_pixels} pixel")
    print(f"Bit per Pixel: 4 bit (16 levels)")
    print(f"Total Bit Gambar: {quant_bits} bit")
    print(f"Total Bytes: {quant_bytes:.0f} bytes")
    print(f"Ukuran Data: {quant_size_kb:.2f} KB")
    print(f"Penghematan: {original_size_kb - quant_size_kb:.2f} KB ({((original_bits - quant_bits) / original_bits * 100):.2f}%)")
    print("=" * 50)
    print()

    output_image_name = 'hasil_kompresi_quantized.png'
    plt.imsave(output_image_name, result_quant, cmap='gray', vmin=0, vmax=255)
    print(f"[INFO] Gambar hasil disimpan: {output_image_name}")

    # Visualisasi
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    title_asli = (
        f"Citra Asli (Grayscale)\n"
        f"Dimensi: {width} x {height} = {total_pixels} pixel\n"
        f"Bit: {original_bits} bit ({original_size_kb:.2f} KB)"
    )
    plt.title(title_asli, fontsize=10)
    plt.imshow(pixels, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    title_hasil = (
        f"Hasil Kuantisasi (16 Level)\n"
        f"Dimensi: {width} x {height} = {total_pixels} pixel\n"
        f"Bit: {quant_bits} bit ({quant_size_kb:.2f} KB)"
    )
    plt.title(title_hasil, fontsize=10)
    plt.imshow(result_quant, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
    
    output_plot_name = 'hasil_perbandingan_plot.png'
    plt.savefig(output_plot_name, dpi=150, bbox_inches='tight')
    print(f"[INFO] Plot perbandingan disimpan: {output_plot_name}")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()