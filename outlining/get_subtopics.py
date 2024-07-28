import pandas as pd
from together import Together
from utils import extract_valid_json, format_context
from prompts import SubtopicPrompts


# TODO modify this function so that the output columns match the input columns.
# TODO modify the function so the df that is returned contains all columns we need (topic, sub, subsub, etc)
def get_subtopics(df_topics, chatbot, context, max_llm_retries=3, outfile='subtopics.csv'):
    output = []
    for i, row in df_topics.iterrows():
        topic = row['topic']
        description = row.get('description', None)
        context_str = format_context(row.get('Context'], None))
        prompt = SubtopicPrompts.get_subtopic_generation_prompt(topic, description, context_str)
        response = chatbot.chat.completions.create(model="meta-llama/Llama-3-8b-chat-hf", messages=[{"role": "user", "content": prompt}])
        llm_retry = 0
        while llm_retry < max_llm_retries:
            response_content = response.choices[0].message.content
            response_json = extract_valid_json(response_content)
            if response_content is not None:
                break
            llm_retry += 1
        if response_content is None:
            return None
        df_subtopics = pd.DataFrame(response_json)
        df_subtopics['topic'] = topic
        df_subtopics['description'] = description
        df_subtopics['citation'] = row['Citation']
        output.append(df_subtopics)
    df_subtopics = pd.concat(output)
    df_subtopics.to_csv(outfile, index=False)
    return df_subtopics

def get_concept_hierarchy(initial_query, description, context)
    df_initial_topic = pd.DataFrame({'topic': [initial_query], 'description': [description], 'context': [None]})
    df_subtopics = get_subtopics(df_initial_topic, chatbot, max_llm_retries=3, outfile='subtopics.csv')
    df_subsubtopics = []
    for _,row in df_subtopics:
        subtopic = row['topic']
        df_subsubtopic = get_subtopics(row, chatbot, max_llm_retries=3, outfile=f'{subtopic}_subtopics.csv')
        df_subsubtopics.append(df_subsubtopic)
    df_subsubtopics = pd.concat(df_subsubtopics)


if __name__ == "__main__":
    chatbot = Together(api_key=API_KEY)
    df_topics = pd.read_csv('papers_df.csv')
    get_subtopics(df_topics, chatbot, max_llm_retries=3, outfile='subtopics.csv')

    return df_subtopics
