# mASR

### Cài đặt môi trường
- Python 3.6
- Tạo thư mục chứa project (ví dụ: `mASR`)
- cd đến folder `mASR` và tạo môi trường ảo : `python3 -m venv venv`
- Cài đặt các môi trường phụ thuộc : `pip install -r requirements.txt`

### Tiền xử lý dữ liệu
- Chuyển đổi âm thanh được ghi ở định dạng `mp3` hoặc `m4a` sang định dạng `wav`, `mono-chanel`, `sample rate = 16kHz`: 
```
for f in *.m4a; do ffmpeg -i "$f" -acodec pcm_s16le -ac 1 -ar 16000 "${f/%m4a/wav}"; done
```
- Phân cắt dữ liệu thành các file con và tạo description cho từng file dữ liệu:
```
python3 preprocessing_data.py
```

### Sử dụng
1. Tạo data train và data valid. Lưu vào định dạng `.json`
 ```buildoutcfg
python3 create_json_desc.py data/wav/ train_corpus.json valid_corpus.json
```
 
2. Để huấn luyện model, Run
```buildoutcfg
python3 main.py --input_dim 13 \
                --epochs 100 \ 
                --train_desc_file train_corpus.json \ 
                --valid_desc_file valid_corpus.json \
                --save_model_path mmodel1.h5 \
                --pickle_path mmodel1.pickle \
```
Model sau đó được lưu vào folder `results/`

3. Để đánh giá model, Run
```buildoutcfg
python3 evaluation.py --r labels.txt --t prediction.txt

xer/xer -i file -r labels.txt -t prediction.txt
```

4. Để chạy thử nghiệm, Run 
```buildoutcfg
python3 app.py

Run Browser: `http://0.0.0.0:8888/`

Sau đó, upload 1 file `.wav`. Mô hình sẽ đưa ra transcript tương ứng của n
```

Ngoài ra, để xem loss của tập train và valid trong quá trình huấn luyện, Run
```buildoutcfg
python3 visual_loss.py
```

### Bộ dữ liệu
- Bộ dữ liệu được ghi âm bằng trình ghi âm của điện thoại Sol Prime T1000, Redmi Note 8 và Samsung A8 Star
- Gồm có 3 speaker
- Tập corpus gồm 1600 từ đơn. Ghi tâm tại 4 thời điểm khác nhau
- Để xem phân bố âm vị của 1600 từ, Run
 ```
cd data/
python3 systhesis_data.py
```
    
### Mô hình
- `Convolutional + GRU`
- Loss Function:
    - `CTC loss`
- Decoding Algorithmn:
    - `Max-decoding`
    - `Beam search`
- Metrics:
    - `Word Error Rate (WER)`
    - `Character Error Rate (CER)`
    - `Sentence Error Rate (SER)`
    
### Cấu trúc file/folder
```
app.py
data
    test
    wav
        DTM1
        DTM2
        DTM3
        NB
    corpus3k.txt
    lexicon_vietnamese_phoneme.txt
    phonemes.txt
    preprocessing_data.py
    systhesis_data.py
results
templates
    home.html
statis
char_map.py
create_json_desc.py
data_generator.py
evaluation.py
main.py
models.py
README.md
requirements.txt
train_corpus.json
train_utils.py
utils.py
valid_corpus.json
visual_loss.py
```
