import pandas as pd

incident_name = 'tacoma'

def create_dataframe():
    df = pd.DataFrame(columns = column_names)
    return df

column_names = ['author_id', 'conversation_id', 'created_at', 'id', 'text', 'like_count', 'quote_count',
       'reply_count', 'retweet_count', 'date_time', 'media_keys', 'referenced_tweets']

test_data_frame = create_dataframe()

test_data_frame.to_csv(incident_name + '.csv', index=False)

print(pd.read_csv(incident_name + '.csv'))
