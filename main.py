from flask import Flask, request, jsonify, render_template
import pandas as pd

# Inicializar la aplicación Flask
app = Flask(__name__)

# Cargar los datos de Excel al iniciar la aplicación
df = pd.read_excel('calificaciones.xlsx', usecols=["Nombre", "Email", "Calificacion"])
df['Email'] = df['Email'].str.lower()  # Convertir todos los correos a minúsculas para evitar errores de búsqueda

@app.route("/")
def index():
    # Renderizar el template HTML principal
    return render_template("frontend.html")

@app.route('/get_grade', methods=['POST'])
def get_grade():
    try:
        # Obtener los datos JSON enviados por el cliente
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"error": "Falta el campo 'email'."}), 400

        email = email.lower()  # Convertir el correo ingresado a minúsculas

        # Verificar si el correo existe en el DataFrame
        if email in df['Email'].values:
            student = df[df['Email'] == email].iloc[0]  # Obtener la fila correspondiente
            name = student['Nombre']
            grade = int(student['Calificacion'])  # Convertir explícitamente a int

            return jsonify({
                "nombre": name,
                "email": email,
                "calificación": grade  # Mapeo correcto con el frontend
            }), 200
        else:
            return jsonify({"error": "Correo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
