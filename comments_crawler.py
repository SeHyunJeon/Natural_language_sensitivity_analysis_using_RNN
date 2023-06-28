from selenium import webdriver as wd
from bs4 import BeautifulSoup
import time
import tkinter as tk
import pandas as pd
import sys

def open_youtube():
    global url  # 전역 변수로 선언
    url = entry.get()
    if url == '':   
        print("주소를 입력하지 않으셨습니다.")
        window.destroy()
        sys.exit()
    else:
        print("입력한 주소:", url)

# 윈도우 생성
window = tk.Tk()

# 윈도우 사이즈 조정
window.geometry('500x100')

# 레이블 생성
label = tk.Label(window, text="유튜브 주소를 입력하세요:")
label.pack()

# 텍스트 입력 상자 생성
entry = tk.Entry(window)
entry.pack()

# 버튼 생성
button = tk.Button(window, text="열기", command=open_youtube)
button.pack()

# 윈도우 실행
window.mainloop()

#---------------------------------------------------

driver = wd.Chrome(executable_path="chromedriver")
    

driver.get(url)

last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

time.sleep(5)

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(3.0)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height
    

html_source = driver.page_source


driver.quit()  # WebDriver 종료

soup = BeautifulSoup(html_source, 'lxml')

youtube_comments = soup.select('yt-formatted-string#content-text')

str_youtube_comments = []

for i in range(len(youtube_comments)):
    str_tmp = str(youtube_comments[i].text)
    str_tmp = str(youtube_comments[i].text) 
    str_tmp = str_tmp.replace('\n', '')
    str_tmp = str_tmp.replace('\t', '')
    str_tmp = str_tmp.replace('               ', '')
    
    str_youtube_comments.append(str_tmp)
      
pd_data = {"comment" : str_youtube_comments}
youtube_pd = pd.DataFrame(pd_data)
idx = youtube_pd[youtube_pd['comment'] == ''].index
youtube_pd.drop(idx, inplace=True)

youtube_pd.to_csv("comments.csv")