from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException


class WebParse:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.page_links = []
        self.image_links = []

    def close_driver(self):
        self.driver.close()

    def load_link(self, _link):
        self.driver.get(_link)

    def clear_persons(self):
        self.page_links.clear()

    def get_persons(self):
        return self.page_links

    def get_image_links(self):
        return self.image_links

    def scroll_down(self):
        # scroll down to load all elements
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def get_page_soup_code(self, _link):
        # open link and convert to bs4 soup
        self.load_link(_link)
        self.refresh_page()
        time.sleep(1)
        return self.html_to_soup_code(self.driver.page_source)

    def refresh_page(self):
        self.driver.refresh()
        time.sleep(1)

    @staticmethod
    def html_to_soup_code(html_code):
        # html code to bs4 soup
        soup_code = BeautifulSoup(html_code, "html.parser")
        return soup_code

    def input_data(self, _link, _name="", _forename=""):
        # parse input data from user
        self.clear_persons()
        self.load_link(_link)


        # wait for form to be clickable
        WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.ID, "name")))
        self.driver.find_element(By.ID, "name").send_keys(_name)
        self.driver.find_element(By.ID, "forename").send_keys(_forename)

        # wait for button to be clickable
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.ID, "submit")))
        try:
            self.driver.find_element(By.ID, "submit").click()
        except WebDriverException:
            pass
        time.sleep(1)
        self.move_through_pages()

    def move_through_pages(self):
        # Move through each page of search results if exists
        try:
            # Move through multiple pages and collect links
            wait = WebDriverWait(self.driver, 1)
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "nextElement")))
            self.get_page_links()
            while self.driver.find_element(By.CLASS_NAME, "nextElement").is_displayed():
                try:
                    self.scroll_down()
                    self.driver.find_element(By.CLASS_NAME, "nextElement").click()
                    time.sleep(1)
                    self.get_page_links()
                except WebDriverException:
                    self.scroll_down()
                    self.get_page_links()

        except WebDriverException:
            # Collect links only from first page
            self.get_page_links()

    def get_page_links(self):
        # collect links on page
        try:
            for item in self.driver.find_elements(By.XPATH, "//a[@class='redNoticeItem__labelLink']"):
                self.page_links.append(item.get_attribute('href'))
        except WebDriverException:
            pass

    def get_page_images(self):
        # collect image links
        self.image_links.clear()

        try:
            if self.driver.find_element(By.XPATH,
                                            "//div[@class='redNoticeLargePhoto__wrapperImg']/img[@class='redNoticeLargePhoto__img']").is_displayed():
                main_image = self.driver.find_element(By.XPATH, "//div[@class='redNoticeLargePhoto__wrapperImg']/img[@class='redNoticeLargePhoto__img']")
                self.image_links.append(main_image.get_attribute('src'))
                other_images = self.driver.find_element(By.CLASS_NAME,
                                                            "wantedsingle__wrapperOtherPhotos")
                for item in other_images.find_elements(By.CLASS_NAME, "wantedsingle__otherPhotosImage"):
                    self.image_links.append(item.get_attribute('src'))

        except WebDriverException:
            print('image can not be loaded')






