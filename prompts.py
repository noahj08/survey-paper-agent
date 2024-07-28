class ArxivQueryPrompts:
    @staticmethod
    def generate_arxiv_queries_prompt(initial_query, num_queries, context_str):
        return (
            f"You are part of a system tasked to generate search queries on the ArXiv search engine in order to build "
            f"a repository of papers for use in a survey paper about {initial_query}. Generate {num_queries} unique "
            f"and relevant search queries for arXiv based on the initial query '{initial_query}'{context_str}. "
            f"Provide the queries in a comma-separated format without any additional text. EXAMPLE: initial_query: "
            f"Retrieval augmented generation, RESPONSE: 'RAG', 'RAG LLM', 'Retrieval-Augmented LLM', 'Retrieval'"
        )


class TopicPrompts:
    @staticmethod
    def generate_topics_prompt(text, num_topics):
        return f"Identify {num_topics} key topics from the following text and only return the topic name:\n{text[:1000]}"

    @staticmethod
    def summarize_text_prompt(text, topic, max_length):
        return f"Summarize the following text focusing on the topic '{topic}' and don't start with the topic name:\n{text[:8000]}"

    @staticmethod
    def summarize_section_prompt(text, section):
        return f"Summarize the following text focusing on the section '{section}' and start directly with the summary:\n{text}"


class SubtopicPrompts:
    @staticmethod
    def get_subtopic_generation_prompt(topic, description, context):
        if description is not None:
            return (
                "You will be given a research area and a brief overview of this area. You will output a JSON dictionary "
                "with two columns, 'Subtopic' and 'Subtopic Description'. In these fields, describe all academic areas "
                "which are sub-topics of the original topic. Make sure that your list of subtopics makes sense as a set "
                "of distinct and comprehensive sub-topics that somebody trying to learn about the original topic would "
                "need to know in order to fully understand the space. Here is an example of what you should do: INPUTS: "
                "RESEARCH_AREA: 'Retrieval Augmented Generation', DESCRIPTION: 'Retrieval augmented generation is a "
                "research topic at the intersection of natural language processing and artificial intelligence, focusing "
                "on enhancing text generation models by incorporating information retrieved from external sources. This "
                "approach aims to improve the relevance, coherence, and factual accuracy of generated text by leveraging "
                "relevant data or knowledge retrieved from large-scale repositories like databases, documents, or the web. "
                "By integrating retrieval mechanisms into generative models, researchers seek to create more contextually "
                "aware and informative outputs, addressing challenges such as content fidelity and diversity in automated "
                "content generation tasks. This paradigm holds promise for applications in automated summarization, question "
                "answering, and personalized content creation across various domains.' YOUR RESPONSE: { 'subtopic_name': "
                "['Information Retrieval Techniques', 'Content Selection and Fusion', 'Evaluation Metrics', 'Domain-Specific "
                "Applications'], 'subtopic_description': ['Methods for effectively retrieving relevant information from "
                "large-scale datasets, including keyword-based search, semantic search, and document retrieval.', 'Strategies "
                "for selecting and fusing retrieved content into generated outputs while maintaining coherence, relevance, and "
                "factual accuracy.', 'Development of metrics and benchmarks to assess the performance of RAG models in terms "
                "of informativeness, diversity, and alignment with retrieved information.', 'Exploration of RAG techniques in "
                "specific applications such as medical text generation, legal document summarization, and personalized content "
                "creation in e-commerce, adapting methodologies to suit different domains' requirements and challenges.']} "
                "Now, your turn. INPUTS: RESEARCH_AREA: " + f'{topic}' + " DESCRIPTION: " + f'{description}' + " Context: " + f'{context}' + " YOUR RESPONSE: {"
            )
        else:
            return (
                "You will be given a research area; you are trying to write an outline for a survey paper about that area. "
                "You will output a JSON dictionary with two columns, 'Subtopic' and 'Subtopic Description'. In these fields, "
                "describe all academic areas which are sub-topics of the original topic. Here is an example of what you should do: "
                "INPUTS: RESEARCH_AREA: 'Retrieval Augmented Generation', DESCRIPTION: 'Retrieval augmented generation is a "
                "research topic at the intersection of natural language processing and artificial intelligence, focusing on "
                "enhancing text generation models by incorporating information retrieved from external sources. This approach "
                "aims to improve the relevance, coherence, and factual accuracy of generated text by leveraging relevant data or "
                "knowledge retrieved from large-scale repositories like databases, documents, or the web. By integrating retrieval "
                "mechanisms into generative models, researchers seek to create more contextually aware and informative outputs, "
                "addressing challenges such as content fidelity and diversity in automated content generation tasks. This paradigm "
                "holds promise for applications in automated summarization, question answering, and personalized content creation "
                "across various domains.' YOUR RESPONSE: { 'subtopic_name': ['Information Retrieval Techniques', 'Content Selection "
                "and Fusion', 'Evaluation Metrics', 'Domain-Specific Applications'], 'subtopic_description': ['Methods for effectively "
                "retrieving relevant information from large-scale datasets, including keyword-based search, semantic search, and document "
                "retrieval.', 'Strategies for selecting and fusing retrieved content into generated outputs while maintaining coherence, "
                "relevance, and factual accuracy.', 'Development of metrics and benchmarks to assess the performance of RAG models in terms "
                "of informativeness, diversity, and alignment with retrieved information.', 'Exploration of RAG techniques in specific "
                "applications such as medical text generation, legal document summarization, and personalized content creation in e-commerce, "
                "adapting methodologies to suit different domains' requirements and challenges.']} Now, your turn. INPUTS: RESEARCH_AREA: " + f'{topic}' + " DESCRIPTION: " + f'{description}' + " Context: " + f'{context}' + " YOUR RESPONSE: {"
            )
