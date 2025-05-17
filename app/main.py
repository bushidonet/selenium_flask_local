from flask import Flask, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flasgger import Swagger
import tempfile

app = Flask(__name__)
swagger = Swagger(app)

def create_browser():
    options = Options()
    options.add_argument("--headless")  # Ejecutar sin interfaz
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1200,800")  # Tamaño fijo de ventana

    browser = webdriver.Chrome(options=options)
    return browser

@app.route('/test', methods=['GET'])
def test_selenium():
    """
    Toma una captura de pantalla de example.com usando Selenium
    ---
    tags:
      - Selenium
    responses:
      200:
        description: Captura tomada exitosamente
        content:
          image/png:
            schema:
              type: string
              format: binary
      500:
        description: Error durante la ejecución
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    browser = create_browser()
    try:
        url = 'https://example.com'
        browser.get(url)

        # Tomar screenshot
        tmp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        browser.save_screenshot(tmp_file.name)
        tmp_file.close()

        return send_file(tmp_file.name, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        browser.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
