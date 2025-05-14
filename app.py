from flask import Flask, request, send_file, abort
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import os, tempfile, uuid

app = Flask(__name__)
env = Environment(loader=FileSystemLoader('plantillas'))

@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    data = request.get_json()
    if not data:
        return abort(400, 'JSON payload required')

    tipo = data.get('tipo_documento', 'albaran')
    template_name = f'{tipo}.html'
    try:
        template = env.get_template(template_name)
    except Exception:
        return abort(400, f'Template {template_name} not found')

    html_rendered = template.render(**data)

    tmp_dir = tempfile.gettempdir()
    filename = f"{tipo}_{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join(tmp_dir, filename)

    HTML(string=html_rendered, base_url='.').write_pdf(pdf_path)

    return send_file(pdf_path, as_attachment=True, download_name=f"{tipo}.pdf")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
