
# Sistema para compartir sets de datos

Esta es la primera tarea programada de ITCR del curso de base de datos 2, en ella se comparten sets de datos (datasets) con información variada, el sistema usa 4 bases de datos distintas para alcanzar dicho objetivo

## Funcionalidades

El sistema puede cargar datasets, clonar datasets, los usuarios pueden comentar en los datasets y contestar comentarios, y los usuarios pueden cambiar su perfil. Los usuarios tambien pueden subscribirse a otros usuarios y ver sus datasets

## Requerimientos

Se requiere, al menos a la fecha de haber creado el sistema:

Bases de datos:

- Raven (5.4)
- Neo4j (5.6.0)
- MariaDB (10.11.2)
- MongoDB (6.0.5)

Software:

- Python 3.10
- Poetry

Se usa Poetry para lo que es el manejo de las dependencias del proyecto, todas las dependencias están dentro del archivo `pyproject.toml`. Solo basta con clonar el repositorio y correr el siguiente commando:

```sh
$ poetry install
```

Quien quiera correr la aplicación también debe tener un conocimiento básico de django, correr las migraciones en MariaDB y correr la aplicación.

## Razones tras la base de datos

**RavenDB**: Se pueden guardar archivos fácilmente y agregar datos de forma sencilla, se pueden adjuntar multiples archivos a un solo documento, se puede usar clases para abstraer sus atributos.
**Neo4j**: Excelenete para manejo de mensajes debido a su sistema de nodos, se vincularon los comentarios con los datastes, y las respuestas con los comentarios, se pueden usar clases también para abstraer sus atributos.
**MaridaDB**: Robusta base de datos SQL, simple y bien conocida, ya sabía usarla.
**MongoDB**: Se pueden manejar documentos de forma rápida, la estructura flexible ayuda a crear datos rápidos
