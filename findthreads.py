import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from post_extractor import extract_text
import asyncio


base_url = "https://forum.ih8mud.com/forums/40-55-series-tech.8/"
ignores = ["who-replied", "latest"]

def load_visited_threads(filename='visited_threads.txt'):
    """Load visited threads from a file into a set."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return set(line.strip() for line in f)
    return set()  # Return an empty set if the file does not exist

def save_visited_threads(filename='visited_threads.txt'):
    with open(filename, 'w') as f:
        for thread in visited_threads:
            f.write(f"{thread}\n")
    print(f"Visited threads saved to {filename}")

# Load visited threads from the file
visited_threads = load_visited_threads()

def get_page_urls(page_url):
    response = requests.get(page_url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all thread links on the page
    body_content = soup.select_one('.p-body-content')
    thread_links = body_content.select('a[href*="/threads/"]')
    next_main_link = soup.select_one('a.pageNav-jump--next')
   
    for link in thread_links:
        if link['href'].__contains__("what-have-you-done-to-your-land-cruiser-this-week"):
            continue
        thread_url = urljoin(base_url, link['href'])
        if thread_url not in visited_threads and not (thread_url.endswith("who-replied/") or thread_url.endswith("latest") or thread_url.__contains__("page")):
            visited_threads.add(thread_url)
            print(f"Visiting thread: {thread_url}")
            response = requests.get(thread_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            next_page_link = soup.select_one('a.pageNav-jump--next')
            asyncio.run(extract_text(thread_url))
            
            while next_page_link:
                next_page_url = urljoin(base_url, next_page_link['href'])
                print(f"Thread has next page: {next_page_url}")
                visited_threads.add(next_page_url)
                response = requests.get(next_page_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                next_page_link = soup.select_one('a.pageNav-jump--next')
                asyncio.run(extract_text(next_page_url))
                if len(visited_threads) % 100 == 0:  # Save every 250 threads visited
                    save_visited_threads()

            # Save visited threads periodically
            if len(visited_threads) % 100 == 0:  # Save every 250 threads visited
                save_visited_threads()

    # Find the next page link
    if next_main_link:
        next_main_link = urljoin(base_url, next_main_link['href'])
        print(f"Moving to next page: {next_main_link}")
        get_page_urls(next_main_link)

# Start scraping from the first page
if __name__ == "__main__":
    attempts = 0
    while attempts < 10:
        try:
            get_page_urls(base_url)
            # Save any remaining visited threads when done
            save_visited_threads()
            break   
        except Exception as e:
            print(f"Error: {e}")
            attempts += 1
            time.sleep(180)