import pandas as pd
papers_sum = pd.read_csv("sections_df.csv")
subtopics = pd.read_csv("subtopics.csv")


joined_tables = pd.merge(subtopics, papers_sum,left_on='citation', right_on='Citation', how='left')
joined_tables.to_csv("joined_tables.csv", index=False)
