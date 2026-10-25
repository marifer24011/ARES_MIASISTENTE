
# ARES – Mi Asistente

Plataforma web de asistencia en trámites escolares para los estudiantes del TSJ.

## Objetivo

Facilitar la consulta de información, requisitos y seguimiento de trámites escolares mediante una plataforma web con un asistente interactivo.

## Tecnologías

- Python
- FastAPI
- MySQL 8.4
- phpMyAdmin
- Docker y Docker Compose
- Git y GitHub
- HTML

## Integrantes y ramas

| Integrante | Rama |
|------------|------|
| Marifer | desarrollo-marifer |
| Alma | desarrollo-alma |
| Dylan | desarrollo-dylan |
| Sergio | desarrollo-sergio |

Rama principal: `main`.

## Requisitos previos

Instalar:

- Git
- Docker Desktop
- Visual Studio Code (recomendado)

Docker Desktop debe estar iniciado antes de ejecutar el proyecto.

## Instalación

### 1. Clonar el repositorio

git clone https://github.com/marifer24011/ARES_MIASISTENTE.git

### 2. Entrar a la carpeta

cd ARES_MIASISTENTE

### 3. Cambiar a la rama personal

Ejemplo para Alma:

git switch desarrollo-alma

Cada integrante debe seleccionar su propia rama.

### 4. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto tomando como referencia `.env.example`.

Definir contraseñas propias para:

- MYSQL_ROOT_PASSWORD
- MYSQL_PASSWORD

No compartir ni subir `.env` a GitHub.

### 5. Iniciar Docker

docker compose up -d --build

### 6. Comprobar los servicios

docker compose ps

## Acceso a los servicios

FastAPI:
http://localhost:8000

phpMyAdmin:
http://localhost:8081

Base de datos: ares_db

Usuario de MySQL: ares_user

La contraseña es la definida en MYSQL_PASSWORD.

## Detener los servicios

docker compose down

Este comando detiene y elimina los contenedores del proyecto, pero conserva el volumen de MySQL.

No utilizar `docker compose down -v` salvo que se quiera eliminar también la información de la base de datos.

## Organización del proyecto

- backend/: Servidor Python y FastAPI.
- frontend/: Interfaz web.
- database/: Archivos relacionados con la base de datos.
- docs/: Documentación técnica.
- tests/: Pruebas del sistema.

## Trabajo colaborativo

Cada integrante debe desarrollar en su rama personal.

Antes de incorporar cambios a main, se debe crear un Pull Request para su revisión.

No subir contraseñas, entornos virtuales ni archivos privados.
