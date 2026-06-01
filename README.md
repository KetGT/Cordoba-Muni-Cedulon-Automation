# 🏢 Automatización de Cedulones - Municipalidad de Córdoba

Este proyecto es un script de automatización en Python diseñado para optimizar la descarga masiva de cedulones inmobiliarios desde el portal tributario de la Municipalidad de Córdoba. 

Es una herramienta ideal para agilizar tareas administrativas, de gestión de alquileres y conciliación de cuentas, eliminando el trabajo manual repetitivo mediante la extracción segura y unificada de la documentación.

## ✨ Características Principales

* **Lectura de Datos en Lote:** Consume un archivo Excel (`.xlsx`) utilizando `pandas` para obtener las nomenclaturas catastrales a procesar.
* **Navegación Humanizada (Anti-Bot):** Utiliza `playwright` configurado con pausas aleatorias (`random.uniform`) y retrasos de tipeo (`slow_mo`) para emular el comportamiento humano y evitar bloqueos por parte del firewall del servidor.
* **Intercepción Avanzada de Descargas:** Implementa inyección de JavaScript en el navegador para interceptar la generación temporal de archivos PDF (`blob:`) en memoria, convirtiéndolos a Base64 y guardándolos de forma segura en el disco local sin depender de integraciones frágiles.
* **Unificación de Documentos:** Al finalizar el ciclo de descarga, utiliza `PyPDF2` para compilar automáticamente todos los cedulones individuales en un único archivo maestro (`todos_unidos.pdf`) respetando el orden original.

## 📋 Requisitos Previos

Asegúrate de tener instalado [Python 3.8+](https://www.python.org/downloads/) en tu sistema.

Las librerías necesarias para ejecutar este proyecto son:
* `playwright`
* `pandas`
* `openpyxl` (necesario para que pandas lea archivos Excel)
* `PyPDF2`

## 🚀 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/KetGT/Cordoba-Muni-Cedulon-Automation.git](https://github.com/KetGT/Cordoba-Muni-Cedulon-Automation.git)
   cd Cordoba-Muni-Cedulon-Automation

2. **Instalar las dependencias de Python:**
   ```bash
   pip install playwright pandas openpyxl PyPDF2

3. **Instalar los navegadores de Playwright:**
Nota: El script intenta hacer esto automáticamente en su primera ejecución, pero puedes forzarlo manualmente con:
   ```bash
   playwright install chromium


## 📁 Estructura del Archivo Excel de Entrada

El script requiere un archivo en el directorio raíz llamado Municipalidad_Demo.xlsx. El programa extrae los datos específicamente de la columna llamada Municipal.La tabla debe tener un formato similar a este:

## N° Locador Locatario Domicilio Municipal 
## 1 Nombre_Dueño Nombre_Locatario_1 Domicilio_1 01-11-111-111-11111-1
## 2 Nombre_Dueño_2 Nombre_Locatario_2 Domicilio_2 02-22-222-222-22222-2
## 3 Nombre_Dueño_3 Nombre_Locatario_3 Domicilio_3 03-33-333-333-33333-3

El script limpia automáticamente los datos de la columna Municipal, eliminando los guiones (-) y descartando el último dígito verificador para adaptarlo al formato de búsqueda requerido por el portal web.


## 💻 Uso
Una vez configurado el entorno y preparado el archivo Excel, simplemente ejecuta el script principal:

   ```bash
   python main.py
```

## Flujo de ejecución:

1.El script limpiará el directorio /descargas si existen ejecuciones previas.

2.Abrirá una instancia de Chromium visible para poder monitorear el proceso.

3.Iterará sobre cada nomenclatura, procesará la descarga y esperará unos segundos (pausa de seguridad).

4.Al finalizar, encontrarás todos los PDFs individuales en la carpeta /descargas y un archivo unificado llamado todos_unidos.pdf.


## ⚠️ Consideraciones y Responsabilidad
Este script fue creado con fines educativos y de optimización de flujos de trabajo administrativos. El uso de pausas y slow_mo está diseñado explícitamente para no sobrecargar los servidores gubernamentales. Se recomienda ejecutar las descargas masivas en horarios de bajo tráfico web.
