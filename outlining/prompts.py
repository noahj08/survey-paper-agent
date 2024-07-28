def get_subtopic_generation_prompt(topic, description, context):
    if description is not None:
        output = """You will be given a research area and a brief overview of this area.
You will output a JSON dictionary with two columns, "Subtopic" and "Subtopic Description"
In these fields, describe all academic areas which are sub-topics of the original topic.
Make sure that your list of subtopics makes sense as a set of distinct and comprehensive sub-topics that somebody trying to learn about the original topic would need to know in order to fully understand the space.
Here is an example of what you should do:
INPUTS:
RESEARCH_AREA: "Retrieval Augmented Generation", 
DESCRIPTION: "Retrieval augmented generation is a research topic at the intersection of natural language processing and artificial intelligence, focusing on enhancing text generation models by incorporating information retrieved from external sources. This approach aims to improve the relevance, coherence, and factual accuracy of generated text by leveraging relevant data or knowledge retrieved from large-scale repositories like databases, documents, or the web. By integrating retrieval mechanisms into generative models, researchers seek to create more contextually aware and informative outputs, addressing challenges such as content fidelity and diversity in automated content generation tasks. This paradigm holds promise for applications in automated summarization, question answering, and personalized content creation across various domains."
YOUR RESPONSE: {
"subtopic_name": [
"Information Retrieval Techniques",
"Content Selection and Fusion",
"Evaluation Metrics",
"Domain-Specific Applications"
],
"subtopic_description": [
"Methods for effectively retrieving relevant information from large-scale datasets, including keyword-based search, semantic search, and document retrieval.",
"Strategies for selecting and fusing retrieved content into generated outputs while maintaining coherence, relevance, and factual accuracy.",
"Development of metrics and benchmarks to assess the performance of RAG models in terms of informativeness, diversity, and alignment with retrieved information.",
"Exploration of RAG techniques in specific applications such as medical text generation, legal document summarization, and personalized content creation in e-commerce, adapting methodologies to suit different domains' requirements and challenges."
]
}
Now, your turn.
INPUTS:
RESEARCH_AREA: """  + f'{topic}' +"""
DESCRIPTION: """ + f'{description}' +"""
Context: """ + f'{context}' + """
YOUR RESPONSE: {"""
    else:
        output = """You will be given a research area; you are trying to write an outline for a survey paper about that area.
You will output a JSON dictionary with two columns, "Subtopic" and "Subtopic Description"
In these fields, describe all academic areas which are sub-topics of the original topic.
Here is an example of what you should do:
INPUTS:
RESEARCH_AREA: "Retrieval Augmented Generation", 
DESCRIPTION: "Retrieval augmented generation is a research topic at the intersection of natural language processing and artificial intelligence, focusing on enhancing text generation models by incorporating information retrieved from external sources. This approach aims to improve the relevance, coherence, and factual accuracy of generated text by leveraging relevant data or knowledge retrieved from large-scale repositories like databases, documents, or the web. By integrating retrieval mechanisms into generative models, researchers seek to create more contextually aware and informative outputs, addressing challenges such as content fidelity and diversity in automated content generation tasks. This paradigm holds promise for applications in automated summarization, question answering, and personalized content creation across various domains."
YOUR RESPONSE: {
"subtopic_name": [
"Information Retrieval Techniques",
"Content Selection and Fusion",
"Evaluation Metrics",
"Domain-Specific Applications"
],
"subtopic_description": [
"Methods for effectively retrieving relevant information from large-scale datasets, including keyword-based search, semantic search, and document retrieval.",
"Strategies for selecting and fusing retrieved content into generated outputs while maintaining coherence, relevance, and factual accuracy.",
"Development of metrics and benchmarks to assess the performance of RAG models in terms of informativeness, diversity, and alignment with retrieved information.",
"Exploration of RAG techniques in specific applications such as medical text generation, legal document summarization, and personalized content creation in e-commerce, adapting methodologies to suit different domains' requirements and challenges."
]
}
Now, your turn.
INPUTS:
RESEARCH_AREA: """  + f'{topic}' +"""
DESCRIPTION: """ + f'{description}' +"""
Context: """ + f'{context}' + """
YOUR RESPONSE: {"""
    return output
