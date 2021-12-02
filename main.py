from selenium import webdriver
import time
import os
import urllib.error
import urllib.request

from selenium.webdriver.chrome.webdriver import WebDriver
from AutoMe_q.package import page as me_page
from ScrapeDesign.package import page as design_page
import glob

def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)


def get_spcase_design(driver:WebDriver, image_path:"絶対パス"):
    driver.get("https://me-q.i-designer.com/")
    design_page = me_page.DesignPage(driver)
    # iphone13 ハードケース デザインページに遷移
    design_page.set_SPCASE_HARD()
    # 画像アップロード
    design_page.add_image(image_path)
    time.sleep(1)
    # デザインを保存
    time.sleep(1)
    design_page.click_save_button()
    time.sleep(1)
    design_page.click_save_design_button()
    time.sleep(1)
    design_page.click_save_confirm_yes_button()
    time.sleep(5)
    # 最新のデザインidを取得
    id = design_page.get_latest_design_id()
    # デザインダウンロード
    url = "https://me-q.i-designer.com/save/"+id[:3]+"/"+id+"/"+id+"_0.png"
    download_file(url, f"case_image/{id}.png")
    time.sleep(5)

def main():
    root = os.getcwd()
    folder = fr"{root}\source_image"
    print(folder)
    pattern = fr"{folder}\*.png"
    path_list = glob.glob(pattern)
    # chromeドライバー設定
    driver = webdriver.Chrome()
    driver.implicitly_wait(20)
    for path in path_list[15::]:
        print(path)
        get_spcase_design(driver, path)
    driver.close()

if __name__ == '__main__':
    main()