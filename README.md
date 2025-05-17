# RASA Chatbot - IT Support Universitas

Chatbot ini dibuat menggunakan framework RASA untuk menangani pertanyaan terkait permasalahan perangkat jaringan seperti LAN, Access Point (AP), dan Smart TV. Bot juga terintegrasi dengan Telegram untuk penggunaan langsung oleh pengguna kampus.

## Fitur Utama

- Menangani masalah koneksi LAN, Wi-Fi kampus, Smart TV
- Menanggapi pertanyaan seperti koneksi lambat, gagal login ke Wi-Fi, dan konfigurasi perangkat
- Fallback otomatis untuk kasus di luar cakupan
- Integrasi dengan Telegram melalui `bridge.py`
- Mendukung sesi awal dan pengenalan perangkat pengguna

## Installation & Running

1. Siapkan lingkungan virtual:

```python
python3 -m venv rasa
source rasa/bin/activate
```

2. Install dependency:

```python
pip install rasa requests python-telegram-bot python-dotenv
```

3. Jalankan training:

```python
rasa train
```

4. Jalankan server action:

```python
rasa run actions
```

5. Jalankan RASA server:

```python
rasa run --enable-api --cors "*" --debug
```

6. Jalankan integrasi Telegram:

```python
python3 bridge.py
```

## Penanganan Fallback

Jika bot tidak mengenali intent, maka akan menjalankan `action_contact_it_support` yang mengarahkan pengguna untuk menghubungi tim IT melalui email.

## Contoh Intent yang Didukung

- LAN: kabel tidak terdeteksi, lambat, no internet
- AP: gagal login ke Wi-Fi, sinyal hilang
- TV: screen mirroring, HDMI tidak muncul, suara tidak keluar

