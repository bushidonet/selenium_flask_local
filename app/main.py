from flask import Flask, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flasgger import Swagger
import tempfile
from time import sleep

app = Flask(__name__)
swagger = Swagger(app)

def create_browser():
    options = Options()
    # options.add_argument("--headless")  # Ejecutar sin interfaz
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
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
        url = 'https://pdfcv.com/'
        browser.get(url)
        sleep(3)  # Esperar a que la página cargue completamente
        
        boton = browser.find_element(By.CSS_SELECTOR, ".bg-blue-500.text-white.font-bold")
        boton.click()
        sleep(2)
        
        # Rellenar el campo por ID
        input_user = browser.find_element(By.ID, "user_name")
        input_user.send_keys("Juan Pérez")
        sleep(2)
        
        # Llenar los campos por ID (asegúrate de que los IDs existen)
        browser.find_element(By.ID, "user_name").send_keys("Jane")
        browser.find_element(By.ID, "user_last_name").send_keys("Doe")
        browser.find_element(By.ID, "user_contact_email").send_keys("me@example.com")
        browser.find_element(By.ID, "user_phone").send_keys("+1 100 1000 1000")
        browser.find_element(By.ID, "user_link").send_keys("https://www.example.com")
        browser.find_element(By.ID, "user_short_title").send_keys("Web Developer")
        browser.find_element(By.ID, "user_personal_statement").send_keys("Enthusiastic developer with experience in web technologies.")
        browser.find_element(By.ID, "user_address").send_keys("123 Main Street, City, Country")
        sleep(3)
        
        # Llenar datos de experiencia laboral
        browser.find_element(By.ID, "user_experiences_attributes_0_from_date").clear()
        browser.find_element(By.ID, "user_experiences_attributes_0_from_date").send_keys("Jan 2015")

        browser.find_element(By.ID, "user_experiences_attributes_0_to_date").clear()
        browser.find_element(By.ID, "user_experiences_attributes_0_to_date").send_keys("Dec 2020")

        browser.find_element(By.ID, "user_experiences_attributes_0_position").clear()
        browser.find_element(By.ID, "user_experiences_attributes_0_position").send_keys("Software Engineer")

        browser.find_element(By.ID, "user_experiences_attributes_0_emp_name").clear()
        browser.find_element(By.ID, "user_experiences_attributes_0_emp_name").send_keys("TechCorp Inc.")

        browser.find_element(By.XPATH, "//textarea").send_keys("Led development of major software releases with agile methodology.")

        # Hacer clic en el botón "Add position"
        browser.find_element(By.ID, "user_experiences_attributes_0_responsibilities").click()
        sleep(2)
        
        # Click en el botón por texto visible
        browser.find_element(By.XPATH, '//*[@id="experiences"]/fieldset/a').click()
        sleep(2)
        
        browser.find_element(By.XPATH, '//*[@id="user_educations_attributes_0_from_date"]').send_keys("Jan 2010")
        browser.find_element(By.XPATH, '//*[@id="user_educations_attributes_0_to_date"]').send_keys("Dec 2014")
        browser.find_element(By.XPATH, '//*[@id="user_educations_attributes_0_qualification"]').send_keys("BSc in Software Engineering")
        browser.find_element(By.XPATH, '//*[@id="user_educations_attributes_0_org_name"]').send_keys("MIT")
        browser.find_element(By.XPATH, '//*[@id="user_educations_attributes_0_org_name"]').send_keys("AI, ML, Web Dev")


        # Clic en 'Add school'
        browser.find_element(By.XPATH, '//*[@id="educations"]/fieldset/a').click()
        sleep(2)
        
        # Selecciona el checkbox por ID
        checkbox = browser.find_element(By.ID, 'user_accept_terms')  # Reemplaza con el ID real
        sleep(2)
        
        # Marca el checkbox si no está marcado
        if not checkbox.is_selected():
            checkbox.click()
        sleep(4)
        
        boton1 = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div[2]/input')
        # 2. Hacer scroll hasta el elemento
      
        browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton1)
        sleep(3)
        
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[2]/form/div[2]/input")))
        boton1.click()
        sleep(3)
        
        boton2 = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[4]/div[2]/div/form/input')
        browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton2)
        # 2. Hacer scroll hasta el elemento
        sleep(3)
        boton2.click()
        
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
