# By: permite indicar CÓMO buscar un elemento en el HTML (por ID, CLASS_NAME, XPATH, etc.)
from selenium.webdriver.common.by import By

# WebDriverWait: espera hasta que se cumpla una condición, con un tiempo máximo
from selenium.webdriver.support.ui import WebDriverWait

# expected_conditions (EC): condiciones listas para usar con la espera
from selenium.webdriver.support import expected_conditions as EC


# "driver" llega desde el fixture de conftest.py (Chrome ya abierto, se cierra solo al terminar)
def test_catalogo(driver):
    # Creamos una espera explícita de hasta 10 segundos
    wait = WebDriverWait(driver, 10)

    # Abrimos la web que vamos a probar
    driver.get("https://www.saucedemo.com/")

    # Localizar elementos del formulario de login por su ID
    usuario = driver.find_element(By.ID, "user-name")
    contraseña = driver.find_element(By.ID, "password")
    boton_login = driver.find_element(By.ID, "login-button")

    # Completar credenciales y hacer click en el login
    usuario.send_keys("visual_user")
    contraseña.send_keys("secret_sauce")
    boton_login.click()

    # Esperamos a que todos los productos del catálogo sean visibles.
    # Devuelve una lista con un elemento por cada producto.
    productos = wait.until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )

    # Verificamos que el título de la pestaña del navegador sea el correcto
    assert driver.title == "Swag Labs"

    # Comprobamos que haya al menos un producto visible
    assert len(productos) > 0

    # Verificamos que el botón del menú esté visible en pantalla
    menu = driver.find_element(By.ID, "react-burger-menu-btn")
    assert menu.is_displayed()

    # Verificamos que el filtro de ordenamiento esté visible en pantalla
    filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")
    assert filtro.is_displayed()

    # Tomamos el primer producto de la lista y leemos su nombre y precio
    primer_producto = productos[0]
    nombre_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text

    # Lo mostramos en la consola (se ve al correr pytest con la opción -s)
    print(f"\nPrimer producto -> Nombre: {nombre_producto} | Precio: {precio_producto}")

    # El nombre no puede estar vacío y el precio tiene que empezar con "$"
    assert nombre_producto != ""
    assert precio_producto.startswith("$")