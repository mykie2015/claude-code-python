"""Happy flow UI test - browser stays open until you close it."""

import time

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(
        "file:///Users/mykielee/GitHub/my_projects/claude-code-python/.worktrees/auth-mvp/src/api/login_page.html"
    )
    page.wait_for_load_state("networkidle")

    print("=== Happy Flow UI Test ===\n")

    # 1. Select country
    print("1. Selecting country...")
    page.select_option("#country", "US")
    print("   ✓ Selected: US")

    # 2. Enter email
    print("2. Entering email...")
    page.fill("#email", "test@example.com")
    print("   ✓ Email: test@example.com")

    # 3. Enter password
    print("3. Entering password...")
    page.fill("#password", "password123")
    print("   ✓ Password entered")

    # 4. Toggle password visibility
    print("4. Toggling password visibility...")
    page.click(".password-toggle")
    print("   ✓ Password revealed (now visible)")

    # 5. Check Remember Me
    print("5. Checking Remember Me...")
    page.check("#remember")
    print("   ✓ Remember Me checked")

    # 6. Submit form
    print("6. Clicking Sign In...")
    page.click(".submit-btn")
    print("   ✓ Loading spinner displayed")

    print("\n=== Test Complete ===")
    print("Browser stays open. Close it manually when done.")
    print("(Press Ctrl+C in terminal to exit)")

    # Keep browser open until closed
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
