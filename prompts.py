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
                "enhancines the updated prompts.py file with the new get_subtopic_generation_prompt function added:
                text generation models by incorporating information retrieved from external sources. This approach "
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
