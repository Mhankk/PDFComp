# PDF Compressor & Decompressor (.bien format)

## Deskripsi
Script Python ini memungkinkan Anda untuk melakukan kompresi teks dari file PDF menjadi format biner khusus `.bien` dan mengembalikannya ke PDF.
Proses ini bekerja dengan mengganti kata-kata yang berulang dengan indeks numerik untuk menghemat ukuran file.

## Fitur
- **Kompresi**: Mengubah PDF menjadi file `.bien` yang ukurannya lebih kecil.
- **Dekompresi**: Mengubah file `.bien` kembali menjadi PDF.
- Format aman dan kompatibel, mendukung teks non-ASCII.

## Instalasi
Pastikan Python 3 sudah terpasang, lalu instal dependencies:
```bash
pip install msgpack PyPDF2 fpdf
```

## Penggunaan
### Kompres PDF
```bash
python pdfcom.py --compress namafile.pdf
```
Output akan berupa `namafile.pdf.bien`.

### Dekompres ke PDF
```bash
python pdfcom.py --decompress namafile.pdf.bien
```
Output akan berupa `namafile_restored.pdf`.

## Catatan Teknis
- **Ekstensi `.bien`** adalah format biner custom berbasis `msgpack`.
- Dictionary kata disimpan sebagai *list* kata unik, sedangkan teks disimpan dalam bentuk daftar token (integer atau string).
- Menggunakan `PyPDF2` untuk membaca PDF dan `fpdf` untuk membuat PDF hasil dekompresi.

## Disclaimer
Script ini dibuat untuk tujuan edukasi dan optimasi ukuran file berbasis teks. Tidak menjamin hasil identik secara layout dengan PDF asli, terutama jika PDF mengandung gambar atau format kompleks.

---
© 2025 - PDF Compressor (.bien format)
