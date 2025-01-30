import requests
from bs4 import BeautifulSoup
import openai
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def scrape_website(url):
    """Scrape the fully rendered text content from the given URL using Selenium."""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    text = driver.find_element(
        "tag name", "body"
    ).text  # Extract all visible text from the page
    driver.quit()
    return text


def summarize_topics_with_openai(text):
    """Summarize the main topics using OpenAI API."""
    client = openai.OpenAI()

    confirm = input("Do you want to summarize the scraped content? (yes/no): ")
    if confirm.lower() != "yes":
        print("Summary request canceled.")
        return None

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Summarize the content of the website.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # Select a website to scrape
    # url = "https://tuitter.it" # This one has caCAPTCHA
    url = "https://www.theblogstarter.com"  # This one doesn't have caCAPTCHA
    scraped_text = scrape_website(url)

    if scraped_text:
        # print("Scraped Content:\n")
        # print(scraped_text[:1000])  # Print first 1000 characters for preview
        # print("\n" + "-" * 80 + "\n")

        topics_summary = summarize_topics_with_openai(scraped_text)
        if topics_summary:
            print("Main Topics:", topics_summary)
