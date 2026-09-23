# SIPARTA AI Models & Edge Computing

Direktori ini berisi lapisan deteksi fisik SIPARTA yang berjalan langsung pada lingkungan *Edge Device* (Raspberry Pi). Modul ini bertanggung jawab membaca sensor kimia melalui protokol I2C, menjalankan model Artificial Neural Network (TensorFlow Lite), dan mentransmisikan data bahaya ke *Backend Controller*.

## 1. Project Overview

Kecepatan respons adalah elemen paling krusial dalam pencegahan kecelakaan gas beracun. Daripada mengandalkan backend cloud untuk menghitung kadar gas (yang memiliki kelemahan latensi jaringan), SIPARTA menanamkan (embedded) file `.tflite` langsung ke dalam Raspberry Pi. 
Hal ini memastikan bahwa sistem peringatan darurat (seperti Buzzer/LED lokal) bekerja deterministik dan seketika (sub-detik). 

## 2. Architecture Overview

- **Hardware**: Raspberry Pi 3 B+ (atau lebih tinggi).
- **ADC Converter**: ADS1115 (Komunikasi I2C via PIN GPIO).
- **Sensors**: MICS-5524, TGS2600, MQ-2, MQ-135.
- **Machine Learning**: TensorFlow Lite Interpreter (untuk efisiensi prosesor ARM).
- **Communication Protocol**: HTTP POST multipart/form-data menggunakan pustaka `requests`.

## 3. Prerequisites

Bila Anda menjalankan ini di Raspberry Pi, pastikan:
- I2C dan Kamera (jika pakai) telah diaktifkan via `sudo raspi-config`.
- Telah menginstal library sistem: `sudo apt-get install libi2c-dev i2c-tools python3-pip libgl1-mesa-glx`
- Terhubung dengan jaringan WiFi (untuk komunikasi ke backend).

## 4. Environment Configuration

Salin file contoh env:
```bash
cp .env.example .env
```

Sesuaikan isinya:
- `SIPARTA_BACKEND_URL` = URL dari backend FastAPI (contoh: `http://192.168.1.100:8000` atau URL public internet).
- `DEVICE_ID` = String identifier khusus, misalnya didapat dari tabel master device di backend Anda.
- `DEVICE_API_KEY` = Harus **sama** dengan konfigurasi API Key di dalam backend FastAPI, sebagai autentikasi *Edge*.

## 5. Installation & Setup

1. Buka terminal pada Raspberry Pi, arahkan ke `ai_models`.
2. *(Disarankan)* Buat environment Python `python3 -m venv venv`.
3. Install semua *dependencies* (TensorFlow Lite, OpenCV, Numpy, Requests, adafruit-ads1x15):
   ```bash
   pip install -r requirements.txt
   ```
   *Catatan: Instalasi `tflite-runtime` pada OS Pi lama terkadang perlu dilakukan secara manual menggunakan file `.whl` dari repositori resmi TensorFlow.*

## 6. Hardware Connection

Sambungkan sensor analog ke pin ADS1115 sebagai berikut:
- **A0**: MICS-5524 (Gas umum / CO)
- **A1**: TGS2600 (Air Quality / Propana)
- **A2**: MQ-2 (Asap / Gas mudah terbakar)
- **A3**: MQ-135 (NH3, Benzena, CO2)

Hubungkan pin ADS1115 (SDA, SCL, VDD, GND) ke pin I2C Raspberry Pi.

## 7. Running the Application

Pastikan Backend FastAPI sudah berjalan sebelum mengeksekusi ini.
Jalankan skrip utama:
```bash
python main_rpi.py
```

Skrip ini akan:
1. Memuat model `siparta_model.tflite` dari memori.
2. Membaca data ADC berulang (loop).
3. Jika model memprediksi status "BAHAYA" secara konsisten, ia akan mengambil gambar kamera dan mengirim payload POST ke `SIPARTA_BACKEND_URL/api/v1/incidents/report`.

## 8. Troubleshooting

- **Symptom**: `OSError: [Errno 121] Remote I/O error` atau I2C error.
  - **Penyebab**: Pin SDA/SCL kendor, kabel putus, atau fitur I2C belum dienable di OS RPi.
  - **Solusi**: Periksa koneksi hardware dan jalankan `i2cdetect -y 1`. Alamat ADS1115 biasanya `0x48`.
- **Symptom**: 403 Forbidden atau 401 Unauthorized dari Backend.
  - **Penyebab**: `DEVICE_API_KEY` salah/berbeda dengan Backend.
  - **Solusi**: Sesuaikan key pada `.env`.
- **Symptom**: OpenCV Error (Video capture gagal).
  - **Penyebab**: Modul kamera lepas atau `/dev/video0` tidak tersedia.
  - **Solusi**: Matikan sementara fitur tangkapan gambar di kode `main_rpi.py` jika tidak ada kamera, atau perbaiki modul kamera.
