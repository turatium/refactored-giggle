from flask import Flask, redirect, render_template, request, jsonify
import sqlite3
from helpers import SQLiteDatabase, query

program = SQLiteDatabase("static/program.db")
users = SQLiteDatabase("static/users.db")
app = Flask(__name__)

@app.route("/")
def index():
    sessions = query(program, "SELECT * FROM sessions", fetch=True)
    presentations = query(program, "SELECT * FROM presentations", fetch=True)
    return render_template("index.html", sessions=sessions, presentations=presentations)


@app.route("/thesis")
def thesis():
    return render_template("thesis.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    sessions = query(program, "SELECT * FROM sessions", fetch=True)
    return render_template("edit.html", sessions=sessions)


@app.route("/addpresentation", methods=["POST"])
def addpresentation():
    name = request.form["presentation_name"]
    authors = request.form["authors"]
    session_id = request.form["session_id"]
    query(program, "INSERT INTO presentations(name, authors, session_id, likes) VALUES (?, ?, ?, 0)",
          (name, authors, session_id,))
    return redirect("/edit")


@app.route("/addsession", methods=["POST"])
def addsession():
    name = request.form["session_name"]
    query(program, "INSERT INTO sessions(name) VALUES (?)", (name,))
    return redirect("/edit")


@app.route("/like", methods=["POST"])
def like():
    data = request.get_json()
    presentation_id = data.get('id')
    fingerprint = data.get('fingerprint')

    if not presentation_id or not fingerprint:
        return jsonify({'error': 'id and fingerprint are required'}), 400

    # Проверяем, лайкал ли пользователь этот доклад ранее
    liked = query(users, "SELECT id FROM liked WHERE fingerprint_id = (SELECT id FROM users WHERE fingerprint = ?) AND presentation_id = ?",
                  (fingerprint, presentation_id), fetch=True)

    if liked is None:
        return jsonify({'error': 'Database error'}), 500

    if liked:  # Если пользователь уже лайкал этот доклад
        return jsonify({'error': 'User already liked this presentation'}), 400

    # Добавляем лайк в таблицу liked
    query(users, "INSERT INTO liked (fingerprint_id, presentation_id) VALUES ((SELECT id FROM users WHERE fingerprint = ?), ?)",
          (fingerprint, presentation_id))

    # Увеличиваем количество лайков в таблице presentations
    query(program, "UPDATE presentations SET likes = likes + 1 WHERE id = ?", (presentation_id,))

    return jsonify({"status": "success"}), 200


@app.route("/dislike", methods=["POST"])
def dislike():
    data = request.get_json()
    presentation_id = data.get('id')
    fingerprint = data.get('fingerprint')

    if not presentation_id or not fingerprint:
        return jsonify({'error': 'id and fingerprint are required'}), 400

    # Проверяем, лайкал ли пользователь этот доклад ранее
    liked = query(users, "SELECT id FROM liked WHERE fingerprint_id = (SELECT id FROM users WHERE fingerprint = ?) AND presentation_id = ?",
                  (fingerprint, presentation_id), fetch=True)

    if liked is None:
        return jsonify({'error': 'Database error'}), 500

    if not liked:  # Если пользователь не лайкал этот доклад
        return jsonify({'error': 'User did not like this presentation'}), 400

    # Удаляем лайк из таблицы liked
    query(users, "DELETE FROM liked WHERE fingerprint_id = (SELECT id FROM users WHERE fingerprint = ?) AND presentation_id = ?",
          (fingerprint, presentation_id))

    # Уменьшаем количество лайков в таблице presentations
    query(program, "UPDATE presentations SET likes = likes - 1 WHERE id = ?", (presentation_id,))

    return jsonify({"status": "success"}), 200


@app.route("/save_fingerprint", methods=["POST"])
def save_fingerprint():
    data = request.get_json()
    fingerprint = data['fingerprint']
    try:
        query(users, "INSERT INTO users (fingerprint) VALUES (?)", (fingerprint, ))
        return jsonify({"status": "success"}), 200
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Fingerprint is required'}), 400


@app.route("/get_likes", methods=["GET"])
def get_likes():
    fingerprint = request.args.get('fingerprint')
    if not fingerprint:
        return jsonify({'error': 'fingerprint is required'}), 400

    # Получаем список лайков пользователя
    liked = query(users, "SELECT presentation_id FROM liked WHERE fingerprint_id = (SELECT id FROM users WHERE fingerprint = ?)",
                  (fingerprint,), fetch=True)

    if liked is None:
        return jsonify({'error': 'Database error'}), 500

    print("Liked presentations from DB:", liked)  # Логирование данных из базы данных

    # Формируем список presentation_id
    liked_presentations = [str(item['presentation_id']) for item in liked]  # Приводим к строке
    print("Processed liked presentations:", liked_presentations)  # Логирование обработанных данных

    return jsonify({'likedPresentations': liked_presentations})

@app.route("/results", methods=["GET"])
def results():
    sessions = query(program, "SELECT * FROM sessions", fetch=True)
    presentations = query(program, "SELECT * FROM presentations ORDER BY likes DESC", fetch=True)
    return render_template ("results.html", sessions=sessions, presentations=presentations)

if __name__ == '__main__':
    app.run(debug=False)
