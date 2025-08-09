import sys
import os
import msgpack
import re

def tokenize_text(text):
    """Memecah teks menjadi token kata dan non-kata."""
    return re.findall(r'\w+|\W+', text, re.UNICODE)

def compress_file(input_pdf, output_file):
    """Membaca PDF, mengompresi ke format .bien."""
    from PyPDF2 import PdfReader
    reader = PdfReader(input_pdf)
    full_text = "".join(page.extract_text() or "" for page in reader.pages)

    tokens = tokenize_text(full_text)
    unique_words = list(dict.fromkeys([t for t in tokens if re.match(r'\w+', t)]))  # kata unik saja
    word_index = {word: idx for idx, word in enumerate(unique_words)}

    # Ganti kata dengan ID, karakter non-kata tetap string
    compressed_tokens = [
        word_index[t] if t in word_index else t for t in tokens
    ]

    data = {
        "dict": unique_words,      # list kata unik
        "tokens": compressed_tokens
    }

    with open(output_file, "wb") as f:
        f.write(msgpack.packb(data, use_bin_type=True))

    print(f"[+] File dikompresi: {input_pdf} → {output_file}")
    print(f"    Ukuran awal: {os.path.getsize(input_pdf)/1024:.2f} KB")
    print(f"    Ukuran akhir: {os.path.getsize(output_file)/1024:.2f} KB")

def decompress_file(input_file, output_pdf):
    """Membaca .bien, mengembalikan ke PDF."""
    from fpdf import FPDF

    with open(input_file, "rb") as f:
        data = msgpack.unpackb(f.read(), raw=False, strict_map_key=False)

    dictionary = data["dict"]
    tokens = data["tokens"]

    # Rekonstruksi teks
    text = "".join(
        dictionary[t] if isinstance(t, int) else t for t in tokens
    )

    # Simpan ke PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(output_pdf)

    print(f"[+] File didekompres: {input_file} → {output_pdf}")

def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("  Compress:   py pdfcom.py --compress namafile.pdf")
        print("  Decompress: py pdfcom.py --decompress namafile.pdf.bien")
        sys.exit(1)

    mode = sys.argv[1]
    filepath = sys.argv[2]

    if mode == "--compress":
        if not filepath.lower().endswith(".pdf"):
            print("[!] File input harus PDF untuk mode compress.")
            sys.exit(1)
        output_path = filepath + ".bien"
        compress_file(filepath, output_path)

    elif mode == "--decompress":
        if not filepath.lower().endswith(".bien"):
            print("[!] File input harus .bien untuk mode decompress.")
            sys.exit(1)
        output_path = filepath.replace(".bien", "_restored.pdf")
        decompress_file(filepath, output_path)

    else:
        print("[!] Mode tidak dikenal.")
        sys.exit(1)

if __name__ == "__main__":
    main()
