# -*- coding: utf-8 -*-
"""
Created on Wed 10 21:42:42 2021
@author: Ghulam Mustafa
"""
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from os.path import isfile, join
import shutil,csv,os,time
options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : 'C:\\Project5ver\\Reddit\\Media'}
options.add_experimental_option('prefs', prefs)
# driver = webdriver.Chrome(ChromeDriverManager().install())  #For Chrome
driver = webdriver.Chrome('C:\\Project5ver\\Reddit\\chromedriver.exe',chrome_options=options)
wait = WebDriverWait(driver, 10)

# User credentials
user="Mgcoder"
pwd="fool_751"



# Wait until file downloade.    
def download_wait(path_to_downloads):
    for fname in os.listdir(path_to_downloads):
        if fname.endswith('.crdownload'):
            time.sleep(5)
            download_wait('C:/Project5ver/Reddit/Media')
    # Remove Prefix
    rootdir = path_to_downloads
    str = "redditsave.com_"
    for filename in os.listdir(rootdir):
        if str in filename:
            filepath = os.path.join(rootdir, filename)
            newfilepath = os.path.join(rootdir, filename.replace(str, ""))
            os.rename(filepath, newfilepath)
    # Move & Media Loc
    for fn in os.listdir(rootdir):
        if fn.endswith('mp4') or fn.endswith('MKV') or fn.endswith('3gp'):
            fol = fn.split('.')[0]
            fol_path = f'C:/Project5ver/Reddit/Media/{fol}'
            os.mkdir(fol_path)
            fn_path = os.path.join(rootdir, fn)
            shutil.move(fn_path,fol_path)
            media = f'{fol_path}/{fn}'
            data['Media_Location'].append(media)

# Dic for dataframe (df)
data = {'URL':[],'Title':[],'Comments':[],'Photo_Location':[],'Media_Location':[]}

# Login to Reddit.com
url = 'https://www.reddit.com/login/'
driver.get(url)
driver.maximize_window()
driver.find_element(By.CSS_SELECTOR, '#loginUsername').send_keys(user)
driver.find_element(By.CSS_SELECTOR, '#loginPassword').send_keys(pwd)
driver.find_element(By.CSS_SELECTOR, '.m-full-width').click()
driver.get('https://www.reddit.com/search/?q=cat&sort=hot&t=day')

# Get first post links
posts = []
for i in range(1,15):
    # wait.until(EC.visibility_of_element_located((By.XPATH, f'(//*[@class="_eYtD2XCVieq6emjKBH3m"]/span)[{i}]')))
    pstitle = driver.find_element(By.XPATH, f'(//*[@class="_eYtD2XCVieq6emjKBH3m"]/span)[{i}]').text
    pslink = driver.find_element(By.XPATH, f'(//*[@class="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"])[{i}]').get_attribute('href')
    posts.append(pslink)
media_links = []

n = 1
for url in posts:
    driver.get(url)
    # Title
    try:
        psdata_title = driver.find_element(By.XPATH, '(//h1[@class="_eYtD2XCVieq6emjKBH3m"])[2]').text
    except:
        psdata_title = driver.find_element(By.XPATH, '(//h1[@class="_eYtD2XCVieq6emjKBH3m"])').text
    
    print('Post Title: ',psdata_title)

    # Comments
    comments = []
    for i in range(1,4):
        comment = driver.find_element(By.XPATH, f'(//*[@class="_1qeIAgB0cPwnLhDF9XSiJM"])[{i}]').text
        comments.append(comment)
    
    print('Comments:',comments)

    try:
        psdata_photo = driver.find_element(By.CSS_SELECTOR, '._3Oa0THmZ3f5iZXAQ0hBJ0k>a').get_attribute('href')
    except:
        psdata_photo = 'None'
    try:
        psdata_media = driver.find_element(By.CSS_SELECTOR, 'video._1EQJpXY7ExS04odI1YBBlj')
    except:
        psdata_media = 'None'
    
    if psdata_photo != 'None' or psdata_media != 'None':
        
        data['URL'].append(url)
        data['Title'].append(psdata_title)
        data['Comments'].append(comments)
        
        if psdata_photo != 'None':
            print(psdata_photo)
            os.mkdir(f'C:\\Project5ver\\Reddit\\Photos\\300{n}')
            os.chdir(f'C:\\Project5ver\\Reddit\\Photos\\300{n}')
            driver.get(psdata_photo)
            driver.save_screenshot(f"{n}000.png")
            loc_photo = f'C:/Project5ver/Reddit/Photos/300{n}/{n}000.png'
            data['Photo_Location'].append(loc_photo)
            print('Photo Location: ',loc_photo)
            os.chdir('C:\Project5ver\Reddit')
            n+=1
        else:
            data['Photo_Location'].append('None')

        if psdata_media != 'None':
            psdata_media = driver.find_element(By.CSS_SELECTOR, 'video._1EQJpXY7ExS04odI1YBBlj')
            driver.get('https://redditsave.com/')
            driver.find_element(By.CSS_SELECTOR, '#url').send_keys(url)
            driver.find_element(By.CSS_SELECTOR, '#download').click()
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.download-info>a')))
            saveV = driver.find_element(By.CSS_SELECTOR, '.download-info>a')
            driver.execute_script("arguments[0].click();", saveV)
            time.sleep(5)
            download_wait('C:/Project5ver/Reddit/Media')
        else:
            data['Media_Location'].append('None')
    else:
        continue

# DF_Csv
df = pd.DataFrame.from_dict(data, orient='index')
df.to_csv('Reddit.csv', encoding='utf-8')
print(df)

