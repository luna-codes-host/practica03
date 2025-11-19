import csv
from collections import defaultdict
import os

class Analizador:
    # Definimos el separador y la lista de campos que necesitan limpieza numérica
    CAMPOS_NUMERICOS_CLAVE = ["TOTAL_VENTAS", "EXPORTACIONES", "IMPORTACIONES", "VENTAS_NETAS_TARIFA_0"] 

    def __init__(self, ruta_csv, separador='|'):
        # Usamos '|' como separador según tu código original
        self.ruta_csv = ruta_csv
        self.separador = separador
        # Leemos el archivo CSV y guardamos los datos ya limpios en memoria
        self.datos = self.leer_csv()

    def _limpiar_valor_numerico(self, valor):
        """Convierte una cadena a flotante, asegurando que el resultado no sea negativo (>= 0.0)."""
        if valor is None:
            return 0.0
        try:
            # Reemplazamos comas por puntos si el CSV usa formato europeo (opcional)
            valor = str(valor).replace(',', '.') 
            num = float(valor)
            # Requisito de la práctica: asegurar que el valor calculado NO sea negativo.
            return max(0.0, num) 
        except (ValueError, TypeError):
            return 0.0

    def leer_csv(self):
        """Lee el archivo CSV, limpia los valores numéricos de campos clave y devuelve una lista de filas."""
        datos_limpios = []
        
        if not os.path.exists(self.ruta_csv):
            print(f"Advertencia: Archivo no encontrado en {self.ruta_csv}. Retornando lista vacía.")
            return datos_limpios
            
        try:
            with open(self.ruta_csv, "r", encoding="utf-8") as archivo:
                # Usar el separador definido
                lector = csv.DictReader(archivo, delimiter=self.separador) 
                
                for fila in lector:
                    # 1. Normalizar el campo PROVINCIA a mayúsculas para búsquedas consistentes
                    fila["PROVINCIA"] = fila.get("PROVINCIA", "DESCONOCIDA").upper() 
                    
                    # 2. Aplicar limpieza y conversión a todos los campos numéricos clave
                    for campo in self.CAMPOS_NUMERICOS_CLAVE:
                        valor_limpio = self._limpiar_valor_numerico(fila.get(campo))
                        fila[campo] = valor_limpio
                    
                    datos_limpios.append(fila)
                    
        except Exception as e:
            print(f"Error durante la lectura del archivo CSV: {e}")
            return []
            
        return datos_limpios

    # --- Funciones Base (Paso 2) ---

    def ventas_totales_por_provincia(self):
        """Devuelve un diccionario con el total de ventas por provincia."""
        # Usamos defaultdict para un código más limpio y eficiente
        totales = defaultdict(float)

        for fila in self.datos:
            provincia = fila["PROVINCIA"]
            # El valor ya es float y limpio gracias a leer_csv()
            total_venta = fila["TOTAL_VENTAS"] 

            totales[provincia] += total_venta

        return dict(totales)

    def ventas_por_provincia(self, nombre):
        """Devuelve el total de ventas de una provincia específica. Retorna 0.0 si no existe."""
        
        # Normalizar el nombre de la provincia para coincidir con los datos internos (MAYÚSCULAS)
        nombre_normalizado = nombre.upper() 
        
        # Generar los totales (si no se tiene un cache)
        totales = self.ventas_totales_por_provincia()

        # Usar .get() para retornar 0.0 si la provincia no existe (cumple requisito de prueba)
        return totales.get(nombre_normalizado, 0.0)

    # --- Funciones de Trabajo Autónomo (Extensión) ---

    # [cite_start]1. Exportaciones totales por mes [cite: 94]
    def exportaciones_totales_por_mes(self):
        """Suma las EXPORTACIONES agrupadas por MES."""
        exportaciones_por_mes = defaultdict(float)
        
        for fila in self.datos:
            mes = fila.get("MES")
            exportaciones = fila.get("EXPORTACIONES", 0.0)
            
            if mes: 
                exportaciones_por_mes[mes] += exportaciones
                
        return dict(exportaciones_por_mes)

    # [cite_start]3. Provincia con mayor volumen de importaciones [cite: 97]
    def provincia_con_mas_importaciones(self):
        """Identifica la provincia con el mayor total de IMPORTACIONES."""
        importaciones_por_provincia = defaultdict(float)
        
        for fila in self.datos:
            provincia = fila.get("PROVINCIA")
            importaciones = fila.get("IMPORTACIONES", 0.0)
            
            if provincia:
                importaciones_por_provincia[provincia] += importaciones
        
        if not importaciones_por_provincia:
            return None, 0.0 # Retorna None si no hay datos
            
        # Encontrar la provincia con el máximo valor (MAX Key por su valor)
        provincia_max = max(importaciones_por_provincia, key=importaciones_por_provincia.get)
        total_max = importaciones_por_provincia[provincia_max]
        
        return provincia_max, total_max

    # 2. Porcentaje de ventas con tarifa 0% (Opcional, si eliges esta en lugar de la 3)
    def porcentaje_ventas_tarifa_cero(self):
        """Calcula el porcentaje de ventas con tarifa 0% respecto al total por provincia."""
        ventas_cero_por_provincia = defaultdict(float)
        ventas_totales_por_provincia = defaultdict(float)
        
        for fila in self.datos:
            provincia = fila.get("PROVINCIA")
            vta_cero = fila.get("VENTAS_NETAS_TARIFA_0", 0.0)
            vta_total = fila.get("TOTAL_VENTAS", 0.0)
            
            if provincia:
                ventas_cero_por_provincia[provincia] += vta_cero
                ventas_totales_por_provincia[provincia] += vta_total
        
        porcentajes = {}
        for provincia, total_ventas in ventas_totales_por_provincia.items():
            ventas_cero = ventas_cero_por_provincia[provincia]
            if total_ventas > 0:
                porcentaje = (ventas_cero / total_ventas) * 100
                porcentajes[provincia] = porcentaje
            else:
                porcentajes[provincia] = 0.0 # 0% si no hay ventas totales
                
        return porcentajes