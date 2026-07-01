# 🐟 ИАРА — Информационна система

## 📁 СТРУКТУРА НА ПАПКИТЕ

```
iara_app/
├── app.py                    ← главният файл (сървърът)
├── requirements.txt          ← Flask пакет
├── README.md                 ← тези инструкции
└── templates/                ← всички HTML страници
    ├── base.html
    ├── index.html
    ├── koraби.html
    ├── korab_form.html
    ├── korab_detail.html
    ├── razreshitelni.html
    ├── razreshitelno_form.html
    ├── bileti.html
    ├── bilet_form.html
    ├── bilet_proverka.html
    ├── inspektsii.html
    ├── inspektsiya_form.html
    └── dnevnik_form.html
```

---

## ⚙️ КАК ДА СТАРТИРАМ (само първия път)

### Стъпка 1 — Инсталирай Python
Свали от https://python.org → версия 3.10 или по-нова
При инсталацията СЛОЖИ ОТМЕТКА на "Add Python to PATH"!

### Стъпка 2 — Отвори cmd в папката
Отвори папката iara_app → в адресната лента напиши "cmd" → Enter

### Стъпка 3 — Инсталирай Flask (само веднъж)
```
pip install flask
```

### Стъпка 4 — Стартирай
```
python app.py
```

### Стъпка 5 — Отвори в браузър
- Компютър: http://127.0.0.1:5000
- Телефон (същата WiFi): намери IP с ipconfig → http://192.168.x.x:5000
