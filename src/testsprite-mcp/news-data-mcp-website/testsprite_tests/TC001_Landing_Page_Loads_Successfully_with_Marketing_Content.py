import asyncio
from playwright import async_api

async def run_test():
    pw = None
    browser = None
    context = None
    
    try:
        # Start a Playwright session in asynchronous mode
        pw = await async_api.async_playwright().start()
        
        # Launch a Chromium browser in headless mode with custom arguments
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--window-size=1280,720",         # Set the browser window size
                "--disable-dev-shm-usage",        # Avoid using /dev/shm which can cause issues in containers
                "--ipc=host",                     # Use host-level IPC for better stability
                "--single-process"                # Run the browser in a single process mode
            ],
        )
        
        # Create a new browser context (like an incognito window)
        context = await browser.new_context()
        context.set_default_timeout(5000)
        
        # Open a new page in the browser context
        page = await context.new_page()
        
        # Navigate to your target URL and wait until the network request is committed
        await page.goto("http://localhost:3000", wait_until="commit", timeout=10000)
        
        # Wait for the main page to reach DOMContentLoaded state (optional for stability)
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=3000)
        except async_api.Error:
            pass
        
        # Iterate through all iframes and wait for them to load as well
        for frame in page.frames:
            try:
                await frame.wait_for_load_state("domcontentloaded", timeout=3000)
            except async_api.Error:
                pass
        
        # Interact with the page elements to simulate user flow
        # Verify features grid displays all key features described.
        await page.mouse.wheel(0, window.innerHeight)
        

        # Confirm that call-to-action buttons are present and clickable.
        frame = context.pages[-1]
        elem = frame.locator('xpath=html/body/div/section[2]/div/div[2]/div/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # Check that hero section with product pitch is visible.
        hero_section = page.locator('section.hero')
        assert await hero_section.is_visible()
        pitch_text = await hero_section.text_content()
        assert 'News Data MCP' in pitch_text and 'AI-Powered News' in pitch_text
          
        # Verify features grid displays all key features described
        features = ['Real-time News', 'Structured Data', 'MCP Protocol']
        for feature in features:
            feature_locator = page.locator(f'text={feature}')
            assert await feature_locator.is_visible()
          
        # Ensure 3-tier pricing plans are shown with appropriate details
        pricing_tiers = ['Free', 'Monthly', 'Yearly']
        for tier in pricing_tiers:
            tier_section = page.locator(f'text={tier}')
            assert await tier_section.is_visible()
            price_locator = page.locator(f'text={tier}').locator('xpath=..').locator('text=/\$\d+/')
            assert await price_locator.is_visible()
            # Check action button text
            action_text = ''
            if tier == 'Free':
                action_text = 'Get Started'
            elif tier == 'Monthly':
                action_text = 'Start Monthly Plan'
            elif tier == 'Yearly':
                action_text = 'Start Yearly Plan'
            action_button = page.locator(f'text={action_text}')
            assert await action_button.is_visible()
          
        # Confirm that call-to-action buttons are present and clickable
        cta_buttons = page.locator('a, button').filter({ 'hasText': /Get Started|Start Monthly Plan|Start Yearly Plan/ })
        count = await cta_buttons.count()
        assert count >= 3
        for i in range(count):
            button = cta_buttons.nth(i)
            assert await button.is_enabled()
            # Optionally, test clicking without navigation
            # await button.click()
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    