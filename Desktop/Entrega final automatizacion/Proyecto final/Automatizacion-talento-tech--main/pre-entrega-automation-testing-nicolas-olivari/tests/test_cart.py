# By: permite indicar CÓMO buscar un elemento en el HTML (por ID, CLASS_NAME, TAG_NAME, etc.)
from selenium.webdriver.common.by import By

# WebDriverWait: espera hasta que se cumpla una condición, con un tiempo máximo
from selenium.webdriver.support.ui import WebDriverWait

# expected_conditions (EC): condiciones listas para usar con la espera
from selenium.webdriver.support import expected_conditions as EC


# "driver" llega desde el fixture de conftest.py (Chrome ya abierto, se cierra solo al terminar)
def test_cart(driver):
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

    # Esperamos a que el primer producto del catálogo sea visible
    primer_producto = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item"))
    )

    # Guardamos el nombre del producto para compararlo después en el carrito
    nombre_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text

    # Buscamos el botón "Add to cart" dentro del producto y hacemos click
    boton_agregar = primer_producto.find_element(By.TAG_NAME, "button")
    boton_agregar.click()

    # Esperamos a que aparezca el numerito rojo sobre el ícono del carrito
    contador_carrito = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )

    # Validamos que el contador marque 1 producto
    assert contador_carrito.text == "1"

    # Esperamos a que el ícono del carrito se pueda clickear y entramos al carrito
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()

    # Leemos el nombre del producto que aparece dentro del carrito
    nombre_producto_carrito = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
    ).text

    # Validación final: el producto del carrito es el mismo que agregamos
    assert nombre_producto == nombre_producto_carrito