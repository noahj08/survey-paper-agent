import os
from together import Together

def generate_arxiv_queries(initial_query: str, api_key: str, context: str = "", num_queries=1) -> list:
    """
    Generate a list of x unique search queries for arXiv based on an initial query.
    
    Args:
        initial_query (str): The initial query to base the generated queries on.
        api_key (str): The API key for the Together service.
        context (str): Additional context to be used in the prompt.
    
    Returns:
        list: A list of x unique search queries.
    """
    client = Together(api_key=api_key)

    context_str = f" considering the following context: {context}" if context else ""
prompt = (f"You are part of a system tasked to generate serach queries on the ArXiV search engine in order to build a repository of papers for use in a survey paper about {initial_query}. Generate {num_queries} unique and relevant search queries for arXiv based on the initial query '{initial_query}'"
          f"{context_str}. Provide the queries in a comma-separated format without any additional text. EXAMPLE: initial_query: Retrieval augmented generation, RESPONSE: 'RAG', 'RAG LLM', 'Retrieval-Augmented LLM', 'Retrieval'")

    response = client.chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=[{"role": "user", "content": prompt}],
    )

    response_content = response.choices[0].message.content
    generated_queries = [query.strip() for query in response_content.split(",")]

    return generated_queries

