import pandas as pd
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Load the Chrome browser and see it
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://localhost:5006")
    page.locator(".bk.bk-toolbar-button.bk-tool-icon-box-select").click()
    page.mouse.move(50, 50)
    page.mouse.down()
    page.mouse.move(100, 100)
    page.mouse.up()
    page.locator("text=SAVE").click()
    assert pd.read_csv("out.csv").shape[0] > 0
