from flask import Flask, render_template, request,  send_from_directory , jsonify
from title import generate_title, generate_description
from datetime import datetime
import openai
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    main_title = None
    suggestions = []
    topic = ''
    description = None
    tone = 'engaging'
    seo = False  # Default SEO setting
    include_emojis = False  # Default emoji setting
    title_char_limit = 120  # default limit
    title_word_limit = 15
    descrip_char_limit = 250 
    descrip_words_limit = 50  # default limits  
    

    if request.method == 'POST':
        action = request.form['action']

        if action in ['generate', 'regenerate']:
            topic = request.form['topic']
            tone = request.form.get('tone', 'engaging')  # Default tone is 'engaging'
            seo = request.form.get('seo') == 'yes'  # Check if SEO yes selected
            include_emojis = request.form.get('include_emojis') == 'yes'  # Check if emoji checkbox is checked
            title_char_limit = int(request.form.get('title_char_limit', 120))
            title_word_limit = int(request.form.get('title_word_limit', 15))
            main_title, suggestions, description = generate_title( topic, tone, seo=seo, include_emojis=include_emojis, title_char_limit=title_char_limit, title_word_limit=title_word_limit)

        else:  # Retain values in the page for re-rendering
            main_title = request.form.get('main_title')
            suggestions = request.form.get('suggestions').split(',')
            topic = request.form.get('topic') 
            tone = request.form.get('tone')
            seo = request.form.get('seo') == 'yes'
            include_emojis = request.form.get('include_emojis') == 'yes'
            title_char_limit = int(request.form.get('title_char_limit'))
            title_word_limit = int(request.form.get('title_word_limit'))
            descrip_char_limit = int(request.form.get('descrip_char_limit'))
            descrip_words_limit = int(request.form.get('descrip_words_limit'))


        # Log user input
        log_input(topic)

    return render_template('index.html', main_title=main_title, suggestions=suggestions, topic=topic, tone=tone, seo=seo, include_emojis=include_emojis,  description=description,  title_char_limit=title_char_limit, title_word_limit=title_word_limit, descrip_char_limit=descrip_char_limit, descrip_words_limit=descrip_words_limit)


# user title base description
@app.route('/description', methods=['POST'])
def generate_description():
    try:
        # Extract the user-provided text from the JSON request
        data = request.get_json()
        user_desc_txt = data['text']
        desc_char_limit = int(data.get('desc_char_limit', 250))
        desc_word_limit = int(data.get('desc_word_limit', 50))


        # Construct the prompt for OpenAI
        prompt = (
            f"Please write a detailed and engaging description for a video titled: '{user_desc_txt}'. The description should include a concise summary of the video, key points discussed, and any important information that viewers should know. "
            f"It is essential that the entire description is modified to strictly fit within the specified limits of {desc_char_limit} characters and {desc_word_limit} words. "
            f"Description would be well written in good manner must end with full stop sign  . Do not wrap description into double qoutation. Avoid using double quotation mark. "
            f"Please ensure that all content is crafted thoughtfully to maintain quality while respecting these constraints."
        )

        # Call OpenAI's API to generate the description
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens = desc_word_limit * 2  # Adjust as needed
        )

        # Extract and format the generated description
        generated_description = response.choices[0].text.strip()

        # Return the generated description as JSON
        return jsonify({'desc': generated_description})

    except KeyError:
        return jsonify({'error': 'Invalid request format. Missing "text", "desc_char_limit", or "desc_word_limit" in JSON data.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Analysis 
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/filter', methods=['POST'])
def filter():
    keyword = request.form.get('keyword')
    filtered_titles, total_queries, keyword_queries  = filter_titles(keyword)
    filtered_html = filtered_titles.to_html(index=False)

    summary_html = f"""
    <div style="background-color: #B5DEFF ; padding: 20px; border-radius: 8px;">
        <h2> Summary for keywords: {keyword} </h2>
        <p style="font-size: 20px; ;"> Total Queries: {total_queries} </p>
        <p style="font-size: 20px; ;"> Queries with Keyword {keyword} : {keyword_queries} </p>
    </div>
    {filtered_html}
    """
    return summary_html

def log_input(topic):
    with open("youtube-user-titles.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} -  Topic: {topic}\n")

def filter_titles(keyword):
    log_df = pd.read_csv("youtube-user-titles.txt", sep=" - ", header=None, names=["timestamp", "details"], engine='python')
    log_df[['topic']] = log_df['details'].str.extract(r' Topic: (.*)')
    log_df.drop(columns=['details'], inplace=True)
    log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])

    total_queries = log_df.shape[0]   # counts the total quries
    filtered_df =  log_df[log_df['topic'].str.contains(keyword, case=False, na=False)] # na ->handle missing values(NaN) # case=False -> case insensitive
    keyword_queries = filtered_df.shape[0]   # counts number of queries containing keyword
    return  filtered_df, total_queries, keyword_queries


if __name__ == '__main__':
    app.run(debug=True)
