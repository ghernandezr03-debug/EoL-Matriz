
from flask import Flask, render_template, request, send_file
import pandas as pd
import json

app = Flask(__name__)

# Cargar datos desde JSON generado previamente
with open('datos_matriz.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
matriz = data['matriz']
alertas = data['alertas']

@app.route('/')
def index():
    entidades = sorted(set([row['Entidad'] for row in matriz if row.get('Entidad')]))
    tramites = sorted(set([row.get('Tramite que se Realiza') for row in matriz if row.get('Tramite que se Realiza')]))
    return render_template('index.html', entidades=entidades, tramites=tramites)

@app.route('/filtrar', methods=['POST'])
def filtrar():
    entidad = request.form.get('entidad')
    tramite = request.form.get('tramite')
    resultados = [row for row in matriz if (not entidad or row.get('Entidad') == entidad) and (not tramite or row.get('Tramite que se Realiza') == tramite)]
    alerta = alertas.get(entidad, []) if entidad else []
    return render_template('resultado.html', resultados=resultados, alerta=alerta, entidad=entidad)

@app.route('/exportar_excel')
def exportar_excel():
    df = pd.DataFrame(matriz)
    file_path = 'matriz_completa.xlsx'
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)

@app.route('/exportar_excel_filtrado', methods=['POST'])
def exportar_excel_filtrado():
    entidad = request.form.get('entidad')
    tramite = request.form.get('tramite')
    filtrado = [row for row in matriz if (not entidad or row.get('Entidad') == entidad) and (not tramite or row.get('Tramite que se Realiza') == tramite)]
    df = pd.DataFrame(filtrado)
    file_path = 'matriz_filtrada.xlsx'
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
