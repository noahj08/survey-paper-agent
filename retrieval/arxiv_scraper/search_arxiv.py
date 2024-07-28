

import argparse
from arxiv_scraper.query_generator import generate_arxiv_queries
from arxiv_scraper.arxiv_downloader import download_arxiv_papers

def main():
    parser = argparse.ArgumentParser(description="Search arXiv and download papers based on search queries and context.")
    parser.add_argument("--search-query", required=True, help="The initial search query for arXiv.")
    parser.add_argument("--context", default="", help="Additional context to refine the search queries.")
    
    args = parser.parse_args()
    download_papers_for_query(args.search_query, args.context)



def arxiv_query(search_query, context):
    download_papers_for_query(search_query, context)

def download_papers_for_query(initial_query: str, context: str, num_queries=5, max_results=2):
    api_key = "d54dae610f891c57039c871fc9fa4fdb247116726e06f5d8308e3edde2f9f946"
    generated_queries = generate_arxiv_queries(initial_query, api_key, context, num_queries=num_queries)

    for query in generated_queries:
        try:
            download_arxiv_papers(search_query=f"all:{query}", max_results=max_results)
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()

