from flask import Flask, request, jsonify, render_template
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cargar el archivo Excel
excel_file = 'promedios ivan modificados.xlsx'
sheets = pd.ExcelFile(excel_file)
first_sheet_name = sheets.sheet_names[0]
df_combined = sheets.parse(first_sheet_name)

# Obtener el orden exacto de las columnas desde el archivo
ordered_columns = list(df_combined.columns)

@app.route("/")
def index():
    return render_template("frontend.html")

@app.route('/get_data', methods=['POST'])
def get_data():
    try:
        data = request.get_json()
        password = data.get('contraseña')

        if not password:
            return jsonify({"error": "Falta el campo 'contraseña'."}), 400

        if password in df_combined['contraseña'].values:
            student = df_combined[df_combined['contraseña'] == password].iloc[0]

            # Obtener el orden exacto de las columnas
            column_order = list(df_combined.columns)

            # Construir el diccionario de respuesta con el orden correcto
            student_data = {col: student[col] for col in column_order if pd.notna(student[col])}

            # Agregar el grupo del estudiante
            student_data["GRUPO"] = student["GRUPO"]

            # Agregar la clave especial con el orden correcto de columnas
            student_data["__column_order"] = column_order

            return jsonify(student_data), 200
        else:
            return jsonify({"error": "Contraseña no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
