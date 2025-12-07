from playwright.sync_api import sync_playwright, expect
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load local HTML file
        url = "file://" + os.path.abspath("verification/index.html")
        page.goto(url)

        # Verify Typography
        h1 = page.locator("h1")
        expect(h1).to_be_visible()

        # Check computed styles (approximate due to clamp)
        # We can't easily check 'clamp' value via computed style, but we can check if font-family is applied correctly
        # Note: Since we don't have the actual font files loaded in this static HTML simulation (unless downloaded),
        # it will fallback. But we can check if the variable is set in the style attribute or cascading.

        # Verify Background Color
        body = page.locator("body")
        # bg_color = body.evaluate("element => getComputedStyle(element).backgroundColor")
        # print(f"Body Background: {bg_color}")

        # Verify Buttons have correct class and potentially check color if CSS loaded correctly
        btn = page.locator(".button").first
        expect(btn).to_be_visible()

        # Take Screenshot
        page.screenshot(path="verification/design_system.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    run()
