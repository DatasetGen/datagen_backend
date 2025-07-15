# Datagen Backend Service

**Datagen Backend Service** es el componente servidor de **Datagen**, una plataforma SaaS dedicada a la generación y etiquetado automatizado de datasets mediante Inteligencia Artificial Generativa. Este repositorio contiene la API construida con Django y Django REST Framework, diseñada para facilitar a los usuarios la creación, gestión y exportación de conjuntos de datos listos para entrenar modelos de machine learning.

---

## 📋 Características principales

* Gestión completa de **datasets**, **imágenes**, **etiquetas** y **anotaciones**.
* Operaciones en lote para acelerar el flujo de anotación.
* Creación de **snapshots** de datasets en cualquier momento.
* Asignación de **trabajos** y **batches** de anotación a usuarios.
* Endpoints auxiliares para generar gráficos estadísticos (barras, pasteles) directamente desde la API.
* Panel de administración de Django para supervisión y configuración.

---

## 🚀 Instalación


2. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/tu_org/Datagen-Backend.git
   cd Datagen-Backend
   ```

3. **Configurar entorno virtual**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Variables de entorno**:
   Copia el archivo de ejemplo y ajusta las variables según tu entorno:

   ```bash
   cp .env.example .env
   # Edita .env => SECRET_KEY, DEBUG, DATABASE_URL, ALLOWED_HOSTS, etc.
   ```

6. **Migraciones de base de datos**:

   ```bash
   python manage.py migrate
   ```

7. **Crear superusuario (opcional)**:

   ```bash
   python manage.py createsuperuser
   ```

8. **Levantar el servidor de desarrollo**:

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

La API estará disponible en `http://localhost:8000/api/v1/`.

---

## 🛠️ Uso y pruebas

* **Ejecutar pruebas unitarias**:

  ```bash
  python manage.py test
  ```

* **Contenedorización (Docker)**:
  Construir y levantar contenedores:

  ```bash
  docker build -t datagen-backend .
  docker run -p 8000:8000 --env-file .env datagen-backend
  ```

---

## 📚 Configuración avanzada

* Ajustes clave en `datagen_backend/settings.py`:

  * `SECRET_KEY`
  * `DEBUG`
  * `ALLOWED_HOSTS`
  * Configuración de bases de datos (DATABASES)
* Middleware y CORS (`django-cors-headers`).
* Integración con servicios de almacenamiento de archivos (S3, GCS).

---

## 🔗 Endpoints de la API

A continuación se listan todos los endpoints disponibles, junto con una breve descripción de su funcionalidad.

### 1. Autenticación

| Método | Ruta                             | Descripción                       |
| ------ | -------------------------------- | --------------------------------- |
| POST   | `/api/v1/auth/token/`            | Obtener token de acceso (JWT).    |
| GET    | `/api/v1/auth/user/`             | Detalles del usuario autenticado. |
| GET    | `/api/v1/auth/users/`            | Listado de todos los usuarios.    |
| GET    | `/api/v1/auth/is_authenticated/` | Verificar si el token es válido.  |

### 2. Datasets

| Método                  | Ruta                                                                           | Descripción                                           |
| ----------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------- |
| GET, POST               | `/api/v1/datasets/`                                                            | Listar o crear datasets.                              |
| GET, PUT, PATCH, DELETE | `/api/v1/datasets/{dataset_id}/`                                               | Obtener, actualizar o eliminar un dataset específico. |
| GET, POST               | `/api/v1/datasets/{dataset_id}/labels/`                                        | Listar o crear etiquetas para un dataset.             |
| GET, PUT, PATCH, DELETE | `/api/v1/datasets/{dataset_id}/labels/{label_id}/`                             | Operaciones CRUD sobre una etiqueta.                  |
| GET, POST               | `/api/v1/datasets/{dataset_id}/images/`                                        | Listar o subir imágenes al dataset.                   |
| GET, PUT, PATCH, DELETE | `/api/v1/datasets/{dataset_id}/images/{image_id}/`                             | CRUD de imágenes individuales.                        |
| GET, POST               | `/api/v1/datasets/{dataset_id}/images/{image_id}/annotations/`                 | Listar o agregar anotaciones a una imagen.            |
| POST                    | `/api/v1/datasets/{dataset_id}/images/{image_id}/annotations/batch/`           | Agregar múltiples anotaciones en lote.                |
| GET, PUT, PATCH, DELETE | `/api/v1/datasets/{dataset_id}/images/{image_id}/annotations/{annotation_id}/` | CRUD de anotaciones.                                  |

### 3. Snapshots

| Método                  | Ruta                                                     | Descripción                             |
| ----------------------- | -------------------------------------------------------- | --------------------------------------- |
| GET, POST               | `/api/v1/datasets/{dataset_id}/snapshots/`               | Listar o crear snapshots de un dataset. |
| GET, PUT, PATCH, DELETE | `/api/v1/datasets/{dataset_id}/snapshots/{snapshot_id}/` | Operaciones CRUD sobre un snapshot.     |

### 4. Trabajos y Batches

| Método                  | Ruta                                                       | Descripción                             |
| ----------------------- | ---------------------------------------------------------- | --------------------------------------- |
| GET, POST               | `/api/v1/datasets/{dataset_id}/jobs/`                      | Listar o asignar trabajos de anotación. |
| GET, PUT, PATCH, DELETE | `/api/v1/datasets/{dataset_id}/jobs/{job_id}/`             | CRUD de trabajos individuales.          |
| GET, POST               | `/api/v1/datasets/{dataset_id}/batches/`                   | Listar o crear batches de anotaciones.  |
| GET, PUT, PATCH, DELETE | `/api/v1/datasets/{dataset_id}/batches/{batch_id}/`        | CRUD de batches.                        |
| POST                    | `/api/v1/datasets/{dataset_id}/batches/{batch_id}/assign/` | Asignar un batch a un usuario.          |

### 5. Acciones Extra y Métricas

| Método | Ruta                                               | Descripción                                       |
| ------ | -------------------------------------------------- | ------------------------------------------------- |
| POST   | `/api/v1/datasets/{dataset_id}/generate_snapshot/` | Generar un snapshot completo de un dataset.       |
| GET    | `/api/v1/datasets/{dataset_id}/image_bar_chart/`   | Obtener gráfico de barras con conteo de imágenes. |
| GET    | `/api/v1/datasets/{dataset_id}/image_pie_chart/`   | Obtener gráfico de pastel de imágenes.            |
| GET    | `/api/v1/datasets/{dataset_id}/pie_chart/`         | Gráfico de pastel basado en etiquetas.            |
| GET    | `/api/v1/datasets/{dataset_id}/bar_chart/`         | Gráfico de barras basado en etiquetas.            |

---



## 📞 Contacto

Si tienes dudas o sugerencias, escribe a **josericardopenase@proton.me** o abre un issue en GitHub.
