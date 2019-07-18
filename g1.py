import json
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from selenium import webdriver

ROOTDIR = os.path.dirname(__file__) 

# set to use chrome driver
options = Options()
options.add_argument('--headless')

browser = webdriver.Chrome(chrome_options=options,executable_path=ROOTDIR + '/chromedriver')

# access g1 page
browser.get('https://g1.globo.com/')

# await page load
timeout = 5
try:
    el = EC.presence_of_element_located((By.CLASS_NAME, 'feed-post-figure-link'))
    WebDriverWait(browser, timeout).until(el)
except TimeoutException:
    print('timeout exceded')

# find all feed-post elements
feeds_div = browser.find_elements_by_class_name('feed-post')

# create a list to receive feeds
i = 0
feeds = []

# foreach feed element trace
for feed in feeds_div:

    # get only the 3 first feeds
    if i == 3:
        break

    title = None
    link = None
    description = None
    img = None

    # get the title text and link
    try:
        feed_title_a = feed.find_element_by_class_name('feed-post-link')
        title = feed_title_a.text
        link = feed_title_a.get_attribute('href')
    except:
        pass

    # get the resume of feed
    try:
        feed_description_div = feed.find_element_by_class_name('feed-post-body')
        description = feed_description_div.text
    except:
        pass

    # get them image url
    try:
        feed_picture = feed.find_element_by_class_name('feed-post-figure-link').find_element_by_tag_name('img')
        img = feed_picture.get_attribute('src')
    except:
        pass

    # add json object with data in list
    feeds.append({
        'title': title,
        'link': link,
        'description': description,
        'img': img
    })

    # up iter counter
    i+=1

# parse fields into json string
feeds = [json.dumps(item) for item in feeds]

# print data
print(feeds)