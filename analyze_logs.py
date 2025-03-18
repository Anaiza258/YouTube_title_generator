# is files mi saari details commented kr di gi hin aapki easy understanding k liye
# phle is file ko run kr lena hi
# or pir /analytics ko run krna hi browser mi
# credits : anaiza
import pandas as pd
import plotly.express as px

# Read the log file into a DataFrame
log_df = pd.read_csv("youtube-user-titles.txt", sep=" - ", header=None, names=["timestamp", "details"], engine='python')

# Split the 'details' column into 'Platform' and 'Topic'
log_df[[ 'topic']] = log_df['details'].str.extract(r' Topic: (.*)')

# Drop the 'details' column
log_df.drop(columns=['details'], inplace=True)

# Parse the timestamp column  
# Parsing often involves interpreting strings of data and converting them into a more usable format
log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])


# Number of requests per day
log_df['date'] = log_df['timestamp'].dt.date
requests_per_day = log_df['date'].value_counts().sort_index()  # index is the unique dates 

# Plot the number of requests per day                             # .index mean unique date in chronological order
fig_requests_per_day = px.line(requests_per_day, x=requests_per_day.index, y=requests_per_day.values,
                               labels={'x': 'Date', 'y': 'Number of Requests'},         # .values mean counts of request 
                               title='Number of Requests per Day')
fig_requests_per_day.write_html("static/requests_per_day.html")

# Number of requests per month
log_df['month'] = log_df['timestamp'].dt.to_period('M')
requests_per_month = log_df['month'].value_counts().sort_index() # occurance of each unique month count request per month

# Plot the number of requests per month
fig_requests_per_month = px.bar(requests_per_month, x=requests_per_month.index.astype(str), y=requests_per_month.values,
                                labels={'x': 'Month', 'y': 'Number of Requests'},
                                title='Number of Requests per Month')
fig_requests_per_month.write_html("static/requests_per_month.html") 

# Most common topics
common_topics = log_df['topic'].value_counts().head(10)

# Plot the most common topics
fig_common_topics = px.bar(common_topics, x=common_topics.values, y=common_topics.index, orientation='h',
                           labels={'x': 'Number of Occurrences', 'y': 'Topic'},   # orientation of the bars to horizontal.
                           title='Most Common Topics')
fig_common_topics.write_html("static/common_topics.html")

# analysis: Filter titles based on keywords
def filter_titles(keyword, log_df):
    filtered_df =  log_df[log_df['topic'].str.contains(keyword, case=False, na=False)] # na ->handle missing values(NaN) # case=False -> case insensitive
    total_queries = log_df.shape[0]   # counts the total quries
    keyword_queries = filtered_df.shape[0]   # counts number of queries containing keyword
    return filtered_df, total_queries, keyword_queries


