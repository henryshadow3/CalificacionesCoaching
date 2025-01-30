from flask import Flask, request, jsonify, render_template
import pandas as pd
from flask_cors import CORS

# Inicializar la aplicación Flask correctamente antes de usar CORS
app = Flask(__name__)
CORS(app)


# Cargar los datos de todas las hojas del archivo Excel
excel_file = 'promedios ivan modificados.xlsx'  # Nombre del archivo
sheets = pd.ExcelFile(excel_file)
dataframes = {sheet: sheets.parse(sheet) for sheet in sheets.sheet_names}

# Unificar todos los datos en un solo DataFrame con el nombre del grupo
df_combined = pd.concat(
    [df.assign(Grupo=sheet) for sheet, df in dataframes.items()],
    ignore_index=True
)

@app.route("/")
def index():
    # Renderizar el template HTML principal
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

            # Guardamos el orden de las columnas
            column_order = list(df_combined.columns)

            # Diccionario con los datos en el orden correcto
            student_data = {col: value for col, value in student.items() if pd.notna(value)}

            # Agregamos la clave especial para el orden
            student_data["__column_order"] = column_order

            return jsonify(student_data), 200
        else:
            return jsonify({"error": "Contraseña no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
