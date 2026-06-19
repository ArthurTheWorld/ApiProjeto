"""
API Backend - Cadastro e Listagem de Usuários
Trabalho Prático: Docker, MySQL, Nginx e Wireshark
"""

import os
import time

import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "mysql"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "root"),
    "database": os.environ.get("DB_NAME", "appdb"),
}


def get_connection():
    """Cria e retorna uma conexão com o banco MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


def wait_for_db(max_retries=20, delay=3):
    """
    Aguarda o MySQL ficar disponível antes de iniciar a API.
    Necessário pois o container do MySQL pode demorar para aceitar conexões,
    mesmo após o docker-compose iniciar o container.
    """
    for attempt in range(1, max_retries + 1):
        try:
            conn = get_connection()
            conn.close()
            print("Conexão com MySQL estabelecida com sucesso.")
            return
        except mysql.connector.Error as err:
            print(f"Tentativa {attempt}/{max_retries}: MySQL ainda não disponível ({err}).")
            time.sleep(delay)
    raise RuntimeError("Não foi possível conectar ao MySQL após várias tentativas.")


def init_db():
    """Cria a tabela 'users' caso ela não exista."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(120) NOT NULL,
            email VARCHAR(160) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


@app.route("/health", methods=["GET"])
def health():
    """Endpoint simples de verificação de saúde da API."""
    return jsonify({"status": "ok"}), 200


@app.route("/users", methods=["GET"])
def list_users():
    """Lista todos os usuários cadastrados."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY id DESC;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    for user in users:
        if user.get("created_at") is not None:
            user["created_at"] = user["created_at"].isoformat()

    return jsonify(users), 200


@app.route("/users", methods=["POST"])
def create_user():
    """Cadastra um novo usuário. Espera JSON: {"name": "...", "email": "..."}"""
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()

    if not name or not email:
        return jsonify({"error": "Os campos 'name' e 'email' são obrigatórios."}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s);",
            (name, email),
        )
        conn.commit()
        new_id = cursor.lastrowid
    except mysql.connector.IntegrityError:
        cursor.close()
        conn.close()
        return jsonify({"error": "E-mail já cadastrado."}), 409
    finally:
        cursor.close()
        conn.close()

    return jsonify({"id": new_id, "name": name, "email": email}), 201


if __name__ == "__main__":
    wait_for_db()
    init_db()
    app.run(host="0.0.0.0", port=5000)