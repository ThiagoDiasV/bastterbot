from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
# from selenium.common.exceptions import NoSuchElementException
from time import sleep
from sys import argv
from os import path
from glob import glob
import re


class Driver:

    def __init__(self, driver, url):
        # Inicializa uma instância de Driver
        self.driver = driver
        self.url = url
        self.action = ActionChains(self.driver)

    def waits(self, method, element_type, element):
        return WebDriverWait(self.driver, 15).until(
            method((element_type, element))
        )

    def login(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.waits(ec.presence_of_element_located, By.LINK_TEXT, 'Fazer Login')
        self.login_button = self.driver.find_element_by_link_text(
            'Fazer Login'
            ).click()
        self.waits(ec.element_to_be_clickable, By.ID, 'login-email')
        self.driver.find_element_by_id('login-email').send_keys(argv[1])
        sleep(1)
        self.driver.find_element_by_id('login-password').send_keys(argv[2])
        self.driver.find_element_by_xpath(
            '//button[text() = "Acessar"]'
            ).click()

    def go_to_tech_page(self):
        sleep(3)
        self.driver.find_element_by_xpath(
            '//li[contains(@class, "dropdown")]/a[contains(@href, "vai-la-e-faz")]'
            ).click()
        self.driver.find_element_by_xpath(
            '//div[contains(@class, "menuExterior")]/a[contains(@href, "tecnologia")]'
        ).click()

    def new_topic_title(self, title):
        # Clica em novo topico
        self.waits(ec.presence_of_element_located, By.ID, 'btnNovoTopico')
        self.driver.find_element_by_id('btnNovoTopico').click()

        # Preenche o título do tópico
        self.driver.find_element_by_id('titulo-topico').send_keys(title)

    def add_text(self, body):
        # Preenche o corpo do texto
        textarea = self.driver.find_element_by_id(
            'novoTopicoEditable'
            )
        if textarea.text == 'Digite sua mensagem':
            textarea.send_keys(body)
        else:
            textarea.send_keys(Keys.ARROW_RIGHT, Keys.ENTER, body)

    def add_image(self):
        self.waits(ec.element_to_be_clickable, By.ID, 'mceu_50-button')
        self.driver.find_element_by_id('mceu_50-button').click()
        self.driver.find_element_by_id('tiny-image-upload').click()

    def new_python_code(self, text_code):
        # Clica na feature de código
        self.driver.find_element_by_id('mceu_44-button').click()

        # Seleciona a linguagem Python
        self.waits(
            ec.element_to_be_clickable,
            By.XPATH,
            '//button[contains(@id, "mceu_")]/span[text()="HTML/XML"]'
            )
        self.driver.find_element_by_xpath(
            '//button[contains(@id, "mceu_")]/span[text()="HTML/XML"]'
            ).click()

        self.driver.find_element_by_xpath(
            '//div[contains(@id, "mceu_")]/span[text()="Python"]'
            ).click()

        # Preenche o corpo do código
        self.waits(ec.visibility_of_element_located, By.TAG_NAME, 'textarea')
        self.driver.find_element_by_tag_name('textarea').send_keys(text_code)

        # Clica em Ok
        self.driver.find_element_by_xpath(
            '//button[contains(@id, "mceu_")]/span[text()="Ok"]'
            ).click()

    def send_topic(self):
        self.driver.find_elements_by_id('btnEnviarNovoTopico').click()


if __name__ == '__main__':

    chrome = Driver(webdriver.Chrome(), 'https://www.bastter.com')
    chrome.login()
    chrome.go_to_tech_page()
    title = 'Extra[17] - Python - Criei um bot para postar na Bastter.com pra mim'
    chrome.new_topic_title(title)
    text_files = glob('texts/*.txt')
    text_files.sort(key=path.getmtime)
    for text_file in text_files:
        if re.match(r'\w+/body', text_file):
            with open(text_file, 'r') as body:
                text = body.read()
                chrome.add_text(text)
        else:
            with open(text_file, 'r') as code:
                code = code.read()
                chrome.new_python_code(code)
    # chrome.add_image()

    # chrome.send_topic()
