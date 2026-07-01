from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.secret_key = 'iara-secret-key-2024'

DB_PATH = 'iara.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS ships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mezhdunaroden_nomer TEXT NOT NULL,
        pozivna TEXT,
        markirovka TEXT,
        sobstvenik TEXT NOT NULL,
        kapitan TEXT NOT NULL,
        dalzhina REAL,
        shirina REAL,
        tonazh REAL,
        dvigatel_moshnost TEXT,
        gorivo TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS permits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ship_id INTEGER NOT NULL,
        nomer TEXT NOT NULL,
        sobstvenik TEXT NOT NULL,
        validen_do TEXT NOT NULL,
        uredi TEXT,
        kapitan TEXT,
        status TEXT DEFAULT 'активно',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ship_id) REFERENCES ships(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ime TEXT NOT NULL,
        egn TEXT NOT NULL,
        tip TEXT NOT NULL,
        kategoriya TEXT NOT NULL,
        cena REAL NOT NULL,
        validen_do TEXT NOT NULL,
        telk_nomer TEXT,
        status TEXT DEFAULT 'активен',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS inspections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inspektor TEXT NOT NULL,
        obekt_tip TEXT NOT NULL,
        obekt_ime TEXT NOT NULL,
        data TEXT NOT NULL,
        rezultat TEXT NOT NULL,
        narushenie TEXT,
        globa REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS logbook (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ship_id INTEGER NOT NULL,
        data_nachalo TEXT NOT NULL,
        mestopolozhenie TEXT NOT NULL,
        uredi TEXT NOT NULL,
        kolichestvo_ryba REAL NOT NULL,
        vid_ryba TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ship_id) REFERENCES ships(id)
    )''')

    conn.commit()
    conn.close()


# ── НАЧАЛНА СТРАНИЦА ─────────────────────────────────────────────
@app.route('/')
def index():
    conn = get_db()
    stats = {
        'ships':       conn.execute('SELECT COUNT(*) as n FROM ships').fetchone()['n'],
        'permits':     conn.execute('SELECT COUNT(*) as n FROM permits').fetchone()['n'],
        'tickets':     conn.execute('SELECT COUNT(*) as n FROM tickets').fetchone()['n'],
        'inspections': conn.execute('SELECT COUNT(*) as n FROM inspections').fetchone()['n'],
    }
    conn.close()
    return render_template('index.html', stats=stats)


# ── КОРАБИ ───────────────────────────────────────────────────────
@app.route('/koraби')
def ships_list():
    conn = get_db()
    ships = conn.execute('SELECT * FROM ships ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('koraби.html', koraби=ships)

@app.route('/koraби/nov', methods=['GET', 'POST'])
def ship_new():
    if request.method == 'POST':
        conn = get_db()
        conn.execute('''INSERT INTO ships
            (mezhdunaroden_nomer, pozivna, markirovka, sobstvenik, kapitan,
             dalzhina, shirina, tonazh, dvigatel_moshnost, gorivo)
            VALUES (?,?,?,?,?,?,?,?,?,?)''', (
            request.form['mezhdunaroden_nomer'],
            request.form.get('pozivna', ''),
            request.form.get('markirovka', ''),
            request.form['sobstvenik'],
            request.form['kapitan'],
            request.form.get('dalzhina') or None,
            request.form.get('shirina') or None,
            request.form.get('tonazh') or None,
            request.form.get('dvigatel_moshnost', ''),
            request.form.get('gorivo', 'дизел'),
        ))
        conn.commit()
        conn.close()
        flash('Корабът е регистриран успешно!', 'success')
        return redirect(url_for('ships_list'))
    return render_template('korab_form.html')

@app.route('/koraби/<int:id>')
def ship_detail(id):
    conn = get_db()
    ship = conn.execute('SELECT * FROM ships WHERE id=?', (id,)).fetchone()
    permits = conn.execute('SELECT * FROM permits WHERE ship_id=?', (id,)).fetchall()
    logs = conn.execute('SELECT * FROM logbook WHERE ship_id=? ORDER BY data_nachalo DESC', (id,)).fetchall()
    conn.close()
    if not ship:
        flash('Корабът не е намерен.', 'danger')
        return redirect(url_for('ships_list'))
    return render_template('korab_detail.html', korab=ship, razreshitelni=permits, dnevnik=logs)


# ── РАЗРЕШИТЕЛНИ ─────────────────────────────────────────────────
@app.route('/razreshitelni')
def permits_list():
    conn = get_db()
    rows = conn.execute('''
        SELECT p.*, s.mezhdunaroden_nomer, s.markirovka
        FROM permits p JOIN ships s ON p.ship_id = s.id
        ORDER BY p.id DESC
    ''').fetchall()
    conn.close()
    return render_template('razreshitelni.html', razreshitelni=rows)

@app.route('/razreshitelni/novo', methods=['GET', 'POST'])
def permit_new():
    conn = get_db()
    ships = conn.execute('SELECT * FROM ships').fetchall()
    if request.method == 'POST':
        conn.execute('''INSERT INTO permits (ship_id, nomer, sobstvenik, validen_do, uredi, kapitan)
            VALUES (?,?,?,?,?,?)''', (
            request.form['ship_id'],
            request.form['nomer'],
            request.form['sobstvenik'],
            request.form['validen_do'],
            request.form.get('uredi', ''),
            request.form.get('kapitan', ''),
        ))
        conn.commit()
        conn.close()
        flash('Разрешителното е издадено!', 'success')
        return redirect(url_for('permits_list'))
    conn.close()
    return render_template('razreshitelno_form.html', koraби=ships)

@app.route('/razreshitelni/<int:id>/otnemane')
def permit_revoke(id):
    conn = get_db()
    conn.execute("UPDATE permits SET status='отнето' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Разрешителното е отнето.', 'warning')
    return redirect(url_for('permits_list'))


# ── БИЛЕТИ ───────────────────────────────────────────────────────
CENI = {
    ('годишен',  'възрастен'): 30.0,
    ('годишен',  'под 14г'):   10.0,
    ('годишен',  'пенсионер'): 15.0,
    ('годишен',  'инвалид'):    0.0,
    ('месечен',  'възрастен'): 10.0,
    ('месечен',  'под 14г'):    5.0,
    ('месечен',  'пенсионер'):  7.0,
    ('месечен',  'инвалид'):    0.0,
    ('дневен',   'възрастен'):  5.0,
    ('дневен',   'под 14г'):    2.0,
    ('дневен',   'пенсионер'):  3.0,
    ('дневен',   'инвалид'):    0.0,
}

@app.route('/bileti')
def tickets_list():
    conn = get_db()
    tickets = conn.execute('SELECT * FROM tickets ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('bileti.html', bileti=tickets)

@app.route('/bileti/nov', methods=['GET', 'POST'])
def ticket_new():
    if request.method == 'POST':
        tip = request.form['tip']
        kategoriya = request.form['kategoriya']
        cena = CENI.get((tip, kategoriya), 0.0)
        telk = request.form.get('telk_nomer', '')

        today = date.today()
        if tip == 'годишен':
            end = date(today.year + 1, today.month, today.day)
        elif tip == 'месечен':
            month = today.month + 1
            year = today.year
            if month > 12:
                month = 1
                year += 1
            end = date(year, month, today.day)
        else:
            end = today + timedelta(days=1)

        conn = get_db()
        conn.execute('''INSERT INTO tickets (ime, egn, tip, kategoriya, cena, validen_do, telk_nomer)
            VALUES (?,?,?,?,?,?,?)''', (
            request.form['ime'],
            request.form['egn'],
            tip, kategoriya, cena, str(end), telk,
        ))
        conn.commit()
        conn.close()
        flash(f'Билетът е издаден! Цена: {cena:.2f} лв.', 'success')
        return redirect(url_for('tickets_list'))
    return render_template('bilet_form.html')

@app.route('/bileti/<int:id>/proverka')
def ticket_check(id):
    conn = get_db()
    ticket = conn.execute('SELECT * FROM tickets WHERE id=?', (id,)).fetchone()
    conn.close()
    if not ticket:
        flash('Билетът не е намерен.', 'danger')
        return redirect(url_for('tickets_list'))
    validen = ticket['validen_do'] >= str(date.today()) and ticket['status'] == 'активен'
    return render_template('bilet_proverka.html', bilet=ticket, validen=validen)


# ── ИНСПЕКЦИИ ────────────────────────────────────────────────────
@app.route('/inspektsii')
def inspections_list():
    conn = get_db()
    rows = conn.execute('SELECT * FROM inspections ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('inspektsii.html', inspektsii=rows)

@app.route('/inspektsii/nova', methods=['GET', 'POST'])
def inspection_new():
    if request.method == 'POST':
        conn = get_db()
        globa = request.form.get('globa') or None
        conn.execute('''INSERT INTO inspections
            (inspektor, obekt_tip, obekt_ime, data, rezultat, narushenie, globa)
            VALUES (?,?,?,?,?,?,?)''', (
            request.form['inspektor'],
            request.form['obekt_tip'],
            request.form['obekt_ime'],
            request.form['data'],
            request.form['rezultat'],
            request.form.get('narushenie', ''),
            globa,
        ))
        conn.commit()
        conn.close()
        flash('Инспекцията е регистрирана!', 'success')
        return redirect(url_for('inspections_list'))
    return render_template('inspektsiya_form.html', today=str(date.today()))


# ── ДНЕВНИК ──────────────────────────────────────────────────────
@app.route('/dnevnik/nov', methods=['GET', 'POST'])
def logbook_new():
    conn = get_db()
    big_ships = conn.execute('SELECT * FROM ships WHERE dalzhina > 10').fetchall()
    if request.method == 'POST':
        conn.execute('''INSERT INTO logbook
            (ship_id, data_nachalo, mestopolozhenie, uredi, kolichestvo_ryba, vid_ryba)
            VALUES (?,?,?,?,?,?)''', (
            request.form['ship_id'],
            request.form['data_nachalo'],
            request.form['mestopolozhenie'],
            request.form['uredi'],
            request.form['kolichestvo_ryba'],
            request.form['vid_ryba'],
        ))
        conn.commit()
        conn.close()
        flash('Записът в дневника е добавен!', 'success')
        return redirect(url_for('index'))
    conn.close()
    return render_template('dnevnik_form.html', koraби=big_ships, today=str(date.today()))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
