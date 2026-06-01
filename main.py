import os
import base64
import subprocess
import time
import random
from PyPDF2 import PdfMerger
from playwright.sync_api import sync_playwright
import pandas as pd
from playwright._impl._driver import compute_driver_executable

print("🔍 Driver esperado en:", compute_driver_executable())
DOWNLOAD_DIR = "descargas"

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

def limpiar_descargas():
    if os.path.exists(DOWNLOAD_DIR):
        for archivo in os.listdir(DOWNLOAD_DIR):
            ruta_archivo = os.path.join(DOWNLOAD_DIR, archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
        print(f"🧹 Carpeta '{DOWNLOAD_DIR}' limpiada.")
    else:
        os.makedirs(DOWNLOAD_DIR)
        print(f"📁 Carpeta '{DOWNLOAD_DIR}' creada.")


def unir_pdfs(carpeta, nombre_salida, orden_designaciones):
    merger = PdfMerger()
    archivos_pdf = sorted([
        archivo for archivo in os.listdir(carpeta)
        if archivo.lower().endswith(".pdf")
    ])

    archivos_pdf.sort(key=lambda x: orden_designaciones.index(x.split('.')[0]))

    if not archivos_pdf:
        print("❌ No se encontraron PDFs en la carpeta.")
        return

    for archivo in archivos_pdf:
        ruta = os.path.join(carpeta, archivo)
        try:
            merger.append(ruta)
            print(f"➕ Agregado: {archivo}")
        except Exception as e:
            print(f"⚠️ Error al unir {archivo}: {e}")

    salida = os.path.join(carpeta, nombre_salida)
    merger.write(salida)
    merger.close()
    print(f"✅ PDFs unidos en: {salida}")


# Ahora la función recibe la 'page' y el 'context' activos para no reabrir el navegador
def descargar_archivos(page, context, identificador):
    try:
        # Ir a la web (si ya estamos, la recarga limpia para el siguiente trámite)
        page.goto("https://tributariomuni.cordoba.gob.ar/inmuebles")

        # 1. Rellenar y buscar (con slow_mo va a parecer que alguien tipea)
        page.fill("#search", identificador)
        page.get_by_role("button", name="Buscar").click()
        
        # 2. Esperar el checkbox y tildarlo
        checkbox_maestro = page.locator(".mantine-Checkbox-input").nth(3)
        checkbox_maestro.wait_for(state="visible", timeout=15000)
        checkbox_maestro.check()

        # 3. Inyectar el espía para interceptar el Blob del PDF
        page.evaluate("""
            window.pdfBase64 = null;
            if (!window.blobSpyInstalled) {
                window.originalCreateObjectURL = URL.createObjectURL;
                URL.createObjectURL = function(blob) {
                    if (blob.size > 1000) { 
                        const reader = new FileReader();
                        reader.onloadend = () => {
                            window.pdfBase64 = reader.result.split(',')[1];
                        };
                        reader.readAsDataURL(blob);
                    }
                    return window.originalCreateObjectURL(blob);
                };
                window.blobSpyInstalled = true;
            }
        """)

        # 4. Click en Cedulón y capturar pestaña
        with context.expect_page() as new_page_info:
            page.get_by_role("button", name="Cedulón").click()

        new_page = new_page_info.value
        new_page.wait_for_load_state()
        
        nombre = f"{identificador}.pdf"

        # 5. Extraer datos capturados por el espía
        page.wait_for_function("window.pdfBase64 !== null", timeout=15000)
        base64_pdf = page.evaluate("window.pdfBase64")
        
        ruta = os.path.join(DOWNLOAD_DIR, nombre)
        with open(ruta, "wb") as f:
            f.write(base64.b64decode(base64_pdf))
        print(f"✅ PDF extraído con éxito: {nombre}")
        
        # Cerramos solo la pestaña del PDF flotante
        new_page.close()

    except Exception as e:
        print(f"⚠️ Error al descargar archivos para {identificador}: {e}")


def leer_catastral():
    df = pd.read_excel("Municipalidad_Demo.xlsx")
    numeros = df["Municipal"].dropna().astype(str).tolist()
    
    designaciones = []
    for numero in numeros:
        numero = numero.strip()
        if not numero:
            continue
        designacion = numero[:-1].replace("-", "")
        if not designacion.isdigit():
            continue
        designaciones.append(designacion)
    return designaciones


def main():
    try:
        subprocess.run(["playwright", "install"], check=True)
    except Exception as e:
        print("⚠️ Error instalando navegadores:", e)

    limpiar_descargas()
    dc = leer_catastral()
    
    # Levantar el navegador UNA SOLA VEZ para todo el ciclo
    # slow_mo=1200 agrega 1.2 segundos de delay obligatorio entre acciones de Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1200)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        for i in dc:
            print(f"--- Iniciando trámite para: {i} ---")
            descargar_archivos(page, context, i)
            
            # PAUSA ALEATORIA: Simula el tiempo que le toma a una persona 
            # mirar la pantalla antes de poner el siguiente número.
            tiempo_espera = random.uniform(3.0, 6.5)
            print(f"😴 Pausa de seguridad: esperando {tiempo_espera:.2f} segundos...")
            time.sleep(tiempo_espera)

        browser.close()
    
    # Al final de todo, unir
    unir_pdfs(DOWNLOAD_DIR, "todos_unidos.pdf", dc)


if __name__ == "__main__":
    main()