from flask import Flask, request, send_file, render_template_string
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

# Inicializa la app Flask
app = Flask(__name__)

# Configura el entorno de plantillas Jinja2
template_loader = FileSystemLoader(searchpath="plantillas")
template_env = Environment(loader=template_loader)

@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    # Imprime headers y cuerpo crudo para trazabilidad
    print("[HEADERS]:", dict(request.headers), flush=True)
    print("[CUERPO RAW]:", request.get_data(as_text=True), flush=True)

    try:
        # Parseo forzado del cuerpo como JSON
        data = request.get_json(force=True)
    except Exception as e:
        return {"error": f"Error al parsear JSON: {str(e)}"}, 400

    try:
        # Carga y renderiza la plantilla con los datos del JSON
        template = template_env.get_template("albaran.html")
        rendered_html = template.render(data)

        # Genera el PDF con WeasyPrint
        pdf_path = "albaran.pdf"
        HTML(string=rendered_html).write_pdf(pdf_path)

        # Retorna el PDF como archivo adjunto
        return send_file(pdf_path, as_attachment=True, download_name="albaran.pdf")

    except Exception as e:
        return {"error": f"Error generando el PDF: {str(e)}"}, 500

# Ejecuta la app en modo producción (sin debug)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
