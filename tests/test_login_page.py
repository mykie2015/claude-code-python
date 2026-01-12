"""Test modernized login page UI with Playwright."""

from playwright.sync_api import sync_playwright


def test_modernized_login_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the static HTML file
        page.goto(
            "file:///Users/mykielee/GitHub/my_projects/claude-code-python/.worktrees/auth-mvp/src/api/login_page.html"
        )
        page.wait_for_load_state("networkidle")

        # Check page title
        title = page.title()
        print(f"Page title: {title}")
        assert title == "Sign In - NexaBank", f"Unexpected title: {title}"

        # Verify key elements exist with new selectors
        assert page.locator("#country").is_visible(), "Country selector not visible"
        assert page.locator("#email").is_visible(), "Email input not visible"
        assert page.locator("#password").is_visible(), "Password input not visible"
        assert page.locator("#remember").is_visible(), "Remember me checkbox not visible"
        assert page.locator(".submit-btn").is_visible(), "Submit button not visible"

        # Verify brand elements
        assert page.locator(".brand-mark").is_visible(), "Brand mark not visible"
        assert page.locator(".brand h1").is_visible(), "Brand heading not visible"
        assert page.locator(".security-note").is_visible(), "Security note not visible"

        # Check country dropdown has options
        country_options = page.locator("#country option").count()
        print(f"Country options found: {country_options}")
        assert country_options > 10, f"Expected multiple countries, found {country_options}"

        # Check for loading spinner (hidden by default)
        spinner = page.locator(".spinner")
        assert not spinner.is_visible(), "Spinner should be hidden initially"

        # Check error toast is hidden initially
        error_toast = page.locator(".error-toast")
        assert not error_toast.is_visible(), "Error toast should be hidden initially"

        print("\n✓ All modernized UI tests passed!")

        browser.close()


if __name__ == "__main__":
    test_modernized_login_page()
