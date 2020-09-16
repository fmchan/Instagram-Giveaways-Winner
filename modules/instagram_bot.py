from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from typing import List, Iterator
from itertools import chain
from time import perf_counter
import re
import sys
import os
from pathlib import Path
import json
import random
import time

class Comments:
    
    def __init__(self, iter_connections:Iterator[str], parts_expr:List[str]):
        self.iter_connections = iter_connections
        self.parts_expr = parts_expr

    def generate(self) -> Iterator[str]:

        last_part = self.parts_expr[-1]

        while True:

            if len(self.parts_expr) == 1:
                yield last_part

            else:
            
                try:
                
                    users = next(self.iter_connections)
                except StopIteration:
                    return

                comment = ''.join(chain.from_iterable(zip(self.parts_expr, users)))

                yield (comment + last_part).replace(r'\@', '@')


class Bot:

    __version__ = '1.0.3'

    
    def __init__(self, window:bool=True, timeout=30):

        '''

        Web Driver's path
        Credits: https://github.com/nateshmbhat/webbot/blob/master/webbot/webbot.py

        '''
        
        if sys.platform == 'linux' or sys.platform == 'linux2':
            driver_file_name = 'chrome_linux'
        elif sys.platform == 'win32':
            driver_file_name = 'chrome_windows.exe'
        elif sys.platform == 'darwin':
            driver_file_name = 'chrome_mac'
            
        driver_path = os.path.join(os.getcwd() , f'drivers{os.path.sep}{driver_file_name}')
        
        os.chmod(driver_path , 0o755) 

        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.headless = not window ; 

        
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)


        self.url_base = 'https://www.instagram.com/'
        self.url_login = self.url_base + 'accounts/login'
        self.timeout = timeout

    def log_in(self, username:str, password:str):
        self.driver.get(self.url_login)
        
        WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_elements_by_css_selector('form input'))
        
        username_input, password_input, *_ = self.driver.find_elements_by_css_selector('form input')

        username_input.send_keys(username)
        password_input.send_keys(password + Keys.ENTER)

        WebDriverWait(self.driver, self.timeout).until(
            lambda x: 'js logged-in' in x.find_element_by_tag_name('html').get_attribute('class'))


    def new_tab(self, url:str='https://www.google.com'):
        
        self.driver.execute_script(f'window.open(\'{url}\');')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        

    def close_tab(self):
        
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1]) # could write 'main' but later on could be modified
        
    
    def get_user_json(self, username:str) -> List[str]:
        with open(f'records//db//{username}.json', 'r') as file:
            return json.load(file)

    def get_and_reformat_json(self, code:str, connections:List[str]) -> List[str]:
        with open(f'records//tags//{code}.json', 'r') as file:
            data = json.load(file)
            common_elements = set(data).intersection(connections)
            user_following_not_comment = list(set(connections).difference(common_elements))
            random.shuffle(user_following_not_comment)
            return list(common_elements) + user_following_not_comment

    def get_user_connections(self, username:str, limit:int=None, followers=True) -> List[str]:

        '''

        Connections means followers or followings depending on the chosen data

        Args:
            - username : target's username
            - limit : limit number of connections to save
            - followers: if True returns a list of user's followers, if False returns of user's followings

        Returns:
            - list of usernames
        '''
        
        if limit == 0:
            return []

        path = 'records//' + ('followers' if followers else 'followings')

        if limit:

            try:
                
                with open(f'{path}//{username}_{limit}.json', 'r') as file:
                    return json.load(file)
                
            except FileNotFoundError:
                pass
        
        self.new_tab(self.url_base + username)

        WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_element_by_css_selector('header h1'))
        
        if followers:
            connections_link = self.driver.find_element_by_css_selector('ul li a span')
            connections_limit = int(connections_link.get_attribute('title').replace(',', ''))
        else:
            connections_link = self.driver.find_element_by_css_selector('ul li:nth-child(3) a span')

            try:
                connections_limit = int(connections_link.text.replace(',', ''))
                
            except ValueError:
                exit('''
                        You must choose a UserTarget which following < 10,000 users
                        This happens because instagram doesn't provide by source the whole number,
                        and it would be a pain to translate every possible letter
                    ''')

        limit = min(connections_limit, limit) if limit else connections_limit

        if limit == connections_limit:
            try:
                
                with open(f'{path}//{username}_{limit}.json', 'r') as file:
                    self.close_tab()
                    return json.load(file)
                
            except FileNotFoundError:
                pass
                
        connections_link.click()

        WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_element_by_css_selector('div[role=\'dialog\'] ul'))
        
        connections_list = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
        connections_count = len(connections_list.find_elements_by_css_selector('li'))
        
        connections_list.click()
        
        action_chain = webdriver.ActionChains(self.driver)

        last_count = connections_count
        arrow_down = False

        timestamp = perf_counter()

        try:
            if limit != connections_limit:
                raise FileNotFoundError # Already searched and not found

            file = open(f'{path}//{username}_{limit}.json', 'r')
        
        except FileNotFoundError:
            
            while connections_count < limit and perf_counter() - timestamp < self.timeout:

                if last_count == connections_count:
                    action_chain.key_up(Keys.PAGE_DOWN).perform()
                    connections_list.click()
                    arrow_down = False
                    timestamp = perf_counter()
                
                if not arrow_down:
                    action_chain.key_down(Keys.PAGE_DOWN).perform()
                    arrow_down = True
                
                last_count = connections_count

                connections_count = len(connections_list.find_elements_by_css_selector('li'))

            connections = []
        
            for connection_obj in connections_list.find_elements_by_css_selector('li'):
                connection = connection_obj.find_element_by_css_selector('a')

                connection_name = connection.text

                if not connection_name:
                    connection_name = connection.get_attribute('href').split('/')[-2]

                connections.append('@' + connection_name)
                if (len(connections) == limit):
                    break

            Path(path).mkdir(parents=True, exist_ok=True)


            with open(f'{path}//{username}_{len(connections)}.json', 'w') as file:
                json.dump(connections, file)

        else:
            connections = json.load(file)
            file.close()

        self.close_tab()
            
        return connections


    def get_user_from_post(self, url:str) -> str:
        self.driver.get(url)

        WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_element_by_css_selector('article[role=\'presentation\'] a'))
        
        user = self.driver.find_element_by_css_selector('article[role=\'presentation\'] a') \
                                .get_attribute('href').split('/')[-2]
        return user

    '''def read_comment(self):
        # Message Popup `Retry` (Timeout=Inf since this won't be an obstacle from the internet)
        WebDriverWait(self.driver, float('Inf'), 10).until_not(
            lambda x: x.find_element_by_tag_name('p'))

        while True:
            try:
                WebDriverWait(self.driver, self.timeout).until(
                    lambda x: x.find_element_by_css_selector('article[role=\'presentation\'] span[aria-label=\'Load more comments\']'))
                self.driver \
                    .find_element_by_css_selector('article[role=\'presentation\'] span[aria-label=\'Load more comments\']') \
                    .click()
            except TimeoutException:
                break
    '''
        
    def send_comment_like(self):
        WebDriverWait(self.driver, float('Inf'), 10).until_not(
            lambda x: x.find_element_by_tag_name('p'))
        for i in range(random.randint(2,5)):
            try:
                WebDriverWait(self.driver, self.timeout).until(
                    lambda x: x.find_element_by_css_selector('article[role=\'presentation\'] svg[aria-label=\'Like\']'))
                self.driver \
                    .find_element_by_css_selector('article[role=\'presentation\'] svg[aria-label=\'Like\']') \
                    .click()
                print('liked')
                time.sleep(random.randint(1,3))
            except TimeoutException:
                break

    def send_comment(self, comment:str):

        # Message Popup `Retry` (Timeout=Inf since this won't be an obstacle from the internet)
        WebDriverWait(self.driver, float('Inf'), 10).until_not(
            lambda x: x.find_element_by_tag_name('p'))

        # Text in Comment's Box
        if not self.driver.find_element_by_css_selector('article[role=\'presentation\'] form > textarea').text:

            # Click Comment's Box
            self.driver \
                    .find_element_by_css_selector('article[role=\'presentation\'] form > textarea') \
                    .click()

            # Write in Comment's Box
            comment_box = self.driver \
                    .find_element_by_css_selector('article[role=\'presentation\'] form > textarea') \
                    .send_keys(comment)
        
        # Click Post's Button to send Comment
        idx = 1
        baseSec = 30
        while True:
        # Click Button to send Comment
            self.driver \
              .find_element_by_css_selector('article[role=\'presentation\'] form > button[type=submit]') \
              .click()
            time.sleep(1)
            if (self.driver.find_element_by_css_selector('div.Z2m7o').text.find('post comment') >= 0):
                print(idx, 'cannot comment, gotta sleep', baseSec * idx, 'secs')
                self.send_comment_like()
                time.sleep(baseSec * idx)
                idx = idx + 1
            else:
                break

        # Wait the loading icon disappear
        WebDriverWait(self.driver, self.timeout).until_not(
            lambda x: x.find_element_by_css_selector('article[role=\'presentation\'] form > div'))
        
        
        
    def comment_post(self, url:str, expr:str, connections:List[str], count_comments:int):
        expr_parts = re.split(r'(?<!\\)@', expr)
        n = len(expr_parts) - 1

        if self.driver.current_url != url:
            self.driver.get(url)
            
            WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_element_by_css_selector('article[role=\'presentation\'] a'))
        
 
        def chunks() -> Iterator[str]: 
            for idx in range(0, (len(connections) // n) * n, n):  
                yield connections[idx:idx + n]

        comments = Comments(chunks(), expr_parts)

        idx = 1
        for comment in comments.generate():
            print(idx, ':', comment)
            self.send_comment(comment)
            time.sleep(random.randint(2,10))
            if (idx % 4 == 0):
                self.send_comment_like()
            idx = idx + 1
            if (idx > count_comments):
                break


    def close_driver(self):
        self.driver.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_driver()
