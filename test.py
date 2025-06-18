url = "https://popmartth.rocket-booking.app/booking"

import time
import nodriver as uc
from selenium.webdriver.common.by import By
import asyncio

async def main():

    browser = await uc.start()
    page = await browser.get(url)
    await browser.wait(2)
    await page.wait_for(text="โปรไฟล์", timeout=5000)
    await browser.wait(2)  # wait for the page to load
    print('gonna find element')
    btn = await page.find("โปรไฟล์", best_match=True)
    print(btn)
    if btn:
        await btn.mouse_click()
    await page.wait_for(text="connect", timeout=5000)
    btn = await page.find("connect", best_match=True)
    print(btn)
    if btn:
        await btn.mouse_click()
    await browser.wait(1)
    btn = await page.find("Connect Line Account*", best_match=True)
    await btn.mouse_click()
    print(btn)
    await browser.wait(1)
    await page.wait_for(selector="input[type='text'][name='tid']", timeout=10000)
    email = await page.select("input[type='text'][name='tid']")
    await browser.wait(0.1)   
    await email.send_keys("line_email@gmail.com")
    await browser.wait(0.1)
    password = await page.select("input[type='password'][name='tpasswd']")
    await browser.wait(0.1)   
    await password.send_keys("password")   
    btn = await page.find("Log in", best_match=True)
    await btn.mouse_click()
    #await browser.wait(10)  # wait for the login to complete
    i = 0
    while i == 0:
        if await page.find("Booking", best_match=True):
            print("Booking button found")
            i = 1
        else:
            await browser.wait(1)
    j = 0
    while j == 0:
        if await page.find("Register", best_match=True):
            print("Register button found")
            j = 1
        else:
            await browser.wait(1)

    await page.wait_for(text="Register", timeout=20000)
    btn = await page.find("Register", best_match=True)
    await btn.mouse_click()
    await page.wait_for(text="Central Ladprao", timeout=20000)
    btn = await page.find("Central Ladprao", best_match=True)
    await btn.mouse_click()
    await page.scroll_down(50)
    btn = await page.find("Next", best_match=True)
    await btn.mouse_click()
    await page.wait_for(text="Select Date & Time Booking", timeout=5000)
    await page.scroll_down(50)
    dates = page.query_selector_all('td >> visible=true')
    available_dates = []
    for el in dates:
        try:
            style = el.get_property('style') or ''
            text = el.inner_text().strip()

            if text.isdigit():
                # Check opacity or disabled class to ignore grayed out
                opacity = el.evaluate("e => window.getComputedStyle(e).opacity")
                if float(opacity) >= 1:
                    available_dates.append((int(text), el))
        except Exception as e:
            continue
    if available_dates:
        earliest = sorted(available_dates, key=lambda x: x[0])[0]
        print(f"Clicking earliest date: {earliest[0]}")
        earliest[1].mouse_click()
    else:
        print("No available date found.")
    await page.wait_for(text="Select Time", timeout=5000)
    await page.scroll_down(50)
    btn = await page.find("12:30", best_match=True)
    opacity = await btn.evaluate("e => window.getComputedStyle(e).opacity")
    if float(opacity) >= 1:
        await btn.mouse_click()
    else:
        print("12:30 is unavailable.")
    await page.scroll_down(50)
    await page.wait_for(text="Confirm", timeout=5000)
    btn = await page.find("Confirm", best_match=True)
    await btn.mouse_click()
    await page.wait_for(selector="input[type='checkbox']", timeout=5000)
    btn = await page.select("input[type='checkbox']")
    await btn.mouse_click()
    # await page.wait_for(text="Confirm Booking", timeout=5000)
    # btn = await page.find("Confirm Booking", best_match=True)
    # await btn.mouse_click()
    # await page.wait_for(text="Booking Successful", timeout=5000)
    # print("Booking Successful")
    # await browser.wait(5) 
    print('gonna quit')
    await browser.wait(20)
    #await browser.quit()

if __name__ == '__main__':
    uc.loop().run_until_complete(main())