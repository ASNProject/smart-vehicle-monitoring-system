<!--
 Copyright 2025 ariefsetyonugroho
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     https://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

# 📦 Smart Vehicle Monitoring System  
Sistem ini dirancang untuk mendeteksi kendaraan berupa mobil dan sepeda motor menggunakan dua kamera USB yang terhubung ke Raspberry Pi 5. Sistem melakukan pemrosesan citra secara real-time menggunakan metode deep learning YOLO untuk mendeteksi objek kendaraan. Hasil deteksi akan ditampilkan pada LCD 7 inch dan dikirimkan melalui komunikasi serial.

## ✨ Features  
- Realtime dual kamera 
- Deteksi objek menggunakan model YOLO 
- Deteksi estimasi jarak
- Tampilan UI LCD
- Komunikasi Serial

## ⚙️ Installation & 🚀 Usage 
- Clone Project
```
git clone https://github.com/username/project_name.git
```
- Buka Project
```
cd project_name
```
- Install requirements
```
pip install -r requirements.txt
```
- Run Project
```p
python main.py
```


## Notes
### Cara kalibrasi jarak
- Letakan objek (motor/mobil) 
- Ukur jarak asli (misal 2 meter)
- Ambil nilai pixel width yang ada di terminal console
- Ambil 3-5 sample dan cari rata-ratanya
Contoh
```
pixel width: 200
jarak asli: 2 meter

focal = (pixel_width * distance) / real_width

focal = (200 * 2) / 1.8
focal ≈ 222
```

### Other Notes
- Create requirements.txt
```
pip freeze > requirements.txt
```

- If only library used
```
pip install pipreqs
pipreqs . --force
pipreqs project_name --force (Jika mau update)
```