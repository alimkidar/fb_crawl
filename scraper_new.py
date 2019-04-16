import getpass
import calendar
import os
import platform
import sys
import urllib.request
import re, time
from bs4 import BeautifulSoup as soup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

def ts2dt_jakarta(ts):
    try:
        ts = int(ts)
        offset = 3600 * 7
        ts = ts + offset
        return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return '-'
def load_fb():
    global driver

    options = Options()

    #  Code to disable notifications pop up of Chrome Browser
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    # options.add_argument("headless")

    try:
        platform_ = platform.system().lower()
        if platform_ in ['linux', 'darwin']:
            driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
        else:
            driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
    except:
        print("Kindly replace the Chrome Web Driver with the latest one from"
            "http://chromedriver.chromium.org/downloads"
            "\nYour OS: {}".format(platform_)
            )
        exit()

    driver.get("https://en-gb.facebook.com")
    driver.maximize_window()

def login(email, password):
    driver.find_element_by_name('email').send_keys(email)
    driver.find_element_by_name('pass').send_keys(password)
    # clicking on login button
    driver.find_element_by_id('loginbutton').click()
def go_to(url):
    try:
        driver.get(url)
    except:
        pass
# def get_post_group():
#     all_posts = []
#     # open all see more
#     x = driver.find_elements_by_class_name('see_more_link')
#     for i in x:
#         try:
#              i.click()
#         except:
#             pass
#     # get attribute: all post text
#     contentsc = driver.find_elements_by_xpath("//div[@class='_5pcr userContentWrapper']")
#     contents = []
#     for i in contentsc:
#         contents.append(i)
#     # get attribute: link to the post
#     urlsc = driver.find_elements_by_xpath("//span[@class='fsm fwn fcg']/a[@class='_5pcq']")
#     urlsx_ = []
#     for url in urlsc:
#         urlsx_.append(url)
#     urlsc = driver.find_elements_by_xpath("//span[@class='fsm fwn fcg']/a[@class='_5pcq']/abbr")
#     urlsx = []
#     for x in urlsx_:
#         lokasi_attr = x.get_attribute('data-hovercard')
#         if lokasi_attr is None:
#             urlsx.append(x)
#     # get attribute: timestamp
#     urlsz = []
#     for url in urlsc:
#         urlsz.append(url)
#     # get attribute: profile link
#     profsc = driver.find_elements_by_xpath("//a[@class='_5pb8 i_wvgj7bm5z _8o _8s lfloat _ohe']")
#     profs = []
#     for i in profsc:
#         profs.append(i.get_attribute('href').split("&")[0])
#     # get all data
#     # parsing
#     # etc.
#     for i in range(len(contents)):
#         content = contents[i].text
#         prof_link = clean_url(profs[i])
#         username = get_username(prof_link)
#         bedge = get_bedge(content)
#         dtime = urlsx[i].text
#         ts = urlsz[i].get_attribute('data-utime')
#         dtime_jkt = ts2dt_jakarta(ts)
#         post_url = urlsx[i].get_attribute('href')
#         name = get_name(content, bedge, dtime)
#         clear_content = make_clear_content(content, dtime)
#         comments_count = get_comment(content)
#         temp_numbs = re.findall(r"\d+",clear_content)
#         likes = temp_numbs[len(temp_numbs)-1]
#         parm = str(likes) + ".*" + str(likes) + ".*"
#         convo = re.sub(parm, '', clear_content)
#         all_posts.append({'name':name,
#         'prof_link':prof_link,
#         'username':username,
#         'bedge':bedge,
#         'time(gmt+7)':dtime_jkt,
#         'timestamp':ts,
#         'post_url':post_url,
#         'convo':anti_ws(convo),
#         'likes_count':likes,
#         'comments_count':comments_count
#         })
#     return all_posts
def generate_data(source):
    content_wrappers = driver.find_elements_by_xpath("//div[@class='_5pcr userContentWrapper']")
    contents = []
    for i in content_wrappers:
        str_html = i.get_attribute('innerHTML')
        contents += get_attrib(str_html, source)
    return contents

