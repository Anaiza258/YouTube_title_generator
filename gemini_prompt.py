import os
from dotenv import load_dotenv
import google.generativeai as genai
import re


# Load environment variables
load_dotenv()

# Initialize Gemini client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Title generation
def generate_title(topic, tone="engaging", seo=False, include_emojis=False, title_char_limit=120, title_word_limit=15, num_suggestions=5):
    if seo:
        prompt = (
            f"Act as an SEO expert and a YouTube marketer. Create an SEO-optimized YouTube title for {topic}. "
            f"The title should be {tone} and optimized within {title_char_limit} characters and {title_word_limit} words. "
            f"Number of titles are 6. Do not add emojis until user wants. Do not add any heading on top just write 6 titles."
        )
    else:
        prompt = (
            f"Act as a YouTube marketer. Create a YouTube title for {topic}. "
            f"The title should be {tone} and optimized within {title_char_limit} characters and {title_word_limit} words. "
            f"Number of titles are 6. Do not add emojis until user wants.  Do not add any heading on top just write 6 titles."
        )
    
    if include_emojis:
        prompt += " Add relevant emojis to enhance the title."
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    content = response.candidates[0].content.parts[0].text
    
    # Extract titles from response
    titles = content.split("\n")[:num_suggestions + 1]  # Ensuring correct number of titles
    titles = [re.sub(r"\*\*", "", title.strip()) for title in titles if title.strip()]  # Remove empty lines
    
    
    if not titles:
        raise ValueError("No titles generated. Check API response.")
    
    main_title = titles[0]
    suggestions = titles[1:]
    
    # Generate description based on the main title
    description = generate_description(main_title, descrip_char_limit=250, descrip_words_limit=50)
    
    return main_title, suggestions, description

# Auto Description generation
def generate_description(title, descrip_char_limit=250, descrip_words_limit=50):
    prompt = (
        f"Please write a detailed and engaging description for a video titled: '{title}'. The description should include a concise summary of the video, key points discussed, and any important information that viewers should know. "
        f"It is essential that the entire description is modified to strictly fit within the specified limits of {descrip_char_limit} characters and {descrip_words_limit} words. "
        f"Make sure the description perfectly fits within the limit that the user sets. "
        f"The description should be well-written, perfectly done, detail oriented ending with a full stop. Avoid using double quotation marks."
    )
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    content = response.candidates[0].content.parts[0].text.strip()
    
    # Clean any markdown formatting
    content = re.sub(r"```|```json", "", content).strip()
    
    return content
