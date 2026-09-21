import json

with open('SIPARTA.ipynb', 'r') as f:
    nb = json.load(f)

# Cell 1: TFLite Conversion
markdown_1 = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n",
        "# ============================================================\n",
        "# TFLITE CONVERSION (Pipeline Integrasi Edge AI)\n",
        "# ============================================================\n",
        "# Tahap krusial untuk perangkat Edge (Raspberry Pi 3 B+):\n",
        "# Model `.keras` yang berat akan dikonversi menjadi format `.tflite`.\n",
        "# Format ini dapat dieksekusi oleh `tflite-runtime` dengan memori sangat rendah.\n"
    ]
}

code_1 = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ============================================================\n",
        "# 1. Konversi Keras ke TensorFlow Lite\n",
        "# ============================================================\n",
        "import tensorflow as tf\n",
        "\n",
        "# Gunakan converter bawaan TF\n",
        "converter = tf.lite.TFLiteConverter.from_keras_model(model)\n",
        "tflite_model = converter.convert()\n",
        "\n",
        "# Simpan model TFLite\n",
        "with open('siparta_edge_model.tflite', 'wb') as f:\n",
        "    f.write(tflite_model)\n",
        "    \n",
        "print(\"✅ Model sukses dikonversi menjadi: siparta_edge_model.tflite\")\n"
    ]
}

# Cell 2: RPi Simulation
markdown_2 = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n",
        "# ============================================================\n",
        "# SIMULASI INTEGRASI main_rpi.py\n",
        "# ============================================================\n",
        "# Menguji simulasi alur `main_rpi.py` langsung di Notebook.\n",
        "# Menjalankan model Edge (.tflite) dan melakukan triger HTTP ke Backend / Web3.\n"
    ]
}

code_2 = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ============================================================\n",
        "# 2. Simulasi Eksekusi tflite-runtime ala main_rpi.py\n",
        "# ============================================================\n",
        "import numpy as np\n",
        "\n",
        "# A. Inisialisasi Interpreter TFLite (seperti di Raspberry Pi)\n",
        "interpreter = tf.lite.Interpreter(model_path=\"siparta_edge_model.tflite\")\n",
        "interpreter.allocate_tensors()\n",
        "\n",
        "input_details = interpreter.get_input_details()\n",
        "output_details = interpreter.get_output_details()\n",
        "\n",
        "def inferensi_rpi_tflite(features):\n",
        "    \"\"\"\n",
        "    Fungsi replika dari run_inference() di main_rpi.py\n",
        "    \"\"\"\n",
        "    # Lakukan scaling menggunakan scaler yang sudah kita fit (di RPi bisa pakai Matrix statis)\n",
        "    features_scaled = scaler.transform([features]).astype(np.float32)\n",
        "    \n",
        "    # Set Tensor Input\n",
        "    interpreter.set_tensor(input_details[0]['index'], features_scaled)\n",
        "    \n",
        "    # Jalankan Edge Inferensi\n",
        "    interpreter.invoke()\n",
        "    \n",
        "    # Ambil Hasil\n",
        "    output_data = interpreter.get_tensor(output_details[0]['index'])\n",
        "    predicted_class = np.argmax(output_data)\n",
        "    \n",
        "    status_map = {0: \"AMAN\", 1: \"WASPADA\", 2: \"BAHAYA\"}\n",
        "    return status_map[predicted_class]\n",
        "\n",
        "# B. Testing dengan dummy payload (Asumsi Campuran Pemutih & HCl)\n",
        "# Berdasarkan urutan fitur: [bahan_1, bahan_2, pH_1, pH_2, diff, kon_1, kon_2, suhu, ventilasi, vol]\n",
        "dummy_sensor_payload = [0, 4, 12.0, 1.0, 11.0, 5.0, 20.0, 30.0, 0.2, 500.0]\n",
        "\n",
        "status_terdeteksi = inferensi_rpi_tflite(dummy_sensor_payload)\n",
        "print(f\"📡 Data Telemetri masuk: {dummy_sensor_payload}\")\n",
        "print(f\"🧠 Hasil Edge TFLite  : {status_terdeteksi}\")\n",
        "\n",
        "# C. Triger Hardware Aktuator & Komunikasi Eksternal\n",
        "if status_terdeteksi == \"BAHAYA\":\n",
        "    print(\"\\n🚨 [HARDWARE TRIGGER] Menghidupkan LED Merah & Buzzer 5V...\")\n",
        "    print(\"📸 [CAMERA MODULE] RPi OV5647 mengambil foto bukti (danger_log_xxx.jpg)!\")\n",
        "    print(\"🌐 [WEB3 & BACKEND] Mengirim Multipart Data (JSON + Image) ke FastAPI /api/v1/incidents/report...\")\n"
    ]
}

nb['cells'].extend([markdown_1, code_1, markdown_2, code_2])

with open('SIPARTA.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("Notebook SIPARTA.ipynb successfully updated!")
