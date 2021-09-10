from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

def insta_searching(word):
    url = "https://www.instagram.com/explore/tags/" + str(word)
    return url

def select_first(driver):
    first = driver.find_elements_by_css_selector("div._9AhH0")[0]
    first.click()
    time.sleep(3)

def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    try:
        content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ' '
    
    tags = re.findall(r'#[^\s#,\\]+', content)
    
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
    print(soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10])
    
    try:
        like = soup.select('div.Nm9Fw a span')[0].text
    except:
        like = 0
    
    try:
        place = soup.select('div.M30cS')[0].text
    except:
        place = ''
    
    data = [content, date, like, place, tags]
    return data

def move_next(driver):
    right = driver.find_element_by_css_selector ('a.coreSpriteRightPaginationArrow')
    right.click()
    time.sleep(3)

driver = webdriver.Chrome('chromedriver.exe')

driver.get('https://www.instagram.com')
time.sleep(3)

email = ''
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(email)

password = ''
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()

time.sleep(5)

word = input('검색어를 입력하세요 : ')
word = str(word)
url = insta_searching(word)

driver.get(url)
time.sleep(5)

select_first(driver)

results = []

target = 10

for i in range(target):
    try:
        data = get_content(driver)
        results.append(data)
        move_next(driver)
    except:
        time.sleep(2)
        move_next(driver)

results
type(results)
import pandas as pd

results_df = pd.DataFrame(results)
results_df.columns = ['content', 'date', 'like', 'place', 'tags']
results_df.to_excel('morning.xlsx')

results_df

#pip install lxml
#