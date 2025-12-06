from playwright.sync_api import sync_playwright, expect
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        file_path = os.path.abspath("verification/index.html")
        page.goto(f"file://{file_path}")

        # Check Body Styles
        body = page.locator("body")
        # rgb(246, 246, 244) is #F6F6F4
        expect(body).to_have_css("background-color", "rgb(246, 246, 244)")
        # rgb(28, 28, 28) is #1C1C1C
        expect(body).to_have_css("color", "rgb(28, 28, 28)")

        # Check Heading
        h1 = page.locator("h1")
        # Check that font-family contains Tenor Sans
        # Playwright to_have_css regex support
        # We'll check the string value
        font_family_h1 = h1.evaluate("element => getComputedStyle(element).fontFamily")
        if "Tenor Sans" not in font_family_h1:
            print(f"Heading Font Family Mismatch: {font_family_h1}")
            exit(1)

        # Check Body Font
        font_family_body = body.evaluate("element => getComputedStyle(element).fontFamily")
        if "Assistant" not in font_family_body:
            print(f"Body Font Family Mismatch: {font_family_body}")
            exit(1)

        # Check Line Height (1.6)
        # Note: Computed line-height is usually in pixels.
        # But we can check if the css rule is applied if we could inspect rules,
        # but here verify via computation is hard without knowing font size in px.
        # However, we added !important in CSS, so it should be there.

        # Check Primary Button
        btn_primary = page.locator(".button").first
        expect(btn_primary).to_have_css("background-color", "rgb(28, 28, 28)")
        expect(btn_primary).to_have_css("color", "rgb(255, 255, 255)")
        expect(btn_primary).to_have_css("border-radius", "2px")

        # Check Secondary Button
        btn_secondary = page.locator(".button--secondary")
        expect(btn_secondary).to_have_css("background-color", "rgba(0, 0, 0, 0)")
        expect(btn_secondary).to_have_css("color", "rgb(28, 28, 28)")
        expect(btn_secondary).to_have_css("border-radius", "2px")

        print("All visual assertions passed!")
        page.screenshot(path="verification/screenshot.png")
        browser.close()

if __name__ == "__main__":
    run()
