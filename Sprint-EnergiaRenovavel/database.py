import sqlite3


def create_connection():
    conn = sqlite3.connect('energy_data.db')
    return conn


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Tabela para dispositivos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            importance INTEGER NOT NULL
        )
    ''')

    # Tabela para consumo de energia do usuário
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_energy (
            id INTEGER PRIMARY KEY,
            monthly_consumption REAL DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


def add_device(name, importance):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO devices (name, importance) VALUES (?, ?)', (name, importance))
    conn.commit()
    conn.close()


def get_devices():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    devices = cursor.fetchall()
    conn.close()
    return devices


def delete_device(device_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM devices WHERE id = ?', (device_id,))
    conn.commit()
    conn.close()


def set_user_energy(monthly_consumption):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_energy')  # Limpa a tabela antes de inserir um novo valor
    cursor.execute('INSERT INTO user_energy (monthly_consumption) VALUES (?)', (monthly_consumption,))
    conn.commit()
    conn.close()


def get_user_energy():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_energy')
    energy = cursor.fetchone()
    conn.close()
    return energy[1] if energy else 0  # Retorna 0 se não houver registro


