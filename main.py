from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

# Clase para el modelo de solicitud
class StudentEmail(BaseModel):
    email: str

# Carga los datos de Excel
df = pd.read_excel('calificaciones.xlsx')
df['Examen(60)'] = pd.to_numeric(df['Examen(60)'], errors='coerce')

app = FastAPI()



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origins (para desarrollo; ajusta en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# El resto de tu código de FastAPI...


@app.post("/get_grade")
async def get_grade(student: StudentEmail):
    # Buscar la calificación por correo electrónico
    if student.email in df['Correo'].values:
        examen10 = float(df[df['Correo'] == student.email]['Examen(10pts)'].iloc[0])
        examen60 = float(df[df['Correo'] == student.email]['Examen(60)'].iloc[0])
       
        proyecto = float(df[df['Correo'] == student.email]['Proyecto(30)'].iloc[0])
        participacion = float(df[df['Correo'] == student.email]['Participación'].iloc[0])
        calificacion3 =float( df[df['Correo'] == student.email]['Calificación Bloque III'].iloc[0])
        calificacionf = float(df[df['Correo'] == student.email]['Calificación Final'].iloc[0])




        return {"email": student.email, 
                "examen 10 pts": examen10,
                "examen60%": examen60,
                 "proyecto":proyecto,
                 "participación":participacion,
                 "Calificación Bloque 3":calificacion3,
                 "Calificación Final (tres bloques)": calificacionf}
    else:
        raise HTTPException(status_code=404, detail="Correo no encontrado")

