from flask import Blueprint, render_template
from flask import request, redirect
import re
import time
from .consultas import ConsultaDados

kryptacode_bp = Blueprint("kryptacode", __name__)

def public_endpoint(function):
    """Decorator for public routes"""
    function.is_public = True
    return function

ultimos_envios = {}

def validar_telefone(numero):
    return re.match(r'^\d{10,11}$', numero)

@public_endpoint
@kryptacode_bp.route("/orcamento", methods=["POST"])
def orcamento():
    ip = request.remote_addr
    agora = time.time()

    # ⛔ anti-spam simples
    if ip in ultimos_envios and agora - ultimos_envios[ip] < 10:
        return "Aguarde alguns segundos 😅", 429

    ultimos_envios[ip] = agora

    # 🪤 honeypot
    if request.form.get("website"):
        return "Bot detectado", 400

    nome = request.form.get("nome", "").strip()
    whatsapp = request.form.get("whatsapp", "").strip()
    mensagem = request.form.get("mensagem", "").strip()
    email = request.form.get("email", "").strip()
    empresa = request.form.get("empresa", "").strip()

    data = {
        "username": nome,
        "email": email,
        "empresa": empresa,
        "numero": whatsapp,
        "observacao": mensagem
    }

    resultado = ConsultaDados.cadastrar_contato(data)

    if resultado["status"] == "erro":

        if resultado["tipo"] == "duplicado":
            return redirect("/?erro=email_existe")

        return redirect("/?erro=generico")

    return redirect("/?sucesso=1")



@public_endpoint
@kryptacode_bp.route("/", methods=["GET"])
def serve():
    return render_template("index.html")

@kryptacode_bp.route("/termos_resposabilidade", methods=["GET"])
def termos_resposabilidade():
    return render_template("termos_resposabilidade.html")

@kryptacode_bp.route("/politica_privacidade", methods=["GET"])
def politica_privacidade():
    return render_template("politica_privacidade.html")





