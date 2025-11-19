import unittest
import os
import csv
from src.procesador import Analizador

# --- DATOS SIMULADOS (MOCK DATA) ---
# Usamos el pipe '|' como separador para que coincida con la configuración de Analizador.
MOCK_FILE = 'mock_sri_ventas.csv'
MOCK_SEPARATOR = '|' 

# Datos de prueba controlados para verificar todos los requisitos.
# Incluye un dato negativo en 'EXPORTACIONES' (-10.00) para probar la limpieza a 0.0.
MOCK_DATA = [
    # TOTAL_VENTAS | EXPORTACIONES | IMPORTACIONES | MES
    {'PROVINCIA': 'PICHINCHA', 'TOTAL_VENTAS': '1000.00', 'EXPORTACIONES': '500.00', 'IMPORTACIONES': '100.00', 'MES': '01'},
    {'PROVINCIA': 'GUAYAS', 'TOTAL_VENTAS': '2000.00', 'EXPORTACIONES': '1000.00', 'IMPORTACIONES': '500.00', 'MES': '02'},
    {'PROVINCIA': 'PICHINCHA', 'TOTAL_VENTAS': '500.00', 'EXPORTACIONES': '200.00', 'IMPORTACIONES': '50.00', 'MES': '01'},
    {'PROVINCIA': 'GUAYAS', 'TOTAL_VENTAS': '100.00', 'EXPORTACIONES': '-10.00', 'IMPORTACIONES': '800.00', 'MES': '02'}, 
    {'PROVINCIA': 'AZUAY', 'TOTAL_VENTAS': '3000.00', 'EXPORTACIONES': '0.00', 'IMPORTACIONES': '1000.00', 'MES': '03'},
    {'PROVINCIA': 'IMBABURA', 'TOTAL_VENTAS': 'NO_NUM', 'EXPORTACIONES': '0.00', 'IMPORTACIONES': '0.00', 'MES': '04'}
]

# Sumas Esperadas (basadas en la limpieza a 0.0 de Analizador):
# Ventas: PICHINCHA: 1500.00 | GUAYAS: 2100.00 | AZUAY: 3000.00
# Exportaciones: Mes 01: 700.00 | Mes 02: 1000.00 
# Importaciones Max: GUAYAS (1300.00)

class TestAnalizador(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 1. Crear el archivo CSV mock
        with open(MOCK_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = MOCK_DATA[0].keys()
            # Usar el separador '|'
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=MOCK_SEPARATOR)
            writer.writeheader()
            writer.writerows(MOCK_DATA)
        
        # 2. Inicializar la clase Analizador con los datos mock
        cls.analizador = Analizador(MOCK_FILE, separador=MOCK_SEPARATOR) 

    @classmethod
    def tearDownClass(cls):
        # 3. Limpiar: Eliminar el archivo CSV mock
        if os.path.exists(MOCK_FILE):
            os.remove(MOCK_FILE)

    # -----------------------------------------------
    # PRUEBAS PASO 4: Funciones Base
    # -----------------------------------------------

    # 3. Garantizar que la función retorne un diccionario.
    def test_ventas_totales_retorna_diccionario(self):
        resumen = self.analizador.ventas_totales_por_provincia()
        self.assertIsInstance(resumen, dict, "El resultado debe ser un diccionario.")

    # 1. Validar que el número de provincias sea coherente.
    def test_numero_provincias_coherente(self):
        resumen = self.analizador.ventas_totales_por_provincia()
        # Esperamos 4 provincias únicas de nuestro MOCK DATA
        provincias_esperadas = {'PICHINCHA', 'GUAYAS', 'AZUAY', 'IMBABURA'}
        self.assertEqual(len(resumen), len(provincias_esperadas), "El número de provincias únicas es incorrecto.")

    # 2. Verificar que los valores calculados sean numéricos y no negativos.
    def test_valores_son_numericos_y_no_negativos(self):
        resumen = self.analizador.ventas_totales_por_provincia()
        for provincia, total_ventas in resumen.items():
            self.assertIsInstance(total_ventas, (int, float), f"El valor de ventas de {provincia} no es numérico.")
            # Aseguramos que la limpieza de datos funcionó
            self.assertGreaterEqual(total_ventas, 0, f"El valor de ventas de {provincia} es negativo.")
            
    # 4. Verificar que las provincias consultadas existan (y manejen la inexistencia).
    def test_ventas_por_provincia_inexistente_retorna_cero(self):
        resultado = self.analizador.ventas_por_provincia("NARNIA_NO_EXISTE")
        self.assertEqual(resultado, 0.0, "Debe retornar 0.0 para una provincia inexistente.")

    # 5. Verificar que los valores consultados de 3 provincias sean correctos (validación de cálculo).
    def test_valores_consultados_de_provincias_son_correctos(self):
        
        # Validación 1: PICHINCHA (1000 + 500 = 1500.00)
        pichincha_ventas = self.analizador.ventas_por_provincia('PICHINCHA')
        self.assertAlmostEqual(pichincha_ventas, 1500.00, 2, "El total de ventas para PICHINCHA es incorrecto.")
        
        # Validación 2: GUAYAS (2000 + 100 = 2100.00)
        guayas_ventas = self.analizador.ventas_por_provincia('GUAYAS')
        self.assertAlmostEqual(guayas_ventas, 2100.00, 2, "El total de ventas para GUAYAS es incorrecto.")
        
        # Validación 3: AZUAY (3000.00)
        azuay_ventas = self.analizador.ventas_por_provincia('AZUAY')
        self.assertAlmostEqual(azuay_ventas, 3000.00, 2, "El total de ventas para AZUAY es incorrecto.")

    # -----------------------------------------------
    # PRUEBAS TRABAJO AUTÓNOMO
    # -----------------------------------------------
    
    # 1. Exportaciones totales por mes
    def test_exportaciones_totales_por_mes_calculo_correcto(self):
        # Sumar EXPORTACIONES agrupadas por MES.
        resumen = self.analizador.exportaciones_totales_por_mes()
        
        self.assertIsInstance(resumen, dict, "La exportación por mes debe retornar un diccionario.")
        
        # Validar Mes 01: 500.00 + 200.00 = 700.00
        self.assertAlmostEqual(resumen.get('01'), 700.00, 2, "El total de exportaciones para el mes 01 es incorrecto.")
        
        # Validar Mes 02: 1000.00 + 0.00 (el -10.00 se limpió a 0) = 1000.00
        self.assertAlmostEqual(resumen.get('02'), 1000.00, 2, "El total de exportaciones para el mes 02 es incorrecto.")
167420
    # 3. Provincia con mayor volumen de importaciones
def test_provincia_con_mas_importaciones_identificacion(self):
        # Identificar la provincia con el mayor total de IMPORTACIONES.
        provincia, total = self.analizador.provincia_con_mas_importaciones()
        
        # Importaciones: GUAYAS: 500 + 800 = 1300.00 (MAX)
        
        self.assertEqual(provincia, 'GUAYAS', "La provincia identificada con más importaciones es incorrecta.")
        self.assertAlmostEqual(total, 1300.00, 2, "El total de importaciones para la provincia máxima es incorrecto.")
        self.assertGreater(total, 0.0, "El valor de importaciones debe ser positivo.")

if __name__ == '__main__':
    unittest.main()