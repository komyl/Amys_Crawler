import requests
from bs4 import BeautifulSoup
import time
import re
from collections import defaultdict
import random


# Welcome message
def print_welcome_message():
 welcome_message = """
    🌐✨ Hello and Welcome to Amy's Crawler! ✨🌐
    This crawler will search Wikipedia, arXiv, Google Scholar, and PubMed for a specified keyword.
    It will index the content of pages and search through them efficiently. 🚀
    """
 print(welcome_message)


# Error handling with retry for 404, 429 and other HTTP errors
def handle_http_errors(status_code, source, retries=1):
 if status_code == 403:
  return f"🚫 Access to {source} is restricted (403 Forbidden)."
 elif status_code == 404 and retries > 0:
  print(f"🔄 Retrying {source} due to 404 error...")
  time.sleep(2)
  return None  # No error if retrying
 elif status_code == 404:
  return f"❌ The page on {source} was not found (404 Not Found)."
 elif status_code == 429 and retries > 0:  # Handling rate limiting (429 Too Many Requests)
  wait_time = random.uniform(10, 20)  # Random delay between 10 and 20 seconds
  print(f"⚠️ Rate limiting detected (429) for {source}. Retrying in {wait_time:.2f} seconds...")
  time.sleep(wait_time)  # Sleep for the calculated delay
  return None  # Retry
 elif status_code == 500:
  return f"⚠️ {source} is experiencing internal issues (500 Server Error)."
 elif status_code == 503:
  return f"🔧 {source} is temporarily unavailable (503 Service Unavailable)."
 else:
  return f"⚠️ An error occurred while accessing {source} (Status Code: {status_code})."


# Function to perform keyword search and link extraction on specific websites
def crawl_and_index(keyword, max_depth=1, max_links_per_site=20):
 base_urls = {
  "Wikipedia": "https://en.wikipedia.org/w/index.php?search=",
  "arXiv": "https://arxiv.org/search/?query=",
  "Google Scholar": "https://scholar.google.com/scholar?hl=en&q=",
  "PubMed": "https://pubmed.ncbi.nlm.nih.gov/?term=",
 }

 visited_links = set()  # To avoid revisiting links
 keyword_occurrences = []  # To store found keyword occurrences
 related_links = {}  # Dictionary to store related links and keyword context
 index = defaultdict(list)  # Index to store words and their occurrences (word -> [page URLs])

 def recursive_crawl(current_url, keyword, depth, retries=1):
  if depth > max_depth or current_url in visited_links:
   return
  visited_links.add(current_url)

  print(f"🔍 Crawling URL: {current_url}")  # Debug output

  try:
   response = requests.get(current_url, timeout=10)

   # Retry handling for 404 and 429 errors
   if response.status_code == 404 and retries > 0:
    error_message = handle_http_errors(response.status_code, current_url, retries=retries)
    if error_message:
     print(error_message)
     return
    return recursive_crawl(current_url, keyword, depth, retries - 1)
   elif response.status_code == 429 and retries > 0:  # 429 Too Many Requests Handling
    error_message = handle_http_errors(response.status_code, current_url, retries=retries)
    if error_message:
     print(error_message)
     return
    return recursive_crawl(current_url, keyword, depth, retries - 1)

   if response.status_code == 200:
    print(f"✅ Successfully fetched: {current_url}")  # Debug output
    soup = BeautifulSoup(response.content, 'html.parser')
    page_text = soup.get_text()
    title = soup.find('title').text.strip() if soup.find('title') else "No Title"
    keyword_count = page_text.lower().count(keyword.lower())

    # Indexing content for later search
    words = re.findall(r'\w+', page_text.lower())  # Tokenizing the text
    for word in set(words):  # Avoid duplicates in the same page
     index[word].append(current_url)

    if keyword_count > 0:
     keyword_occurrences.append({
      'url': current_url,
      'title': title,
      'keyword_count': keyword_count
     })

    # Stop further crawling if we've already crawled this site
    if current_url not in related_links:
     related_links[current_url] = []

    # Finding related links containing the keyword, limited to max_links_per_site
    for link in soup.find_all('a', href=True):
     if len(related_links[current_url]) >= max_links_per_site:
      break
     href = link['href']
     full_link = href if href.startswith('http') else re.sub(r'/$', '', current_url) + '/' + href.lstrip('/')

     if keyword.lower() in link.text.lower():
      related_links[current_url].append({
       'url': full_link,
       'title': link.text.strip()
      })

    # Do not follow any further links after processing one page
    return

   else:
    print(handle_http_errors(response.status_code, current_url, retries=retries))
  except requests.exceptions.RequestException as e:
   print(f"❌ Request failed for {current_url}: {e}")
   time.sleep(random.uniform(1, 3))  # Random sleep time between 1 and 3 seconds if request fails

 # Start crawling from each base URL
 for site, url_prefix in base_urls.items():
  if site == "arXiv":
   search_url = f"{url_prefix}{keyword.replace(' ', '+')}&searchtype=all&abstracts=show&order=-announced_date_first&size=50"
  elif site == "Wikipedia":
   search_url = f"{url_prefix}{keyword.replace(' ', '%2Fwiki%2F')}"
  else:
   search_url = f"{url_prefix}{keyword.replace(' ', '+')}"

  print(f"🚀 Starting crawl on {site} with URL: {search_url}")
  recursive_crawl(search_url, keyword, 0)

 return keyword_occurrences, related_links, index


# Function to search through the index
def search_index(keyword, index):
 print(f"\n🔍 Searching for '{keyword}' in the index...\n")

 if keyword.lower() in index:
  results = index[keyword.lower()]
  print(f"🔑 Found the keyword in {len(results)} pages:")
  for result in results:
   print(f"  - 🗂️ {result}")
 else:
  print(f"❌ No results found for the keyword '{keyword}' in the index.")


# Main function to handle the full process
def main():
 print_welcome_message()
 keyword = input("🔍 Enter the keyword to search for: ").strip()

 keyword_occurrences, related_links, index = crawl_and_index(keyword)

 print("\n--- 📝 Crawler Results ---")

 print("\n🔍 **Keyword Occurrences**:")
 for entry in keyword_occurrences:
  print(f"🗂️ **URL**: {entry['url']}\n📋 **Title**: {entry['title']}\n🔑 **Keyword Count**: {entry['keyword_count']}\n")

 print("\n🔗 **Related Links (Keyword in Link Text, up to 20 per site)**:")
 for page, links in related_links.items():
  print(f"\n📄 **Page**: {page}")
  for link in links:
   print(f"  - 📝 **Title**: {link['title']}\n    🔗 **Link**: {link['url']}")

 # Search the index after crawling
 search_index(keyword, index)


if __name__ == "__main__":
 main()

