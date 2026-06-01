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