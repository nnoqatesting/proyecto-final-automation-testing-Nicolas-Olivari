# conftest.py
# Archivo especial de pytest: lo lee solo, sin importarlo, y sirve para
# compartir fixtures y "hooks" entre todos los tests del proyecto.

# re: para limpiar el nombre del test (quitar caracteres raros del nombre de archivo)
import re

# datetime: para ponerle fecha y hora al nombre de cada captura
from datetime import datetime

# Path: forma cómoda de armar rutas de carpetas y archivos
from pathlib import Path

# pytest: la librería de testing; la necesitamos para declarar fixtures y hooks
import pytest

# webdriver: la herramienta de Selenium que controla el navegador
from selenium import webdriver

# extras: permite agregar contenido extra (como imágenes) al reporte de pytest-html
from pytest_html import extras


# Carpeta donde se guardan las capturas: reports/screenshots/ (junto a este archivo).
# Usar __file__ hace que funcione aunque corras pytest desde otra carpeta.
CARPETA_CAPTURAS = Path(__file__).parent / "reports" / "screenshots"


# @pytest.fixture marca esta función como un "fixture": un test puede pedirlo
# escribiendo su nombre ("driver") como parámetro, y pytest se lo entrega.
@pytest.fixture
def driver():
    # PREPARACIÓN (antes del test): abrimos una ventana nueva de Chrome
    driver = webdriver.Chrome()

    # yield entrega el driver al test y pausa esta función acá.
    # Mientras tanto, el test corre usando ese navegador.
    yield driver

    # LIMPIEZA (después del test): se ejecuta siempre, el test pase o falle.
    # Cierra el navegador y libera la memoria.
    driver.quit()


# Hook de pytest: se ejecuta cada vez que pytest arma el resultado de un test.
# hookwrapper=True nos deja "envolver" ese proceso: primero lo dejamos correr
# (yield) y después modificamos el resultado ya armado.
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Dejamos que pytest arme el resultado normal del test
    outcome = yield
    reporte = outcome.get_result()

    # Un test tiene 3 fases (setup, call, teardown). Nos interesa "call",
    # que es cuando corre el test en sí, y solo si falló.
    if reporte.when == "call" and reporte.failed:
        # Buscamos el driver entre los fixtures que usó este test.
        # Los tests de API no lo usan, así que en esos devuelve None y no hacemos nada.
        driver = item.funcargs.get("driver")

        if driver is not None:
            # Nombre del archivo: fecha_hora + nombre del test.
            # re.sub reemplaza todo lo que no sea letra, número o guion por "_".
            fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_test = re.sub(r"[^\w\-]", "_", item.name)
            nombre_archivo = f"{fecha_hora}_{nombre_test}.png"

            # Creamos la carpeta de capturas si todavía no existe
            CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)

            # Guardamos la captura como archivo .png en esa carpeta
            driver.save_screenshot(str(CARPETA_CAPTURAS / nombre_archivo))

            # Pedimos la misma captura en base64 (la imagen como texto) para
            # poder incrustarla dentro del reporte HTML autocontenido.
            captura_base64 = driver.get_screenshot_as_base64()

            # Agregamos la imagen a los "extras" de este resultado en el reporte
            reporte.extras = getattr(reporte, "extras", []) + [
                extras.image(captura_base64)
            ]