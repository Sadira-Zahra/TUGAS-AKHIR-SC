# TUGAS-AKHIR-SC
 Aplikasi Deteksi Kerusakan Pada Mobil dan Estimasi Harga Perbaikan dengan YOLOV8 dan CNN


**Tujuan**

Proyek ini bertujuan untuk membuat sistem yang mampu memprediksi estimasi biaya 
perbaikan mobil berdasarkan kerusakan yang terdeteksi. Dengan adanya sistem ini, pengguna 
diharapkan dapat dengan mudah mengetahui estimasi biaya dan waktu perbaikan mobil mereka 
secara cepat dan akurat, tanpa perlu mendatangi bengkel terlebih dahulu.

**Data**

Dataset yang digunakan dalam penelitian ini diperoleh dari repository publik di GitHub dan 
juga dari Roboflow. Repository tersebut menyediakan kumpulan data yg relevan untuk deteksi 
kerusakan mobil dan estimasi perbaikannya dan juga roboflow tersebut menyediakan kumpulan 
gambar yg relevan yang dapat mendukung sistem deteksi kerusakan mobil.

**Arsitektur Model**

Proyek ini bertujuan mendeteksi kerusakan mobil dan estimasi perbaikan menggunakan dataset dari GitHub yang dikelola melalui Roboflow. Dataset mencakup tiga kelas kerusakan: GlassBreak (kaca pecah), Dent (penyok), dan Scratch (goresan), dengan anotasi dan konfigurasi data.yaml. YOLOv8 Nano digunakan sebagai model deteksi objek karena keunggulan dalam kecepatan dan akurasi, serta efisiensi sumber daya, dengan pelatihan dilakukan pada CPU menggunakan parameter default yang disesuaikan.

**Hasil**

![image](https://github.com/user-attachments/assets/2dc61ada-c095-4e1f-9277-5e207ab0a675)
