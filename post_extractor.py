import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import os

output_dir = 'forum_content'

async def extract_text(url):
    # 1. Define a simple extraction schema
    css_selector = "div.bbWrapper"

    base_selector = "div.message-inner"  # Adjust this based on the forum's structure

    # Define the schema for the JSON output
    schema = {
        "baseSelector": base_selector,  # Root element for extraction
        "fields": [
            {
                "name": "post",  # Name of the field
                "selector": "div.bbWrapper",  # CSS selector for the post content
                "type": "text"
            },
            {
                "name": "timestamp",  # Name of the field
                "selector": "time.u-dt",  # CSS selector for the timestamp
                "type": "text"
            }
        ]
    }

    # 2. Create the extraction strategy
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    # 3. Set up your crawler config (if needed)
    config = CrawlerRunConfig(
        # e.g., pass js_code or wait_for if the page is dynamic
        # wait_for="css:.crypto-row:nth-child(20)"
        cache_mode = CacheMode.BYPASS,
        extraction_strategy=extraction_strategy,
    )

    async with AsyncWebCrawler(verbose=True) as crawler:
        # 4. Run the crawl and extraction
        result = await crawler.arun(
            url=url,
            config=config
        )

        if not result.success:
            print("Crawl failed:", result.error_message)
            return
        
        # 5. Parse the extracted JSON
        data = json.loads(result.extracted_content)
        filename = url.replace('/', '_') + '.json'
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            print(f"Extracted {len(data)} post entries from {filepath}")
            json.dump(data, f)
