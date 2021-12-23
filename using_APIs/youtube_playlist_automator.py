# importing microsoft edge webdriver from selenium
from selenium.webdriver import Edge
from msedge.selenium_tools import EdgeOptions
import time 

# assigning the path of the msedgedriver.exe file and then assigning that to the executable path to follow
class Youtube():
    def __init__(self):
        self.PATH = "C:\Program Files (x86)\Microsoft\msedgedriver.exe"
        self.opt = EdgeOptions()
        self.opt.use_chromium = True
        self.driver = Edge(options=self.opt)
        self.driver.get("https://youtube.com")

        # allowing webpage to load before clicking sign in 
        time.sleep(2)


    def login(self):
        # clicking sign in 
        sign_in_btn = self.driver.find_element_by_xpath('//*[@id="buttons"]/ytd-button-renderer')
        sign_in_btn.click()
        # entering email and password 

if __name__ == '__main__':
    pass
