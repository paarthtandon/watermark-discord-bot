import discord
import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
driver = webdriver.Firefox(capabilities=cap, executable_path='./geckodriver')

def get_sauce(url):
    driver.get('https://saucenao.com/')
    advanced = driver.find_element_by_class_name('style7')
    advanced.click()
    url_box = driver.find_element_by_name('url')
    url_box.send_keys(url)
    url_box.submit()
    time.sleep(3)
    return driver.find_element_by_css_selector('div.result:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(2) > div:nth-child(2) > a:nth-child(2)').get_attribute('href')
    results = driver.find_elements_by_class_name('resultcontentcolumn')
    sauces = []
    for result in results:
        print(result)
        result.find_element_by_class_name('linkify')
        sauces.append(result.get_attribute('href'))
    return sauces

def get_links(url):
    headers = {"user-agent" : USER_AGENT}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    results = []
    time.sleep(10 + random.random())
    for g in soup.find_all('div', class_='r'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            results.append(link)
    print(results)
    return results

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if len(message.attachments) != 0:
            await message.channel.send(content="Processing image...")
            out = ""
            url = message.attachments[0].url
            print(url)
            results = get_sauce(url)
            await message.channel.send(content=results);

client = MyClient()

code_file = open('./priv/code', 'r')
client.run(code_file.readline())
code_file.close()

