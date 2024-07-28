# Not used, was a misunderstanding during hackathon
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

def get_topics_df(save_path, api_key, num_topics=5):
    text = extract_text_from_pdf(save_path)
    topics = generate_topics(text, api_key, num_topics)
    topics_list = [line.split('. ', 1)[1] for line in topics.split('\n') if line.strip()]
    summaries = [summarize_text(text, api_key, topic) for topic in topics_list]
    df = pd.DataFrame({"Topic": topics_list, "Summary": summaries})
    return df


    # Print the list of filenames
    # print(file_list)
    #print("Getting the topic list.")
    
    #paper_df_topic_list = []
    #file_list.sort()
    #for file in file_list:
    #    paper_df = get_topics_df(f"{folder_arxiv_pdfs}/{file}", api_key, num_topics)
    #    paper_df['Name']=file[:-4]
    #    with open(f"{folder_arxiv_cits}/{file[:-4]}.bib", "r") as txt_file:
    #        txt_contents = txt_file.read()
    #        paper_df['Citation'] = txt_contents
#
#        paper_df_topic_list.append(paper_df)
#   
#    
#    paper_topics_concat = (pd.concat(paper_df_topic_list))

