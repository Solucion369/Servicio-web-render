from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from flask_cors import CORS

from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome()
def crear_app():
        
    app = Flask(__name__)

    CORS(app)
    # Ruta para manejar la solicitud y devolver datos como JSON
    @app.route('/followers', methods=['POST'])
    def get_followers():
        
        # url = request.args.get("url")
        driver = webdriver.Chrome()

        seguidores = []
        datos_json = request.get_json()

        if 'enlaces' in datos_json and isinstance(datos_json['enlaces'], list):
            # Iterar sobre los enlaces y llamar a la función para extraer seguidores
            for url in datos_json['enlaces']:
                if "facebook.com" in url:
                    followers = obtenerSeguidoresFacebook(url, driver)
                    seguidores.append(followers)

                elif "instagram.com" in url:
                    followers = obtenerSeguidoresInstagram(url, driver)
                    seguidores.append(followers)
                else:
                    seguidores.append("")
            
            return jsonify({'followers': seguidores})
        else:
            return 'Los datos JSON deben contener un arreglo de enlaces.'
        
        # driver.quit()
        
        # return jsonify({'followers': numero_seguidores})

    url_pagina_facebook = 'https://www.facebook.com/CanalBoyaca'
    url_user_instagram = "https://www.instagram.com/huertaagroecologicamuyso/"

    # Cerrar el navegador
    # driver.quit()

    def obtenerSeguidoresFacebook(url, driver):

        driver.get(url)

        driver.implicitly_wait(10)

        seguidores_element = driver.find_element(By.XPATH, "//a[contains(@href, 'followers')]")
        numero_seguidores = seguidores_element.text

        # Imprimir el número de seguidores
        print("Número de seguidores:", numero_seguidores)

        return numero_seguidores


    def obtenerSeguidoresInstagram(url, driver):
        # driver = webdriver.Chrome()
        driver.get(url)

        # Esperar a que la página se cargue completamente (puedes ajustar el tiempo de espera según sea necesario)
        driver.implicitly_wait(10)

        # Encontrar el elemento que contiene el número de seguidores (puedes ajustar el selector según sea necesario)
        boton_seguidores = driver.find_element(By.XPATH, '//button[contains(.,"seguidores")]')
        
        numero_seguidores = boton_seguidores.find_element(By.XPATH, ".//span").text

        # Imprimir el número de seguidores
        print("Número de seguidores:", numero_seguidores)

        return numero_seguidores
        # driver.quit()
        # Cerrar el navegador

    return app

if __name__ == '__main__':
    app = crear_app()
    app.run()
