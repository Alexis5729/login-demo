from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuración de la Base de Datos
def init_db():
    conn = sqlite3.connect('rosselot_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            precio INTEGER NOT NULL,
            patente TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Plantilla HTML corregida y estilizada
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Inventario Rosselot</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
        h1, h2 { color: #333; }
        /* CORREGIDO: Se cambió de 40px a 500px para que el formulario sea visible y usable */
        form { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 500px; margin-bottom: 20px; }
        .campo { margin-bottom: 15px; }
        .campo label { display: block; margin-bottom: 5px; font-weight: bold; }
        .campo input { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        button { background-color: #0056b3; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; }
        button:hover { background-color: #003d82; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; box-shadow: 0 0 10px rgba(0,0,0,0.05); }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #0056b3; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>🚗 Control de Inventario - Rosselot</h1>
    
    <h2>Registrar Nuevo Vehículo</h2>
    <form action="/agregar" method="POST">
        <div class="campo"><label>Patente:</label><input type="text" name="patente" placeholder="ABCD12 o AB1234" required></div>
        <div class="campo"><label>Marca:</label><input type="text" name="marca" placeholder="Ej: Toyota" required></div>
        <div class="campo"><label>Modelo:</label><input type="text" name="modelo" placeholder="Ej: RAV4" required></div>
        <div class="campo"><label>Año:</label><input type="number" name="ano" placeholder="Ej: 2024" required></div>
        <div class="campo"><label>Precio ($):</label><input type="number" name="precio" placeholder="Ej: 18990000" required></div>
        <button type="submit">Guardar Vehículo</button>
    </form>

    <h2>Vehículos en Stock</h2>
    <table>
        <thead>
            <tr>
                <th>ID</th><th>Patente</th><th>Marca</th><th>Modelo</th><th>Año</th><th>Precio</th>
            </tr>
        </thead>
        <tbody>
            {% for v in vehiculos %}
            <tr>
                <td>{{ v[0] }}</td> <!-- ID -->
                <td>{{ v[5] }}</td> <!-- Patente -->
                <td>{{ v[1] }}</td> <!-- Marca -->
                <td>{{ v[2] }}</td> <!-- Modelo -->
                <td>{{ v[3] }}</td> <!-- Año -->
                <td>${{ "{:,}".format(v[4]) }}</td> <!-- Precio mapeado correctamente -->
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
'''

@app.route('/')
def index():
    conn = sqlite3.connect('rosselot_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehiculos')
    vehiculos = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, vehiculos=vehiculos)

@app.route('/agregar', methods=['POST'])
def agregar():
    marca = request.form['marca']
    modelo = request.form['modelo']
    ano = request.form['ano']
    precio = request.form['precio']
    patente = request.form['patente'].upper()

    try:
        conn = sqlite3.connect('rosselot_inventario.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO vehiculos (marca, modelo, ano, precio, patente) VALUES (?, ?, ?, ?, ?)',
            (marca, modelo, ano, precio, patente)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: La patente ya está registrada.")
    finally:
        conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
