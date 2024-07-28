import requests
import PyPDF2
import openai
import pandas as pd
from together import Together
import re
from prompts import TopicPrompts
import pandas as pd
from get_pdf_topics.read_pdf import get_topics_df, summarize_paper
from arxiv_scraper.search_arxiv import download_papers_for_query
import os
import shutil
import time


client = OpenAI()
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def summarize_paper_section(text, api_key, section_name, max_length=500):
    openai.api_key = api_key
    prompt = TopicPrompts.summarize_section_prompt(text, section_name)
    response = chatbot.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[{"role": "user", "content": prompt}]
        )
    summary = response.choices[0].message.content.strip()
    return summary

def summarize_paper(pdf_path, api_key):
    sections = ["Abstract", "Introduction and Contributions", "Related Work", "Method and Experiments", "Results", "Future Work"]
    text = extract_text_from_pdf(pdf_path)
    summaries = [summarize_section(text, api_key, section, 250) for section in sections]
    sections_dict = {section: summary for section, summary in zip(sections, summaries)}
    df = pd.DataFrame(sections_dict, index=[0])
    return df


def summarize_all_papers(folder_arxiv_pdfs, folder_arxiv_cits, api_key, initial_query, num_queries=5, max_results=5,context=""):
    download_papers_for_query(initial_query=initial_query, context=context, num_queries=num_queries, max_results=max_results)

    # Generate a list of all filenames in the folder
    file_list = os.listdir(folder_arxiv_pdfs)

    print("Summarizing all papers.")

    paper_df_sections_list = []
    for file in file_list:
        paper_df = summarize_paper(f"{folder_arxiv_pdfs}/{file}", api_key)
        paper_df['Name']=file[:-4]
        try:
            with open(f"{folder_arxiv_cits}/{file[:-4]}.bib", "r") as txt_file:
                txt_contents = txt_file.read()
                paper_df['Citation'] = txt_contents
        except:
            paper_df['Citation'] = "No citation available"

        paper_df_sections_list.append(paper_df)
    paper_summaries_df = pd.concat(paper_df_sections_list)
    
    return paper_topics_concat.reset_index(drop=True), paper_sections_df.reset_index(drop=True)


if __name__ == "__main__":
    # save_path = "downloaded_paper.pdf"
    folder_arxiv_pdfs = "arxiv_pdfs"
    folder_arxiv_cits = "arxiv_citations"

    # Delete all files in folders
    shutil.rmtree(folder_arxiv_pdfs)
    os.mkdir(folder_arxiv_pdfs)
    shutil.rmtree(folder_arxiv_cits)
    os.mkdir(folder_arxiv_cits)
    # Delay for 1 second to ensure folders are deleted
    time.sleep(1)

    papers, summaries = summarize_all_papers(folder_arxiv_pdfs, folder_arxiv_cits, api_key, initial_query, 5, 5)
    papers.to_csv("papers_df.csv", index=False)
    summaries.to_csv("sections_df.csv", index=False)
