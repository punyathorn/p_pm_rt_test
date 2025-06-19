from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#Change chrome driver path accordingly
ser = Service(r"D:\All py\ACT-Auto-Login\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=ser, options=chrome_options)
print(driver.title)
from selenium.webdriver.common.by import By

i = 0
while i == 0:
    print("Searching for register button...")
    buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Register')]")
    for btn in buttons:
        if 'register' in btn.text.lower():
            print("Found button:", btn.text)
            btn.click()
            i = 1
            break
        else:
            print("Button not found, waiting...")
            driver.implicitly_wait(1)

if i == 1:
    print("Waiting for 'Central Ladprao' button to appear...")
    j = 0
    while j == 0:
        buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Central Ladprao')]")
        for btn in buttons:
            if 'central ladprao' in btn.text.lower():
                print("Found button:", btn.text)
                btn.click()
                j = 1
                break
            else:
                driver.implicitly_wait(1)
                # If "Central Ladprao" button not found, click "X" and then "Register" again
                x_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'X')]")
                if x_buttons:
                    print("Clicking X button to close dialog")
                    x_buttons[0].click()
                    driver.implicitly_wait(1)
                register_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Register')]")
                for btn in register_buttons:
                    if 'register' in btn.text.lower():
                        print("Clicking Register button again")
                        btn.click()
                        driver.implicitly_wait(1)
                        break

    if j == 1:
        element = driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Select Date & Time Booking')]"))
        )
        driver.execute_script("window.scrollBy(0, 500);")
        dates = driver.find_elements(By.XPATH, "//td[not(contains(@style, 'opacity: 0.5')) and not(contains(@class, 'disabled')) and text() != '']")
        available_dates = []
        for el in dates:
            try:
                text = el.text.strip()
                if text.isdigit():
                    # Check opacity or disabled class to ignore grayed out
                    style = el.get_attribute('style') or ''
                    if 'opacity: 1' in style or 'disabled' not in el.get_attribute('class'):
                        available_dates.append((int(text), el))
            except Exception as e:
                continue
        if available_dates:
            earliest = sorted(available_dates, key=lambda x: x[0])[0]
            print(f"Clicking earliest date: {earliest[0]}")
            driver.execute_script("arguments[0].scrollIntoView();", earliest[1])
            earliest[1].click()
        else:
            print("No available date found.")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Select Time')]"))
        )
        driver.execute_script("window.scrollBy(0, 500);")
        driver.find_element(By.XPATH, "//*[contains(text(), '12:30')]").click()
        driver.execute_script("window.scrollBy(0, 500);")
        driver.find_element(By.XPATH, "//*[contains(text(), 'Confirm')]").click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "input[@type='checkbox']"))
        )
        checkbox = driver.find_element(By.XPATH, "input[@type='checkbox']")
        if not checkbox.is_selected():
            checkbox.click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Confirm Booking')]"))
        )
        confirm_booking_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Confirm Booking')]")
        confirm_booking_button.click()
        print("Booking Successful")
