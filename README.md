# README

## DESCRIPCIÓN

Este script utiliza el modelo BERT para calcular la similitud entre una tarea y los perfiles de usuario almacenados en una base de datos SQLite. Puede obtener los correos electrónicos de los usuarios y encontrar los tres perfiles más similares a una tarea dada.

## REQUISITOS

Para ejecutar este script, necesitas tener instalados los siguientes paquetes de Python:

- `torch`
- `transformers`
- `scikit-learn`
- `numpy`
- `sqlite3` (incluido en la biblioteca estándar de Python)
- `json` (incluido en la biblioteca estándar de Python)
- `concurrent.futures` (incluido en la biblioteca estándar de Python)

## INSTALACIÓN

Puedes instalar los paquetes necesarios usando `pip`. Ejecuta el siguiente comando en tu terminal:

```bash
pip install torch transformers scikit-learn numpy
```
## USO

### OBTENER CORREOS ELECTRÓNICOS

Para obtener y mostrar los correos electrónicos de los usuarios (excluyendo a los administradores), ejecuta el script con el siguiente comando:

```
python script3.py obtainEmails
```

## CALCULAR SIMILITUD

Para calcular la similitud entre una tarea y los perfiles de usuario, ejecuta el script proporcionando los siguientes parámetros:

- `requiredSkillsNormalized`: Habilidades requeridas normalizadas.
- `requiredExpertiseNormalized`: Experiencia requerida normalizada.
- `descriptionNormalized`: Descripción de la tarea normalizada.

El comando sería:
```
python script3.py <requiredSkillsNormalized> <requiredExpertiseNormalized> <descriptionNormalized>
```
Asegúrate de reemplazar `<requiredSkillsNormalized>`, `<requiredExpertiseNormalized>`, y `<descriptionNormalized>` con los valores correspondientes.

## EJEMPLO
```
python script3.py "Python, SQL" "Data Analysis" "Looking for a data analyst with expertise in Python and SQL."
```
