"""Test login page UI with Playwright."""

from playwright.sync_api import sync_playwright


def test_login_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the static HTML file
        page.goto(
            "file:///Users/mykielee/GitHub/my_projects/claude-code-python/src/api/login_page.html"
        )
        page.wait_for_load_state("networkidle")

        # Take screenshot for visual verification
        page.screenshot(path="/tmp/login_page.png", full_page=True)

        # Check page title
        title = page.title()
        print(f"Page title: {title}")
        assert title == "Secure Login - NexaBank", f"Unexpected title: {title}"

        # Verify key elements exist
        assert page.locator("#country").is_visible(), "Country selector not visible"
        assert page.locator("#email").is_visible(), "Email input not visible"
        assert page.locator("#password").is_visible(), "Password input not visible"
        assert page.locator("#remember").is_visible(), "Remember me checkbox not visible"
        assert page.locator(".submit-btn").is_visible(), "Submit button not visible"

        # Check country dropdown has options
        country_options = page.locator("#country option").count()
        print(f"Country options found: {country_options}")
        assert country_options > 10, f"Expected multiple countries, found {country_options}"

        # Check footer links
        footer_links = page.locator(".footer-links a").count()
        print(f"Footer links found: {footer_links}")
        assert footer_links >= 3, f"Expected at least 3 footer links, found {footer_links}"

        # Verify security badge is present
        assert page.locator(".security-badge").is_visible(), "Security badge not visible"

        # Check for loading spinner (hidden by default)
        spinner = page.locator(".spinner")
        assert not spinner.is_visible(), "Spinner should be hidden initially"

        # Check error message is hidden initially
        error_msg = page.locator(".error-message")
        assert not error_msg.is_visible(), "Error message should be hidden initially"

        print("\n✓ All UI tests passed!")
        print("✓ Screenshot saved to /tmp/login_page.png")

        browser.close()


if __name__ == "__main__":
    test_login_page()
