from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10) # seconds
driver.get("https://chancoding.tistory.com/199")
myDynamicElement = driver.find_element_by_class_name("area_title")