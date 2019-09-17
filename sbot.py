from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from sys import argv


class Driver:

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def login(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.login_button = self.driver.find_element_by_link_text(
            'Fazer Login'
            ).click()
        sleep(1)
        self.driver.find_element_by_id('login-email').send_keys(argv[1])
        self.driver.find_element_by_id('login-password').send_keys(argv[2])
        self.driver.find_element_by_xpath(
            '//button[text() = "Acessar"]'
            ).click()
        sleep(3)

    def go_to_tech_page(self):
        self.action = ActionChains(self.driver)
        self.parent_element = self.driver.find_element_by_link_text(
            '#VAILÁEFAZ!'
            )
        self.action.move_to_element(self.parent_element).perform()
        sleep(1)
        self.tech_page = self.driver.find_element_by_link_text(
            'Tecnologia'
            ).click()
        sleep(3)

    def new_topic_title(self, title):
        # Clica em novo topico
        self.driver.find_element_by_id('btnNovoTopico').click()

        # Preenche o título do tópico
        self.driver.find_element_by_id('titulo-topico').send_keys(title)

    def add_text(self, body):
        # Preenche o corpo do texto
        self.driver.find_element_by_id('novoTopicoEditable').send_keys(body)

    def add_image(self, image):
        pass

    def new_python_code(self, text_code):
        # Clica na feature de código
        self.driver.find_element_by_id('mceu_44-button').click()
        sleep(1)

        # Seleciona a linguagem Python
        self.driver.find_element_by_id('mceu_59-open').click()
        self.driver.find_element_by_id('mceu_71-text').click()
        sleep(1)

        # Preenche o corpo do código
        self.driver.find_element_by_tag_name('textarea').send_keys(text_code)
        sleep(1)

        # Clica em Ok
        self.driver.find_element_by_id('mceu_62-button').click()

    def send_topic(self):
        self.driver.find_elements_by_id('btnEnviarNovoTopico').click()


if __name__ == '__main__':

    chrome = Driver(webdriver.Chrome(), 'https://www.bastter.com')
    chrome.login()
    chrome.go_to_tech_page()
    chrome.new_topic_title('Teste')
    chrome.add_text('Este tópico foi feito por um bot.\n')
    chrome.new_python_code('print("Hello Bot!")')
    chrome.add_text('Mais texto adicionado após o código')
    #chrome.send_topic()
