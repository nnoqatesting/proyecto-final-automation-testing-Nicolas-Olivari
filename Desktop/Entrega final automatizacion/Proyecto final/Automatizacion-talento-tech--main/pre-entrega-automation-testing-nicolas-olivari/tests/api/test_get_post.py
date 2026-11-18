import requests

# Dirección base de la API pública que vamos a probar
URL_BASE = "https://jsonplaceholder.typicode.com"


def test_obtener_post_existente():
    # Hacemos una petición GET al post número 1
    respuesta = requests.get(f"{URL_BASE}/posts/1", timeout=10)

    # Verificamos el código de estado HTTP: 200 significa "OK"
    assert respuesta.status_code == 200

    # Convertimos el cuerpo de la respuesta (JSON) en un diccionario de Python
    datos = respuesta.json()

    # Verificamos que el post traiga los campos esperados
    assert datos["id"] == 1
    assert "title" in datos
    assert "body" in datos
    assert "userId" in datos

def test_crear_post():
    # Datos del post nuevo que vamos a enviar
    nuevo_post = {
        "title": "Mi primer post",
        "body": "Contenido de prueba",
        "userId": 1,
    }

    # Petición POST: enviamos los datos en formato JSON
    respuesta = requests.post(f"{URL_BASE}/posts", json=nuevo_post, timeout=10)

    # 201 significa "Created": el recurso se creó
    assert respuesta.status_code == 201

    datos = respuesta.json()

    # La API devuelve lo que enviamos, más un id asignado
    assert datos["title"] == nuevo_post["title"]
    assert datos["body"] == nuevo_post["body"]
    assert datos["userId"] == nuevo_post["userId"]
    assert "id" in datos

def test_eliminar_post():
    # Petición DELETE: pedimos eliminar el post número 1
    respuesta = requests.delete(f"{URL_BASE}/posts/1", timeout=10)

    # 200 significa que la API aceptó el pedido
    assert respuesta.status_code == 200

    # JSONPlaceholder responde con un JSON vacío al eliminar
    assert respuesta.json() == {}

def test_obtener_post_inexistente():
    # Pedimos un post con un id que no existe
    respuesta = requests.get(f"{URL_BASE}/posts/999999", timeout=10)

    # 404 significa "Not Found": el recurso no existe
    assert respuesta.status_code == 404

def test_encadenado_usuario_y_sus_posts():
    # Paso 1: obtenemos un usuario
    resp_usuario = requests.get(f"{URL_BASE}/users/1", timeout=10)
    assert resp_usuario.status_code == 200
    id_usuario = resp_usuario.json()["id"]

    # Paso 2: usamos ese id para pedir los posts de ese usuario
    resp_posts = requests.get(f"{URL_BASE}/posts", params={"userId": id_usuario}, timeout=10)
    assert resp_posts.status_code == 200

    posts = resp_posts.json()

    # Verificamos que haya posts y que todos pertenezcan a ese usuario
    assert len(posts) > 0
    for post in posts:
        assert post["userId"] == id_usuario