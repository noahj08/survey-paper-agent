import argparse
import os
import shutil
import time
from together import Together

from retrieval.summarizer.summarize_papers import summarize_all_papers
from outlining.get_subtopics import get_subtopics, get_concept_hierarchy

def setup_dirs():
    shutil.rmtree(folder_arxiv_pdfs)
    os.mkdir(folder_arxiv_pdfs)
    shutil.rmtree(folder_arxiv_cits)
    os.mkdir(folder_arxiv_cits)
    time.sleep(1)

def get_initial_context(topic, summaries, relevant_only=False, threshold=0.7):
    """
    Get the initial context from summaries. If relevant_only is True, only get semantically similar chunks to the topic.

    Args:
        topic (str): The topic to compare against the summaries.
        summaries (pd.DataFrame): DataFrame containing the summaries.
        relevant_only (bool): Flag to filter summaries by semantic similarity.
        threshold (float): Cosine similarity threshold to consider a chunk as similar.

    Returns:
        str: Concatenated string of (optionally filtered) summaries.
    """
    if not relevant_only:
        return summaries.to_string()

    topic_embedding = model.encode(topic, convert_to_tensor=True)
    similar_chunks = []

    for index, row in summaries.iterrows():
        for col in summaries.columns:
            summary = row[col]
            summary_embedding = model.encode(summary, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(topic_embedding, summary_embedding).item()
            if similarity >= threshold:
                similar_chunks.append(summary)

    return ' '.join(similar_chunks)


def write_survey_paper(topic, topic_description, chatbot, folder_arxiv_pdfs="arxiv_pdfs", filder_arxiv_cits='arxiv_citations'): 
    papers, summaries = summarize_all_papers(folder_arxiv_pdfs, folder_arxiv_cits, api_key, initial_query, 5, 5)
    papers.to_csv(f"papers_df_{initial_query}.csv", index=False)
    summaries.to_csv(f"paper_summaries_{initial_query}.csv", index=False)

    context = get_initial_context(topic, summaries)
    df_subtopics = get_concept_hierarchy(initial_query, description, context)
    
    #outline = write_outline(df_subsubtopics, summaries)
    #citations = get_citations(outline, summaries)
    #paper = write_paper(outline, citations, summaries)
    #paper = revise_paper(paper, outline, summaries)
    #decision, reviews = peer_review(paper, outline, summaries)


if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser(description='Summarize papers based on an initial query.')
    parser.add_argument('topic', type=str, help='The initial seed topic for the survey paper.')
    parser.add_argument('topic_description', type=str, optional=True, default=None, help='A description of the seed topic.')
    args = parser.parse_args()

    # Initialization
    initial_query = args.topic
    topic_description = args.topic_description

    api_key = os.getenv('API_KEY')
    chatbot = Together(api_key=api_key)

    setup_dirs()
    
    # Write paper
    write_survey_paper(initial_query, topic_description, chatbot)
