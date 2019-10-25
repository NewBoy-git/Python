from selenium import webdriver

fireFoxOptions = webdriver.FirefoxOptions()

fireFoxOptions.set_headless()

brower = webdriver.Firefox(executable_path='/home/xihonglin/Flask/testSiteCrawlApi/geckodriver',firefox_options=fireFoxOptions)

brower.get('http://www.baidu.com')

print(brower.page_source)

brower.close()