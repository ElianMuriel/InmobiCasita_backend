# InmobiCasita – API REST Inmobiliaria

Proyecto backend desarrollado en **Django REST Framework** para la gestión de una inmobiliaria ficticia llamada **InmobiCasita**.

Permite administrar **propietarios, clientes, tipos de inmueble, inmuebles, visitas, contratos y pagos**, con autenticación por **JWT** y conexión a **PostgreSQL**.

---

## 1. Tecnologías utilizadas

- Python 3.x
- Django 5
- Django REST Framework
- djangorestframework-simplejwt (JWT)
- PostgreSQL
- psycopg2-binary
- python-dotenv (manejo de variables de entorno)

---

## 2. Estructura del proyecto

- Proyecto Django: `inmobicasita_api`
- App principal: `gestion`
- Base de datos: PostgreSQL

Entidades principales:

- `Rol`
- `Propietario`
- `Cliente`
- `TipoInmueble`
- `Inmueble`
- `Visita`
- `Contrato`
- `Pago`

---

## 3. Configuración e instalación

### 3.1. Clonar el repositorio

- git clone https://github.com/ElianMuriel/InmobiCasita_backend.git

- cd InmobiCasita_backend


### 3.2. Crear y activar entorno virtual
- python -m venv .venv
- .\.venv\Scripts\activate   # para Windows
- source .venv/bin/activate  # para Linux/Mac

### 3.3. Instalar dependencias
pip install -r requirements.txt

### 3.4. Configurar variables de entorno
Creamos un archivo .env y colocamos la informacion solicitada

- SECRET_KEY=django-insecure-XXXXXX# tu secret key
- DB_NAME=DB_nombre # Nombre de la Base de Datos
- DB_USER=Tu_usuario # Tu usuario
- DB_PASSWORD=Tu_contraseña # Tu contraseña
- DB_HOST=localhost
- DB_PORT=5432
- DEBUG=True

### 3.5. Configurar base de datos PostgreSQL
Creamos en PostgreSQL una base de datos con el mismo nombre que colocamos en DB_NAM

### 3.6. Aplicar migraciones
- python manage.py makemigrations
- python manage.py migrate

### 3.7. Crear superusuario

- python manage.py createsuperuser
Completamos la informacion solicitada, nombre, correo y contraseña, para crear al superusuario

### 3.8. Ejecutar servidor
python manage.py runserver

- La api estara en http://127.0.0.1:8000/
- El panel de administracion en http://127.0.0.1:8000/admin/

---

## 4. Autenticación (JWT)

La API utiliza JSON Web Tokens (JWT) con djangorestframework-simplejwt.

### 4.1. Obtener token de acceso (login)

En Postman obtenemos el Token mediante

- POST http://127.0.0.1:8000/api/auth/login/
- body (json)
{
  "username": "usuario_creado",
  "password": "contraseña"
}

Dara una respuesta 
{
  "refresh": "token_refresh_largo",
  "access": "token_access_largo"
}

El access se envia al header
Authorization: Bearer <access_token>

---

## 5. Permisos y roles

Se utiliza una clase de permisos tipo “solo lectura para todos, escritura solo para admin”:

GET (list, retrieve): accesibles sin autenticación.

POST, PUT, PATCH, DELETE: requieren:

- Usuario autenticado con JWT (Authorization: Bearer <access_token>)

- Usuario con is_staff = True (administrador).

En caso de no enviar token o no ser admin:

401 Unauthorized 
o
403 Forbidden

---

## 6. Endpoints principales

Todos los endpoints están bajo el prefijo: /api/

### 6.1. Autenticación

POST /api/auth/login/ → obtener tokens access y refresh.

POST /api/auth/refresh/ → renovar access token.

### 6.2. Roles

GET /api/roles/

GET /api/roles/{id}/

POST /api/roles/ (admin)

PUT/PATCH /api/roles/{id}/ (admin)

DELETE /api/roles/{id}/ (admin)

### 6.3. Propietarios

GET /api/propietarios/

GET /api/propietarios/{id}/

POST /api/propietarios/ (admin)

PUT/PATCH /api/propietarios/{id}/ (admin)

DELETE /api/propietarios/{id}/ (admin)

### 6.4. Clientes

GET /api/clientes/

GET /api/clientes/{id}/

POST /api/clientes/ (admin)

PUT/PATCH /api/clientes/{id}/ (admin)

DELETE /api/clientes/{id}/ (admin)

Filtros por búsqueda:

GET /api/clientes/?search=Quito
GET /api/clientes/?search=COMPRADOR

### 6.5. Tipos de inmueble

GET /api/tipos-inmueble/

GET /api/tipos-inmueble/{id}/

POST /api/tipos-inmueble/ (admin)

PUT/PATCH /api/tipos-inmueble/{id}/ (admin)

DELETE /api/tipos-inmueble/{id}/ (admin)

### 6.6. Inmuebles

GET /api/inmuebles/

GET /api/inmuebles/{id}/

POST /api/inmuebles/ (admin)

PUT/PATCH /api/inmuebles/{id}/ (admin)

DELETE /api/inmuebles/{id}/ (admin)

### 6.7. Contratos

GET /api/contratos/

GET /api/contratos/{id}/

POST /api/contratos/ (admin)

PUT/PATCH /api/contratos/{id}/ (admin)

DELETE /api/contratos/{id}/ (admin)

### 6.8. Pagos

GET /api/pagos/

GET /api/pagos/{id}/

POST /api/pagos/ (admin)

PUT/PATCH /api/pagos/{id}/ (admin)

DELETE /api/pagos/{id}/ (admin)

### 6.9. Visitas

GET /api/visitas/

GET /api/visitas/{id}/

POST /api/visitas/ (admin)

PUT/PATCH /api/visitas/{id}/ (admin)

DELETE /api/visitas/{id}/ (admin)

---

## 7. Manejo de errores

Ejemplos de respuestas de error:

### 7.1. 400 – Bad Request (datos inválidos)
{
  "identificacion": [
    "Este campo debe ser único."
  ]
}

### 7.2. 401 – Unauthorized (sin token)
{
  "detail": "Authentication credentials were not provided."
}

### 7.3. 403 – Forbidden (usuario sin permisos)
{
  "detail": "You do not have permission to perform this action."
}

### 7.4. 404 – Not Found
{
  "detail": "Not found."
}

---

## 8. Colección Postman

En la raíz del proyecto se incluye el archivo:

InmobiCasita_API.postman_collection.json

La colección contiene:

- Request de login (POST /api/auth/login/).

- Endpoints GET, POST, PUT/PATCH, DELETE para:

- propietarios

- clientes

- tipos de inmueble

- inmuebles

- contratos

- pagos

- visitas

Para importar en Postman:

Abrir Postman → Import.

Seleccionar InmobiCasita_API.postman_collection.json.

Seleccionar el environment con:

- base_url = http://127.0.0.1:8000

- access_token (token JWT obtenido desde login).
