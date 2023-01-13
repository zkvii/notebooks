from translation import translate, text_translate
import pandas as pd
from tqdm import tqdm
from news import News,save_news,load_news
import pickle
# coding=utf-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
profile = r'C:\Users\zerk\AppData\Roaming\Mozilla\Firefox\Profiles\bld0m1rx.default-release'
options = Options()
# options.headless = True
# options.set_preference('profile', profile)
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
service = Service(r'C:\Users\zerk\notebooks\geckodriver.exe')
base_url='https://mp.toutiao.com/profile_v4/graphic/publish'
wtt='https://mp.toutiao.com/profile_v4/weitoutiao/publish'
# article

if __name__ == '__main__':
    #load news
    articles = load_news()
    #translate news using tencent translate
    print(f'start translating {len(articles)} articles')
    for article in tqdm(articles[:13]):
        if article.is_translated is None or article.is_translated == 0:
            article.zh_title = text_translate(article.news_title)
            article.zh_author = text_translate(article.news_author)
            article.zh_content = text_translate(
                article.news_content.replace('\n', ' '))
            article.is_translated = 1
            time.sleep(1)
    #save translated news
    save_news(articles)
    driver = webdriver.Firefox(
        firefox_profile=profile, service=service, options=options)
    # for sample in tqdm(articles[:10]):
    #     if sample.is_translated == 1 and sample.is_submit_toutiao == 0:
            
    #submit news to toutiao
    print('--------------------------start submitting----------------------------------')
    for sample in tqdm(articles[:13]):
        if sample.is_translated == 1 and sample.is_submit_toutiao == 0:
            try:
            # single title

                driver.get(base_url)
                # WebDriverWait(driver, 3)
                time.sleep(5)
                # driver.implicitly_wait(5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # Y is the height of the page
                time.sleep(1)
                driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/label[1]/span/div').click()
                # claim no image
                time.sleep(1)
                driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/label[3]/span/div').click()
                # claim origin
                driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[3]/div/div[2]/div/div/span/label/span/div').click()
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, 0)") # Y is the height of the page
                #title element
                # title_textarea = driver.find_element(
                #     By.XPATH, '/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/textarea')
                title_textarea = driver.find_element(By.TAG_NAME,'textarea')
                title_textarea.send_keys(sample.zh_title)
                #content element
                # driver.find_element(By.CLASS_NAME,'ProseMirror').send_keys(sample.zh_content)
                content = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div/div[1]/div[3]/div/div[1]')
                content.send_keys(sample.zh_content)

                driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div/div[3]/div/button[1]').click()    
                time.sleep(3)
                # WebDriverWait(driver, 3)
                #do not pub

                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # Y is the height of the page
                # # pub
                # driver.find_element(
                #     By.XPATH, '/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div/div[3]/div/button[3]').click()
                # # re affirm
                # time.sleep(2)
                # driver.find_element(
                #     By.XPATH, '/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div/div[3]/div/button[2]').click()
                #success submit to caogao
                sample.is_submit_toutiao = 1
                save_news(articles)
                print('-----------------------------submit to toutiao caogao success-----------------------------')
                print(f'title: {sample.zh_title}')
            except Exception as e:
                print(e)
                continue
            
    articles_dict = [vars(a) for a in articles]
    df_articles = pd.DataFrame(articles_dict)
    df_articles.to_csv('africa_news.csv', index=False)
