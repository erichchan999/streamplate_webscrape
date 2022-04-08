# Uses selenium to scrape youtube comments

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Change pathname here to your browser's webdriver
# For this task I've used chrome's webdriver
s = Service("/Users/ericchan/Desktop/streamplate/streamplate_webscrape/chromedriver")

chrome_options = Options()
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=s, options=chrome_options)
driver.implicitly_wait(1)

driver.get("https://www.youtube.com/results?search_query=ukraine")

res = {}

with open('output.json', 'w') as out:
    try:
        for i in range(1, 11):
            video = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="contents"]/ytd-video-renderer[{i}]'))
            )

            title = video.find_element(By.ID, "video-title")

            url = title.get_attribute("href")

            print(f'-----Video {i}: {title.text}-----')
            title.click()

            time.sleep(8)

            driver.execute_script("window.scrollTo(0, 400);")

            time.sleep(2)
        
            comments = WebDriverWait(driver, timeout=10).until(
                EC.presence_of_element_located((By.ID, 'comments'))
            )

            comments_list = comments.find_elements(By.ID, 'content-text')

            c_list = []
            if comments_list:
                for j in range(0, 3):
                    print(f'Comment {j+1}:')
                    print(comments_list[j].text)
                    c_list.append(comments_list[j].text)
            else:
                print('comments were disabled')
                c_list.append('comments were disabled')
                
            res[url] = c_list

            driver.back()

        driver.close()
    except:
        print('Something went wrong...')
        print('Closing webdriver')
        driver.close()

    out.write(json.dumps(res))
