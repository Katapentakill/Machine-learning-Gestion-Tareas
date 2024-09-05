import sys
import sqlite3
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from concurrent.futures import ThreadPoolExecutor

# Cargar el modelo y el tokenizer de BERT globalmente para evitar recarga repetida
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_bert_embedding(text):
    """
    Obtiene el embedding de BERT para un texto dado.

    Args:
        text (str): Texto para el cual obtener el embedding.

    Returns:
        np.ndarray: Embedding de BERT para el texto proporcionado.
    """
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

def calculate_similarity(task_embedding, user_embedding):
    """
    Calcula la similitud entre el embedding de una tarea y el embedding de un perfil de usuario.

    Args:
        task_embedding (np.ndarray): Embedding de la tarea.
        user_embedding (np.ndarray): Embedding del perfil de usuario.

    Returns:
        float: Similaridad calculada usando la similitud del coseno.
    """
    return cosine_similarity(task_embedding, user_embedding)[0][0]

def print_emails():
    """
    Imprime los emails de los usuarios obtenidos de la base de datos.
    """
    db_path = r"D:\\Ale\\Recomend System\\Port-backend-nestjs\\database.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT u.email
        FROM user u
        JOIN role r ON u.roleId = r.id
        WHERE r.name != 'Admin'
    ''')
    rows = cursor.fetchall()

    print("Emails de los usuarios obtenidos de la base de datos:")
    for row in rows:
        print(row[0])  # Imprimir el email

    conn.close()

def main(requiredSkillsNormalized, requiredExpertiseNormalized, descriptionNormalized):
    """
    Función principal que gestiona la conexión a la base de datos, consulta los perfiles de usuarios,
    calcula las similitudes y genera un resultado JSON con los usuarios más similares.

    Args:
        requiredSkillsNormalized (str): Habilidades requeridas normalizadas.
        requiredExpertiseNormalized (str): Experiencia requerida normalizada.
        descriptionNormalized (str): Descripción de la tarea normalizada.
    """
    # Conectar a la base de datos SQLite
    db_path = r"D:\\Ale\\Recomend System\\Port-backend-nestjs\\database.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Consultar los perfiles de los usuarios, excluyendo a los que tienen rol "Admin"
    cursor.execute('''
        SELECT u.name, u.lastname, u.email, u.job, u.curriculum, u.curriculumNormalized, u.skillsNormalized, u.expertiseNormalized
        FROM user u
        JOIN role r ON u.roleId = r.id
        WHERE r.name != 'Admin'
    ''')
    rows = cursor.fetchall()

    # Formatear los perfiles de usuarios para el cálculo de similitud
    user_profiles = [
        {
            'name': f"{row[0]} {row[1]}",
            'job': row[3],
            'skills': row[6],
            'expertise': row[7],
            'curriculum': row[4],
            'curriculumNormalized': row[5]
        }
        for row in rows
    ]

    # Obtener el embedding de la tarea
    task_embedding = get_bert_embedding(descriptionNormalized + ' ' + requiredExpertiseNormalized + ' ' + requiredSkillsNormalized)

    # Calcular similitudes
    def calculate_profile_similarity(profile):
        profile_text = profile['skills'] + ' ' + profile['expertise'] + ' ' + profile['curriculumNormalized']
        profile_embedding = get_bert_embedding(profile_text)
        _similarity = calculate_similarity(task_embedding, profile_embedding)
        return _similarity

    # Usar ThreadPoolExecutor para paralelizar el cálculo de similitudes
    with ThreadPoolExecutor() as executor:
        similarities = list(executor.map(calculate_profile_similarity, user_profiles))

    # Encontrar los tres usuarios con mayor similitud
    top_indices = np.argsort(similarities)[-3:][::-1]
    top_users = [user_profiles[i]['name'] for i in top_indices]
    top_emails = [rows[i][2] for i in top_indices]  # Obtener los emails de los usuarios
    top_curriculums = [user_profiles[i]['curriculum'] for i in top_indices]  # Obtener los currículums de los usuarios
    top_similarities = [similarities[i] * 100 for i in top_indices]  # Convertir a porcentaje

    # Crear un resultado JSON
    result = [
        {
            'user': top_users[i],
            'email': top_emails[i],
            'curriculum': top_curriculums[i],
            'similarity': top_similarities[i]  # Porcentaje de similitud
        }
        for i in range(3)
    ]

    # Imprimir el resultado en formato JSON
    print(json.dumps(result, indent=2))

    # Cerrar la conexión a la base de datos
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "obtainEmails":
            print_emails()
        elif len(sys.argv) > 3:
            requiredSkillsNormalized = sys.argv[1]
            requiredExpertiseNormalized = sys.argv[2]
            descriptionNormalized = sys.argv[3]
            main(requiredSkillsNormalized, requiredExpertiseNormalized, descriptionNormalized)
        else:
            print("Faltan argumentos. Proporcione requiredSkillsNormalized, requiredExpertiseNormalized y descriptionNormalized.")
    else:
        print("Debe especificar un argumento. Use 'obtainEmails' para imprimir los emails o proporcione los parámetros necesarios para ejecutar la función principal.")
