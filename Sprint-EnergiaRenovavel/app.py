from flask import Flask, render_template, request, redirect
import random
import database

app = Flask(__name__)

# Inicializa o banco de dados
database.create_tables()


@app.route('/')
def index():
    devices = database.get_devices()
    return render_template('index.html', devices=devices)


@app.route('/set_user_energy', methods=['POST'])
def set_user_energy():
    monthly_consumption = request.form['monthly_consumption']
    database.set_user_energy(monthly_consumption)
    return redirect('/')


@app.route('/add_device', methods=['POST'])
def add_device():
    name = request.form['name']
    importance = request.form['importance']
    database.add_device(name, importance)
    return redirect('/')


@app.route('/delete_device/<int:device_id>', methods=['POST'])
def delete_device(device_id):
    database.delete_device(device_id)
    return redirect('/')


@app.route('/energy_status')
def energy_status():
    # Simula a energia restante
    energy_remaining = random.randint(0, 100)  # Porcentagem de energia restante
    total_consumption = database.get_user_energy()  # Consumo mensal do usuário
    consumption_rate = total_consumption / 30  # Consumo diário médio (supondo 30 dias no mês)

    # Calcular horas restantes
    hours_remaining = energy_remaining / consumption_rate if consumption_rate > 0 else float('inf')

    # Verificar se a energia está acabando
    if energy_remaining < 25:  # Se a energia restante for menor que 25%
        # Deletar dispositivos de alta importância
        devices = database.get_devices()
        for device in devices:
            if device[2] == 3:  # Importância 3
                database.delete_device(device[0])  # Deletar dispositivo
                print(f"Dispositivo {device[1]} foi deletado devido à baixa energia.")

    return f'Energia restante: {energy_remaining}%, Horas restantes: {hours_remaining:.2f}'


if __name__ == '__main__':
    app.run(debug=True)
