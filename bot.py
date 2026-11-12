
import os
import html
import requests
from flask import Flask, request

TOKEN = os.environ["TELEGRAM_TOKEN"]
URL = f"https://api.telegram.org/bot{TOKEN}"
app = Flask(__name__)

usuarios = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}
    msg = data.get("message", {})
    chat = msg.get("chat", {})
    user = msg.get("from", {})

    if chat.get("type") not in ("group", "supergroup"):
        return "OK"

    if user.get("is_bot"):
        return "OK"

    chat_id = chat["id"]
    user_id = user["id"]
    nombre = user.get("first_name", "Usuario")

    usuarios.setdefault(chat_id, {})[user_id] = nombre

    texto = msg.get("text", "").split()

    if texto and texto[0].split("@")[0].lower() == "/todos":
        miembros = usuarios.get(chat_id, {})
        menciones = [
            f'<a href="tg://user?id={uid}">{html.escape(n)}</a>'
            for uid, n in miembros.items()
        ]

        mensaje = "📢 Atención a todos:\n\n" + " ".join(menciones)

        if len(mensaje) <= 4096:
            requests.post(
                f"{URL}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": mensaje,
                    "parse_mode": "HTML"
                }
            )

    return "OK"

@app.route("/")
def inicio():
    return "Bot ThuGatita activo"
  
