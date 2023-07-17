from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time

from selenium.webdriver.common.by import By


@override_settings(ALLOWED_HOSTS=['*'])
class BasicTests(StaticLiveServerTestCase):
    host = '127.0.0.1'
    fixtures = ['test_data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def login(self, user_name, password):
        self.driver.delete_all_cookies()
        self.driver.get(f'{self.live_server_url}/catalog/login/')

        time.sleep(0.5)
        login_field = self.driver.find_element(By.CSS_SELECTOR, "#id_login")
        login_field.click()
        login_field.send_keys(user_name)
        time.sleep(0.5)
        password_field = self.driver.find_element(By.CSS_SELECTOR, "#id_password")
        password_field.click()
        password_field.send_keys(password)
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, "#btn-login").click()
        time.sleep(0.5)

    def test_hello_world(self):
        self.driver.get(f'{self.live_server_url}/catalog/login/')
        assert 'BookApp - Log in' == self.driver.title

    def test_login(self):
        self.login("admin", "12345")

        user_name = self.driver.find_element(By.CSS_SELECTOR, "#user-name").text
        print(user_name)
        assert 'Administrator' == user_name

    def test_edit_profile(self):
        self.login("user", "12345")

        user_name = self.driver.find_element(By.CSS_SELECTOR, "#user-name").text
        print(user_name)
        assert 'Regular user' == user_name

        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, "#menu-lower-right").click()
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, "#user-account").click()
        time.sleep(0.5)
        name_field = self.driver.find_element(By.CSS_SELECTOR, "#id_name")
        name_field.clear()
        name_field.click()
        name_field.send_keys("Test user")
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, "#btn-save").click()
        time.sleep(0.5)

        user_name = self.driver.find_element(By.CSS_SELECTOR, "#user-name").text
        assert 'Test user' == user_name