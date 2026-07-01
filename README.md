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

---

## 🐙 GIT И GITHUB — ПЪЛНИ ИНСТРУКЦИИ

### Инсталирай Git
Свали от https://git-scm.com/download/win → инсталирай (Next навсякъде)

### Създай GitHub акаунт
Регистрирай се на https://github.com

### Създай Repository
1. Натисни зеления бутон "New"
2. Repository name: iara-app
3. Натисни "Create repository"

---

## 🔧 ПЪРВОНАЧАЛНА НАСТРОЙКА НА GIT (само веднъж)

В cmd напиши:
```
git config --global user.name "Твоето Име"
git config --global user.email "твоя@email.com"
```

---

## 📤 КАЧВАНЕ В GITHUB (само първия път)

В cmd, в папката iara_app:

```
git init
git add .
git commit -m "Първи commit - ИАРА система"
git branch -M main
git remote add origin https://github.com/ТВОЕТО_ИМЕ/iara-app.git
git push -u origin main
```

Замени ТВОЕТО_ИМЕ с твоя GitHub username!

---

## 🔄 СЛЕД ВСЯКА ПРОМЯНА (всеки път)

Само 3 реда:
```
git add .
git commit -m "Описание на промяната"
git push
```

Примери за добри commit съобщения:
- "Добавена функция за инспекции"
- "Оправен бъг в билетите"
- "Добавена нова страница"

---

## ❌ АКО ИМА ГРЕШКА

Грешка "pip not found" → преинсталирай Python с отметката "Add to PATH"
Грешка "port in use" → затвори другия cmd и пусни отново
Телефонът не се свързва → провери дали са на една WiFi мрежа