main.py

python
Copy code
import os
import argparse
import requests
import re
import csv
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from together import Together
from prompts import ArxivQueryPrompts, TopicPrompts, SubtopicPrompts


def generate_arxiv_queries(initial_query: str, api_key: str, context: str = "", num_queries=1) -> list:
    client = Together(api_key=api_key)
    context_str = f" considering the following context: {context}" if context else ""
    prompt = ArxivQueryPrompts.generate_arxiv_queries_prompt(initial_query, num_queries, context_str)
    response = client.chat.completions.create(model="meta-llama/Llama-3-8b-chat-hf", messages=[{"role": "user", "content": prompt}])
    response_content = response.choices[0].message.content
    generated_queries = [query.strip() for query in response_content.split(",")]
    return generated_queries


def arxiv_query(search_query, context):
    download_papers_for_query(search_query, context)


def download_papers_for_query(initial_query: str, context: str, num_queries=5, max_results=2):
    generated_queries = generate_arxiv_queries(initial_query, api_key, context, num_queries=num_queries)
    for query in generated_queries:
        try:
            download_arxiv_papers(search_query=f"all:{query}", max_results=max_results)
        except Exception as e:
            print(f"Error occurred: {e}")


def download_arxiv_papers(search_query: str, start: int = 0, max_results: int = 10, pdf_dir: str = "arxiv_pdfs", summary_dir: str = "arxiv_summaries", citation_dir: str = "arxiv_citations", csv_file: str = "arxiv_papers.csv"):
    url = f"http://export.arxiv.org/api/query?search_query={search_query}&start={start}&max_results={max_results}"
    response = requests.get(url)
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(summary_dir, exist_ok=True)
    os.makedirs(citation_dir, exist_ok=True)

    def create_valid_filename(title: str) -> str:
        return re.sub(r'[\\/*?:"<>|]', "", title)

    def fetch_citation(arxiv_id: str) -> str:
        citation_url = f"https://arxiv.org/abs/{arxiv_id}"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(citation_url)
        try:
            export_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "bib-cite-trigger")))
            export_button.click()
            citation_textarea = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "bib-cite-target")))
            citation = citation_textarea.get_attribute("value")
        except Exception as e:
            print(f"Error fetching citation for {arxiv_id}: {e}")
            citation = ""
        finally:
            driver.quit()
        return citation

    def save_metadata_to_csv(metadata: list, csv_file: str):
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


def main():
    parser = argparse.ArgumentParser(description="Search arXiv and download papers based on search queries and context.")
    parser.add_argument("--search-query", required=True, help="The initial search query for arXiv.")
    parser.add_argument("--context", default="", help="Additional context to refine the search queries.")
    args = parser.parse_args()
    download_papers_for_query(args.search_query, args.context)


if __name__ == "__main__":
    main()
get_pdf_topics.py