def get_attrib(html, source):
    bucket = []
    page_html = soup(html, 'html')
    x1 = page_html.find_all('h5')
    try:
        nama = x1[0].text
    except:
        nama = ''
    try:
        prof_link = clean_prof_link(x1[0].a['href'])
    except:
        prof_link = ''

    x2 = page_html.find_all('span', class_="_4bo_")
    try:
        bedge = x2[0].text
    except:
        bedge = ''

    x4 = page_html.find_all('a',class_='_5pcq')
    try:
        ts = x4[0].abbr['data-utime']
    except:
        ts = ''
    try:
        post_url = 'https://www.facebook.com' + x4[0]['href']
    except:
        post_url = ''

    x5 = page_html.find_all('p')
    try:
        convo = ''
        for i in x5:
            convo += i.text + '/n'
        convo = str(convo).strip()
        # convo = x5[0].text
    except:
        convo = ''

    x6 = page_html.find_all('span', class_='_3dlh _3dli')
    try:
        like_count = x6[0].text
    except:
        like_count = ''

    x7 = page_html.find_all('span', class_='_1whp _4vn2')
    try:
        comment_count = x7[0].text.split()[0]
    except:
        comment_count = ''
    x_foto = page_html.findAll('a',rel='theater')

    foto_count = str(len(x))

    username = get_username(prof_link)
    bucket.append({
        'name': nama,
        'username': username,
        'bedge': bedge,
        'prof_link': prof_link,
        'time(gmt+7)': ts2dt_jakarta(ts),
        'timestamp': ts,
        'post_utl': post_url,
        'convo': convo,
        'likes_count': str(like_count),
        'comments_count': str(comment_count),
        'photos_count': foto_count,
        'source': source    
    })
    return bucket
def clean_prof_link (prof_link):
    if 'profile.php?id=' in prof_link:
        x = prof_link.split('&')[0]
    else:
        x = prof_link.split('?')[0]
    return x
def open_seemore():
    # open all see more
    x = driver.find_elements_by_class_name('see_more_link')
    for i in x:
        try:
            i.click()
        except:
            pass
    
# def clean_url(url):
#     if 'profile.php?id=' not in url:
#         url = url.split('?')[0]
#     return url
def get_username(url):
    username = url.replace('https://www.facebook.com/','').replace('profile.php?','')
    return username
def get_comment(content):
    x = content.split('Comments')[0]
    xs = re.findall(r"\d+", x)
    if len(xs) > 0:
        x = xs[len(xs)-1]
    else:
        x = 0
    return x
def anti_ws(string):
    string = string.replace(',','|')
    string = string.replace('\n',' ')
    string = string.replace('\t',' ')
    string = string.strip()
    return string
def get_bedge(string):
    bedges = ['Admin', 'Moderator', 'New Member', 'Group Anniversary', 'Conversation Starter', 'Founding Member', 'Conversation Booster', 'Visual Storyteller', 'Greeter', 'Link Curator', 'Rising Star']
    bedge='TIDAK ADA BEDGE'
    for x in bedges:
        if x in string:
            bedge=x
    return bedge

        
def make_clear_content(content, dtime):
    cc = re.sub(r"Like.+","",content)
    cc_ = cc.split(dtime)
    return cc_[1]

def get_name(content, bedge, dtime):
    nama = 'invalid'
    if ' is at ' in content:
        x1 = content.replace('is at','|-|', 1)
        x2 = x1.split('|-|')
        nama = x2[0]
        # print('is at')
    elif bedge in content:
        x1 = content.replace(bedge,'|-|', 1)
        x2 = x1.split('|-|')
        nama = x2[0]
        # print('bedge')
    elif dtime in content:
        x1 = content.replace(dtime,'|-|', 1)
        x2 = x1.split('|-|')
        nama = x2[0]
        # print('date')
    else:
        # print('kosong')
        nama = 'invalid'
    return nama.strip()

def scroll(times):
    x = 0
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while x != times:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        x += 1