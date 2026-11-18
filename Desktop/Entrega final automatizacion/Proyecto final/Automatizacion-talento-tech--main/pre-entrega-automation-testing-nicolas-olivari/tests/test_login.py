# By: permite indicar CÓMO buscar un elemento en el HTML (por ID, CLASS_NAME, XPATH, etc.)
from selenium.webdriver.common.by import By

# WebDriverWait: espera hasta que se cumpla una condición, con un tiempo máximo
from selenium.webdriver.support.ui import WebDriverWait

# expected_conditions (EC): condiciones listas para usar con la espera
# (que un elemento sea visible, que la URL cambie, etc.)
from selenium.webdriver.support import expected_conditions as EC


# "driver" como parámetro hace que pytest llame al fixture de conftest.py:
# el test recibe un Chrome ya abierto y no tiene que cerrarlo él mismo.
def test_login_exitoso(driver):
    # Abrimos la web que vamos a probar
    driver.get("https://www.saucedemo.com/")

    # Localizar elementos del formulario de login por su ID
    # y guardarlos en variables para poder reutilizarlos
    usuario = driver.find_element(By.ID, "user-name")
    contraseña = driver.find_element(By.ID, "password")
    boton_login = driver.find_element(By.ID, "login-button")

    # Completar el formulario: escribimos usuario y contraseña
    usuario.send_keys("visual_user")
    contraseña.send_keys("secret_sauce")

    # Hacer click en el botón de login
    boton_login.click()

    # Creamos una espera de hasta 10 segundos (se reutiliza más abajo)
    wait = WebDriverWait(driver, 10)

    # Validación del login: esperamos a que la URL sea la del inventario.
    # Si en 10 segundos no cambia, el test falla. Así no dependemos de que
    # la página cargue justo en el instante en que el test la mira.
    wait.until(EC.url_to_be("https://www.saucedemo.com/inventory.html"))

    # Validamos también que aparezca el título "Products" en la página:
    # esperamos a que sea visible y guardamos el elemento
    titulo_products = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )

    # Validación final: el texto del título tiene que ser "Products"
    assert titulo_products.text == "Products"