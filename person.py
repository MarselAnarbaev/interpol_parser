from webparse import WebParse
import time
import json
import requests
import os


class Person:
    def __init__(self, _image_link=None, _page_link=None):
        self.page = WebParse()

        self.personal_info = {}

    def get_main_table_data(self, _soup, _class):
        # get Identity particulars table data
        table_div = _soup.find('div', attrs={"class": _class})
        table = table_div.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if self.make_pretty(cols[0].get_text()) == 'Gender':
                for item in cols[1].find_all('span'):
                    if len(item['class']) == 1:
                        self.personal_info['Gender'] = self.make_pretty(item.get_text())
            else:
                self.personal_info[self.make_pretty(cols[0].get_text())] = \
                    self.make_pretty(cols[1].get_text()).encode('cp1252').decode('cp1252')

    def get_extra_table_data(self, _soup, _class):
        # get extra tables data
        table_div = _soup.find('div', attrs={"class": _class})
        table = table_div.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            self.personal_info[self.make_pretty(cols[0].get_text())] = \
                self.make_pretty(cols[1].get_text()).encode('cp1252').decode('cp1252')

    @staticmethod
    def make_pretty(_string):
        return _string.replace('\n', '').strip()

    @staticmethod
    def save_json(_key1, _key2, _data):
        #save as json
        _filename = '{0} {1}.json'.format(_key1.encode('cp1252').decode('cp1252'), _key2.encode('cp1252').decode('cp1252'))
        try:
            with open(_filename, 'w') as js_data:
                json.dump(_data, js_data)
        except NameError:
            print('error filename:', _filename)

    def get_persons_data(self, _page_link, _name=None, _forename=None):
        self.page.input_data(_page_link, _name, _forename)
        img_dir = self.manage_directory()
        self.clear_directory(img_dir)
        for link in self.page.get_persons():
            self.process_link(link, img_dir)

        self.page.close_driver()

    def process_link(self, link, img_dir):
        self.personal_info.clear()
        time.sleep(1)
        print(link)
        # hard check, sometime interpol doesn't want to load page and gets back to main page
        # so we make it into while loop, unless it loads page and inserts specified key from links list
        while 'Family name' not in self.personal_info.keys():
            soup = self.page.get_page_soup_code(link)
            self.get_main_table_data(soup, "wantedsingle__infosWrapper")
            self.get_extra_table_data(soup, "wantedsingle__infosWrapper physicalDescriptionContent")
            self.get_extra_table_data(soup, "wantedsingle__infosWrapper detailsContent")
            self.page.get_page_images()
        print(self.page.get_image_links())
        try:
            del self.personal_info[""]
        except KeyError:
            pass
        self.save_json(self.personal_info['Family name'], self.personal_info['Forename'], self.personal_info)
        self.get_person_images(self.personal_info['Family name'], self.personal_info['Forename'], img_dir)

    def get_person_images(self, _key1, _key2, _dir):
        # get images from page
        image_links = self.page.get_image_links()
        image_counter = 1
        for item in image_links:
            image_name = '{0} {1} {2}.jpg'.format(_key1.encode('cp1252').decode('cp1252'), _key2.encode('cp1252').decode('cp1252'), image_counter)
            image_counter += 1
            with open(os.path.join(_dir, image_name), 'wb') as person_image:
                response = requests.get(item, stream=True)
                person_image.write(response.content)

    @staticmethod
    def manage_directory():
        # make new directory
        cwd = os.getcwd()
        img_dir = "person_images"
        dir_path = os.path.join(cwd, img_dir)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        return dir_path

    @staticmethod
    def clear_directory(_dir):
        # remove all previous search data from directories
        cwd = os.getcwd()
        for file in os.listdir(cwd):
            if file.endswith(".json"):
                os.remove(file)

        for file in os.listdir(_dir):
            os.remove(os.path.join(_dir, file))
