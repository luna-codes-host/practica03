# 📌 Proyecto Practica03
Validación de pruebas, análisis de datos y medición de cobertura con Python

## 🧰 Descripción del Proyecto
Este proyecto contiene módulos para el procesamiento y análisis de datos, así como un conjunto de pruebas automatizadas que permiten validar su funcionamiento.
Incluye integración con **coverage.py** para medir el porcentaje de líneas ejecutadas durante los tests.

---

## 📁 Estructura del Proyecto

practica03/
│── src/
│ └── procesador.py
│── tests/
│ └── test_analizador.py
│── htmlcov/ # Reporte HTML generado por coverage.py
│── venv/ # Entorno virtual de Python
│── app.py
│── .coverage
│── .gitignore
└── README.md


---

## ⚙️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.10+
- pip
- virtualenv (opcional pero recomendado)

---

## ▶️ Instalación

### 1. Crear y activar entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate

2. Instalar dependencias del proyecto

pip install -r requirements.txt # Si lo tienes

O instalar manualmente:

pip install coverage

🧪 Ejecutar las Pruebas

Para ejecutar los tests del proyecto:

pytest

📊 Medir Cobertura de Código
1. Ejecutar coverage

coverage run -m pytest

2. Ver reporte en consola

coverage report -m

3. Generar reporte HTML

coverage html

El reporte se guarda en la carpeta htmlcov/.
🌐 Abrir el Reporte HTML
Opción 1: Desde el navegador

Ir a:

htmlcov/index.html

Opción 2: Desde terminal

firefox htmlcov/index.html
