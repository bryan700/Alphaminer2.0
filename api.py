from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "data/database.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/save_balance", methods=["POST"])
def save_balance():

    data = request.json

    user_id = data.get("user_id")
    balance = data.get("balance")

    conn = get_db()

    conn.execute(
        "UPDATE users SET balance = ? WHERE user_id = ?",
        (balance, user_id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "balance": balance
    })


@app.route("/get_balance/<int:user_id>")
def get_balance(user_id):

    conn = get_db()

    user = conn.execute(
        "SELECT balance FROM users WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    if user:
        return jsonify({
            "balance": user["balance"]
        })

    return jsonify({
        "balance": 0
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
