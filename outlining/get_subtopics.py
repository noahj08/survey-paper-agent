import pandas as pd
from together import Together
import sys
sys.path.append('AIResearcher/')
from prompts import get_subtopic_generation_prompt
from utils import extract_valid_json, format_context

def get_subtopics(df_topics, chatbot, context, max_llm_retries=3,
                  outfile='subtopics.csv'):
    output = []
    for i,row in df_topics.iterrows():
        topic = row['Topic']
        description = None
        if 'Summary' in row:
            description = row['Summary']
        context = format_context(row['Context'])
        prompt = get_subtopic_generation_prompt(topic, description)
                                                context)
        response = chatbot.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[{"role": "user", "content": prompt}]
        )
        
        llm_retry = 0
        while llm_retry < max_llm_retries:
            response_content = response.choices[0].message.content
            response_json = extract_valid_json(response_content)
            if response_content is not None:
                break
            llm_retry += 1
        if response_content is None:
            return None
        df_subtopics = pd.DataFrame(response_json) # subtopic, subtopic_description
        df_subtopics['topic'] = topic
        df_subtopics['description'] = description
        df_subtopics['citation'] = row['Citation']
        output.append(df_subtopics)
    df_subtopics = pd.concat(output)
    df_subtopics.to_csv(outfile, index=False)
    return df_subtopics

chatbot = Together(api_key=API_KEY)
df_topics = pd.read_csv('papers_df.csv')
get_subtopics(df_topics, chatbot, max_llm_retries=3,
              outfile='subtopics.csv')
