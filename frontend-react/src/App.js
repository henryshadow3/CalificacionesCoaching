import React, { useState } from 'react';

function App() {
  const [contraseña, setContraseña] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:5002/get_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ contraseña }),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error desconocido');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Consulta de Calificaciones</h1>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          placeholder="Ingresa tu contraseña"
          value={contraseña}
          onChange={(e) => setContraseña(e.target.value)}
          required
          style={styles.input}
        />
        <button type="submit" style={styles.button}>
          Consultar
        </button>
      </form>

      {result && (
        <div style={styles.result}>
          <h3>Resultados:</h3>
          <table style={styles.table}>
            <tbody>
              {/* Primero mostramos el nombre */}
              {result.NOMBRE && (
                <tr>
                  <td style={styles.bold}>Nombre:</td>
                  <td>{result.NOMBRE}</td>
                </tr>
              )}
              {/* Mostrar los datos respetando el orden de columnas del Excel, sin mostrar __column_order */}
              {result.__column_order &&
                result.__column_order
                  .filter(key => key !== 'NOMBRE' && key !== 'contraseña' && key !== '__column_order' && !key.startsWith('Unnamed'))
                  .map((key) => (
                    result[key] !== undefined ? (
                      <tr key={key}>
                        <td style={styles.bold}>{key}:</td>
                        <td>{result[key]}</td>
                      </tr>
                    ) : null
                  ))}
            </tbody>
          </table>
        </div>
      )}

      {error && (
        <div style={{ ...styles.result, color: 'red' }}>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f5f5f5',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'column',
    height: '100vh',
    margin: 0,
    padding: 20,
  },
  title: {
    fontSize: '1.5rem',
    marginBottom: '20px',
    textAlign: 'center',
    color: '#333',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    background: '#fff',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  input: {
    padding: '10px',
    marginBottom: '15px',
    border: '1px solid #ddd',
    borderRadius: '5px',
    fontSize: '1rem',
  },
  button: {
    padding: '10px',
    backgroundColor: '#007BFF',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    fontSize: '1rem',
    cursor: 'pointer',
  },
  result: {
    marginTop: '20px',
    padding: '15px',
    backgroundColor: '#f1f1f1',
    borderRadius: '5px',
    width: '60%',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  bold: {
    fontWeight: 'bold',
    paddingRight: '10px',
  },
};

export default App;
