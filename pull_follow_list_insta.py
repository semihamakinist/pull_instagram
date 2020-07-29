# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import urllib.request as request
from datetime import datetime
import logging
import random
import string
import time
import os

now_date = datetime.now()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=os.path.join(os.getcwd(),
                                          '{}-{}-{}-pull_info_instegram.txt'.format(now_date.year,
                                                                                    now_date.month,
                                                                                    now_date.day)),
                    filemode='w'
                    )


class InstagramBot:
    def __init__(self, user_name=""):
        chrome_drive_name = "chromedriver_win32-83.0.4103.39"

        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.chrome_options.add_argument("--mute-audio")
        self.chrome_driver = os.path.join(os.getcwd(), "drive", chrome_drive_name, "chromedriver.exe")
        # closed drive
        # self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.chrome_driver)

        # open drive
        self.driver =webdriver.Chrome(self.chrome_driver)

        self.main_insta_url = "https://www.instagram.com/"
        self.save_image_path = os.path.join(os.getcwd(), "instagrambot")
        self.user_name = user_name
        self.user_id = ""
        self.comment = ""
        self.image_url = ""

    @staticmethod
    def delay(time_number):
        return time.sleep(time_number)

    @staticmethod
    def generator_id(word_length=32):
        x = '{}{}'.format(string.digits, string.ascii_letters)
        return ''.join(random.choice(x) for _ in range(word_length))

    def giris_yap(self, user_name_str, password_str):
        self.driver.get(self.main_insta_url)
        time.sleep(2)

        try:
            # fill login info for instagram
            user_name_input_text = self.driver.find_element_by_name("username")
            password_input_text = self.driver.find_element_by_name("password")
            user_name_input_text.send_keys(user_name_str)
            self.delay(2)
            password_input_text.send_keys(password_str)
            self.delay(2)

            try:
                giris_butonu = self.driver.find_element_by_xpath(
                    "//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[4]/button")
            except Exception as e:
                giris_butonu = self.driver.find_element_by_xpath(
                    "/html/body/div[5]/div[2]/div/div[2]/div/div/div[1]/div/form/div[4]/button")

            giris_butonu.click()
            time.sleep(2)
            self.user_name = user_name
            self.driver.get("{}{}".format(self.main_insta_url, self.user_name))

        except Exception as e:
            logging.error("giris_butonu_error: {}".format(e))

    def get_request_url(self, user_name):
        return "{}{}".format(self.main_insta_url, user_name)

    def scroll_down_page(self, dialog, allfoll):
        for i in range(int(allfoll / 10)):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
            self.delay(random.randint(500, 1000) / 1000)
            print("Extracting scroll_down_page %", round((i / (allfoll / 2) * 100), 2), "from", "%100")
        print("Extracting scroll_down_page complate %100")

    def get_image_list(self, get_url, user_following_count):
        self.driver.get(get_url)
        self.delay(random.randint(500, 1000) / 1000)
        try:
            self.driver.find_element_by_css_selector('.eLAPa').click()  # İlk fotoğrafa tıklayan kod
            # find the followers window
            # people tab panel
            dialog = self.driver.find_element_by_xpath('/html')
            # find number of followers
            allfoll = int(user_following_count)
            print(f"allfoll: {allfoll} - for_loop_range: {int(allfoll / 4)}")
            self.scroll_down_page(dialog, allfoll)

            image_list = []
            while True:
                try:
                    self.delay(random.randint(500, 1000) / 1000)

                    # download image url
                    image_xpath = None
                    save_folder_path = os.path.join(self.save_image_path, "images", self.user_name)
                    self.create_folder(save_folder_path)

                    save_image_file_path = os.path.join(save_folder_path, "{}.png".format(self.generator_id()))

                    try:
                        # _97aPb
                        image_xpath = self.driver.find_element_by_css_selector('._97aPb '). \
                            find_element_by_css_selector(".ZyFrc"). \
                            find_element_by_css_selector(".KL4Bh"). \
                            find_element_by_tag_name("img")
                    except Exception as e:

                        image_xpath = self.driver.find_element_by_css_selector('._97aPb '). \
                            find_element_by_css_selector(".kPFhm.B1JlO.OAXCp"). \
                            find_element_by_css_selector("._5wCQW").\
                            find_element_by_tag_name("img")

                    if image_xpath:
                        # save image
                        image_url = image_xpath.get_attribute('src')
                        logging.info("get image url: {}".format(image_url))
                        print(f"image_xpath: {image_url}")
                        image_list.append(image_url)

                        logging.info("save_image_file_path: {}".format(save_image_file_path))
                        print("save_image_file_path: {}".format(save_image_file_path))
                        request.urlretrieve(image_url, save_image_file_path)

                    # get image commend
                    commend_xpath = None
                    try:
                        # EtaWk
                        commend_xpath = self.driver.find_element_by_css_selector('.EtaWk ').\
                            find_element_by_css_selector(".C4VMK").text
                        commend_xpath = commend_xpath.replace('\n', ' -$#$- ')

                    except Exception as e:
                        logging.error(f"commend_xpath error: {e}")
                        commend_xpath = ""

                    if commend_xpath:
                        print(f"commend_xpath: {commend_xpath}")

                    self.driver.find_element_by_css_selector("._65Bje.coreSpriteRightPaginationArrow").click()
                    time.sleep(random.randint(1, 3))
                    break
                except Exception as e:
                    logging.error("eLAPa_error: {}".format(e))
                    print("eLAPa_error: {}".format(e))
                    break
        except Exception as e:
            logging.error("65Bje_error: {}".format(e))
            print("65Bje_error: {}".format(e))

        logging.info(f"image_list leng: {len(image_list)} - {image_list}")
        print(f"image_list leng: {len(image_list)} - {image_list}")
        return image_list

    def get_fllowing_list(self, get_url, user_following_count):
        self.driver.get(get_url)
        self.delay(random.randint(500, 1000) / 1000)
        flolwing_a_tag = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
        print(f"flolwing_a_tag: {flolwing_a_tag}")
        flolwing_a_tag.click()
        self.delay(random.randint(1, 3))

        # find the followers window
        # kisiler tab panel
        dialog = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        # find number of followers
        allfoll = int(user_following_count)
        print(f"allfoll: {allfoll} - for_loop_range: {int(allfoll / 4)}")
        self.scroll_down_page(dialog, allfoll)

        following_class = self.driver.find_elements_by_css_selector('.Jv7Aj.MqpiF')
        following_list = []
        for fl in following_class:
            following_list.append(fl.text)

        return following_list

    def image_follewer_follewing_count(self, get_url):
        self.driver.get(get_url)

        time.sleep(2)

        user_image_count = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]')
        user_image_count = user_image_count.text.replace(' gönderi', '').replace('.', '').replace(' ', '')

        user_follower_count = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]')
        user_follower_count = user_follower_count.text.replace(' takipçi', '').replace('.', '').replace(' ', '')

        user_following_count = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]')
        user_following_count = user_following_count.text.replace(' takip', '').replace('.', '').replace(' ', '')

        logging.info(f"user_name: {self.user_name} - "
                     f"image_count: {user_image_count} - "
                     f"follower_count: {user_follower_count} - "
                     f"following_count: {user_following_count}")

        print(f"image_count: {user_image_count} - "
              f"follower_count: {user_follower_count} - "
              f"following_count: {user_following_count}")
        return int(user_image_count), int(user_follower_count), int(user_following_count)


if __name__ == '__main__':
    # instagram info
    user_name = "insta_user_name"
    password = "insta_password"

    insta_boot = InstagramBot()
    # login instagram
    insta_boot.giris_yap(user_name, password)

    get_url = insta_boot.get_request_url(user_name)
    logging.info("{} adlı kullanıcının takipçi listesi çekiliyor".format(user_name))
    logging.info("Request insta user url: {}".format(get_url))
    user_image_count, user_follower_count, user_following_count = insta_boot.image_follewer_follewing_count(get_url)

    logging.info(f"get_image_list")
    image_list = insta_boot.get_image_list(get_url, user_following_count)
    logging.info(f"image_list: {image_list}")
    print(f"image_list: {image_list}")

    # logging.info(f"get_following_list")
    # following_list = insta_boot.get_fllowing_list(get_url, user_following_count)
    # logging.info(f"get_following_list: {following_list}")
    # print(f"get_following_list: {following_list}")

    # insta_boot.driver.close()
