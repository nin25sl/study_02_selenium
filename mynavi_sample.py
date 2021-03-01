import os
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import traceback

def setup_class(cls):
    cls.driver = webdriver.Chrome(ChromeDriverManager().install())

def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

def mysearch_keyword(driver):
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    mySearchWord = input('Please search keyword>>')
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(mySearchWord)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    mySearchList = []
    searchList = driver.find_elements_by_class_name("cassetteRecruit__name")
    for search in searchList:
        mySearchList.append(search.text)
        print(search.text)

def writelog(logCentents):
    path = './log.txt'
    if not os.path.isfile(path):
        with open(path, mode='w') as f:
            f.write(logCentents)
    else:
        with open(path, mode = 'a') as f:
            f.write(logCentents)

# main処理
def main():
    search_keyword = "高収入"
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = webdriver.Chrome()
    # Webサイトを開く

    #難易度8 Chromeドライバーがバージョンアップの際に自動で更新されるようにしてみましょう。
    setup_class(driver)

    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_contain_list = []
    exp_midashi_list = []
    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
    for name in name_list:
        exp_name_list.append(name.text)
    print(len(exp_name_list))

    #難易度１　会社名以外の項目を取得して画面にprint文で表示してみましょう。
    #正社員か契約社員かどうかを取得
    midashi_list = driver.find_elements_by_class_name("labelEmploymentStatus")
    # 1ページ分繰り返し
    for midashi in midashi_list:
        exp_midashi_list.append(midashi_list.append)
    
    #難易度2 for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう
    #[会社名、表の見出し（仕事内容、給与など）,表の内容(文章)]を取得
    userselect_list = driver.find_elements_by_class_name('tableCondition')#.find_elements_by_tag_name("tbody")#.find_elements_by_tag_name('tr')#.find_element_by_class_name('tableCondition__body')
    userTable = []
    try:
        for userselect in userselect_list:
            #tempTable = userselect.find_element_by_tag_name("tbody")
            userTable.append(userselect.find_element_by_tag_name("tbody"))

        i = 0           
        for table in userTable:
            tempTr = table.find_elements_by_tag_name("tr")
            for tr in tempTr:
                tempHead = tr.find_element_by_class_name('tableCondition__head')
                tempBody = tr.find_element_by_class_name('tableCondition__body')
                exp_contain_list.append([exp_name_list[i], tempHead.text, tempBody.text])
            i += 1
    except:
        logCentents = traceback.format_exc()
        writelog(logCentents)
        pass
        #print(midashi.text)

    #難易度3 ２ページ目以降の情報も含めて取得できるようにしてみましょう
    #2ページ目を検索して、２ページ目の会社名を取得
    try:
        nextPagePath = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div/nav[2]/ul/li[2]/a').get_attribute('href')
        nextPage = driver.get(nextPagePath)
        #nextPage.click()

        exp_name_list_page2 = []
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        for name in name_list:
            exp_name_list_page2.append(name.text)
            #print(name.text)
        print(len(exp_name_list_page2))
    except:
        pass

    #難易度4 任意のキーワードをコンソール（黒い画面）から指定して検索できるようにしてみましょう
    #"高収入"と同じやり方を用いる。inputで値を受け取る。
    mysearch_keyword(driver)

    #難易度5 取得した結果をpandasモジュールを使ってCSVファイルに出力してみましょう
    #pd.DataFrameを用いて、取得した1ページ目の結果を出力する。
    df = pd.DataFrame(exp_contain_list,columns = ['社名','タイトル', '内容'])
    print(df.head(10))
    df.to_csv('./output.csv',encoding="utf_8-sig")

    #難易度6 エラーが発生した場合に、処理を停止させるのではなく、スキップして処理を継続できるようにしてみましょう(try文)
    try:
        name_list = driver.find_elements_by_class_name("xxx")
        for name in name_list:
            exp_name_list.append(name.text)
    except:
        #難易度7 処理の経過が分かりやすいようにログファイルを出力してみましょう
        logCentents = traceback.format_exc()
        writelog(logCentents)
        print("処理を飛ばすことに成功しました。")
        pass

    driver.quit()

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
