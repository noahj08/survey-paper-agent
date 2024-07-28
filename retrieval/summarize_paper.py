import requests
import PyPDF2
import openai
import pandas as pd
from together import Together
import re
from prompts import TopicPrompts
import pandas as pd


client = OpenAI()


def download_arxiv_pdf(arxiv_id, save_path):
    url = f'https://arxiv.org/pdf/{arxiv_id}.pdf'
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


def generate_topics(text, api_key, num_topics=5):
    openai.api_key = api_key
    prompt = TopicPrompts.generate_topics_prompt(text, num_topics)
    response = chatbot.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[{"role": "user", "content": prompt}]
        )
    topics = response.choices[0].message.content.strip()
    return topics


def summarize_text(text, api_key, topic, max_length=500):
    openai.api_key = api_key
    prompt = TopicPrompts.summarize_text_prompt(text, topic, max_length)
    response = chatbot.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[{"role": "user", "content": prompt}]
        )
    summary = response.choices[0].message.content.strip()
    return summary


def summarize_section(text, api_key, section, max_length=500):
    openai.api_key = api_key
    prompt = TopicPrompts.summarize_section_prompt(text, section)
    response = chatbot.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[{"role": "user", "content": prompt}]
        )
    summary = response.choices[0].message.content.strip()
    return summary


def get_topics_df(save_path, api_key, num_topics=5):
    text = extract_text_from_pdf(save_path)
    topics = generate_topics(text, api_key, num_topics)
    topics_list = [line.split('. ', 1)[1] for line in topics.split('\n') if line.strip()]
    summaries = [summarize_text(text, api_key, topic) for topic in topics_list]
    df = pd.DataFrame({"Topic": topics_list, "Summary": summaries})
    return df


def get_sections_df(pdf_path, api_key):
    sections = ["Abstract", "Introduction and Contributions", "Related Work", "Method and Experiments", "Results", "Future Work"]
    text = extract_text_from_pdf(pdf_path)
    summaries = [summarize_section(text, api_key, section, 250) for section in sections]
    sections_dict = {section: summary for section, summary in zip(sections, summaries)}
    df = pd.DataFrame(sections_dict, index=[0])
    return df


if __name__ == "__main__":
    save_path = "downloaded_paper.pdf"
    api_key = "your_api_key_here"
    get_topics_df(save_path, api_key, 5)
