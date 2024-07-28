import requests
import PyPDF2
import openai
from openai import OpenAI
import pandas as pd
from together import Together
import re



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
    # client = Together(api_key=api_key)
    prompt = f"Identify {num_topics} key topics from the following text and only return the topic name:\n{text[:1000]}"  # Limit the input length

    response = client.chat.completions.create(
    model="gpt-4o",
        # model="meta-llama/Llama-3-8b-chat-hf",

        messages=[{"role": "user", "content": prompt}],

        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7)

    topics = response.choices[0].message.content.strip()
    return topics

def summarize_text(text, api_key, topic,max_length=500):
    openai.api_key = api_key
    # client = Together(api_key=api_key)
    prompt = f"Summarize the following text focusing on the topic '{topic}' and don't start with the topic name:\n{text[:8000]}"  # Limit the input length

    response = client.chat.completions.create(
    model="gpt-4o",
    # model="meta-llama/Llama-3-8b-chat-hf",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_length,
        n=1,
        stop=None,
        temperature=0.7
    )

    summary = response.choices[0].message.content.strip()
    return summary

def summarize_section(text, api_key, section, max_length=500):
    openai.api_key = api_key
    # client = Together(api_key=api_key)
    prompt = f"Summarize the following text focusing on the section '{section}' and start directly with the summary:\n{text}"  # Limit the input length

    response = client.chat.completions.create(
    model="gpt-4o",
        # model="meta-llama/Llama-3-8b-chat-hf",

        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_length,
        n=1,
        stop=None,
        temperature=0.7
    )

    summary = response.choices[0].message.content.strip()
    return summary

def get_topics_df(save_path, api_key, num_topics=5):

    text = extract_text_from_pdf(save_path)
    topics = generate_topics(text, api_key, num_topics)
    # print(topics)
    topics_list = [line.split('. ', 1)[1] for line in topics.split('\n') if line.strip()]
    # topic_pattern = re.compile(r'\d+\.\s+(.+)')
    # topics_list = topic_pattern.findall(topics)

    summaries = [summarize_text(text, api_key, topic) for topic in topics_list]


    df = pd.DataFrame({
        # "Name": "RAG",
        "Topic": topics_list,
        "Summary": summaries,
        # "Citation":"arxiv_something"
    })

    # print(df)
    # df.to_csv("topics_and_summaries.csv", index=False)
    return df


def get_sections_df(pdf_path, api_key):

    sections = ["Abstract","Introduction and Contributions", "Related Work", "Method and Experiments","Results", "Future Work"]
    # sections = ["Abstract","Introduction and Contributions"]

    text = extract_text_from_pdf(pdf_path)
    summaries = [summarize_section(text, api_key, section, 250) for section in sections]
    sections_dict = {}
    for section, summary in zip(sections, summaries):
        sections_dict[section] = summary

    # print(sections_dict)
    df = pd.DataFrame(sections_dict, index=[0])
    return df


if __name__ == "__main__":
    save_path = "downloaded_paper.pdf"
    get_topics_df(save_path, api_key, 5)
