import requests
import xml.etree.ElementTree as ET
import os
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_arxiv_papers(search_query: str, start: int = 0, max_results: int = 10, pdf_dir: str = "arxiv_pdfs", summary_dir: str = "arxiv_summaries", citation_dir: str = "arxiv_citations", csv_file: str = "arxiv_papers.csv"):
    """
    Download PDFs, summaries, and citations of papers from arXiv based on the search query, and save the metadata in a CSV file.
    
    Args:
        search_query (str): The search query to use for fetching papers from arXiv.
        start (int): The starting index for fetching results.
        max_results (int): The maximum number of results to fetch.
        pdf_dir (str): The directory to save the downloaded PDFs.
        summary_dir (str): The directory to save the summaries of the papers.
        citation_dir (str): The directory to save the BibTeX citations of the papers.
        csv_file (str): The CSV file to save the metadata of the papers.
    """
    url = f"http://export.arxiv.org/api/query?search_query={search_query}&start={start}&max_results={max_results}"

    response = requests.get(url)

    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(summary_dir, exist_ok=True)
    os.makedirs(citation_dir, exist_ok=True)

    def create_valid_filename(title: str) -> str:
        """Replace special characters in filename to make it valid."""
        return re.sub(r'[\\/*?:"<>|]', "", title)

    def fetch_citation(arxiv_id: str) -> str:
        """Fetch the BibTeX citation for a given arXiv ID using Selenium."""
        citation_url = f"https://arxiv.org/abs/{arxiv_id}"
        
        # Set up Chrome options for headless mode
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(citation_url)

        try:
            export_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "bib-cite-trigger"))
            )
            export_button.click()

            citation_textarea = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "bib-cite-target"))
            )
            citation = citation_textarea.get_attribute("value")
        except Exception as e:
            print(f"Error fetching citation for {arxiv_id}: {e}")
            citation = ""
        finally:
            driver.quit()

        return citation

    def save_metadata_to_csv(metadata: list, csv_file: str):
        """Save metadata to a CSV file."""
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Title", "Link", "Summary File", "PDF File", "Citation File"])
            writer.writerow(metadata)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()
            link = entry.find("{http://www.w3.org/2005/Atom}id").text.strip()
            arxiv_id = link.split('/')[-1]

            valid_title = create_valid_filename(title)
            pdf_filename = os.path.join(pdf_dir, f"{valid_title}.pdf")
            summary_filename = os.path.join(summary_dir, f"{valid_title}.txt")
            citation_filename = os.path.join(citation_dir, f"{valid_title}.bib")

            pdf_link = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

            pdf_response = requests.get(pdf_link)
            if pdf_response.status_code == 200:
                with open(pdf_filename, "wb") as pdf_file:
                    pdf_file.write(pdf_response.content)

            with open(summary_filename, "w") as summary_file:
                summary_file.write(summary)

            citation = fetch_citation(arxiv_id)
            if citation:
                with open(citation_filename, "w") as citation_file:
                    citation_file.write(citation)

            metadata = [title, link, summary_filename, pdf_filename, citation_filename]
            save_metadata_to_csv(metadata, csv_file)

if __name__ == "__main__":
    download_arxiv_papers("all:Interpretability in Machine Learning")
