
# In[2]:


from selenium import webdriver
import time
import pandas as pd


# In[4]:


USER = "test_user"
PASS = "test_pw"


# In[19]:


browser = webdriver.Chrome()
browser.implicitly_wait(3)
browser.set_page_load_timeout(30)


# In[24]:


url_login = "https://kino-code.work/membership-login"
browser.get(url_login)
time.sleep(3)
print("アクセスしました")


# In[21]:


#htmlの要素をget
element = browser.find_element_by_id('swpm_user_name')
#要素の中身をクリア(中に情報が入っている可能性がある)
element.clear()
#文字列を送信する。
element.send_keys(USER)
element = browser.find_element_by_id('swpm_password')
element.clear()
element.send_keys(PASS)
print('フォームを送信')


# In[23]:


browser_from = browser.find_element_by_name('swpm-login')
time.sleep(3)
browser_from.click()
print("情報を入力してログインしました。")

frm = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div/main/article/div/p[2]/button')
time.sleep(1)
frm.click()
print('ダウンロードをクリック')
# In[ ]:




