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
        # Click on 'Sign In' to start login process.
        frame = context.pages[-1]
        elem = frame.locator('xpath=html/body/div/header/nav/div[2]/a[4]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # Click the 'Sign in' button to log in.
        frame = context.pages[-1]
        elem = frame.locator('xpath=html/body/div/div/form/div[2]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # Click the 'Route Explorer' button to navigate to the Route Explorer page.
        frame = context.pages[-1]
        elem = frame.locator('xpath=html/body/div/header/div/div/div[2]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # Click each tool to verify that sample responses are displayed for example inputs, one by one.
        frame = context.pages[-1]
        elem = frame.locator('xpath=html/body/div/main/div[2]/div/div').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # Click on 'get_article' tool to verify its input parameters and sample response.
        frame = context.pages[-1]
        elem = frame.locator('xpath=html/body/div/main/div[2]/div/div[2]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # Click on 'get_facts_about' tool to verify its input parameters and sample response.
        frame = context.pages[-1]
        elem = frame.locator('xpath=html/body/div/main/div[2]/div/div[3]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # Click on 'get_latest_news' tool to verify its input parameters and sample response.
        frame = context.pages[-1]
        elem = frame.locator('xpath=html/body/div/main/div[2]/div/div[4]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # Assert that all four MCP tools are listed on the Route Explorer page.
        tools = ['search_articles', 'get_article', 'get_facts_about', 'get_latest_news']
        for tool in tools:
            tool_locator = frame.locator(f'text={tool}')
            assert await tool_locator.count() > 0, f"Tool '{tool}' not found on the page."
          
        # Assert that each tool shows required input parameters.
        tool_params = {
            'search_articles': ['query', 'date_range', 'limit'],
            'get_article': ['article_id'],
            'get_facts_about': ['entity', 'fact_type'],
            'get_latest_news': ['topic', 'count']
        }
        for tool, params in tool_params.items():
            # Locate the tool section by tool name
            tool_section = frame.locator(f'text={tool}').first
            for param in params:
                param_locator = tool_section.locator(f'text={param}')
                assert await param_locator.count() > 0, f"Parameter '{param}' not found for tool '{tool}'."
          
        # Assert that sample responses are displayed for example inputs for 'get_latest_news' tool.
        get_latest_news_section = frame.locator('text=get_latest_news').first
        example_response_locator = get_latest_news_section.locator('text=New Smartphone Released')
        assert await example_response_locator.count() > 0, "Sample response for 'get_latest_news' not found."
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    