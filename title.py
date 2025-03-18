# import openai
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv(dotenv_path='D:\AI Projects\Title generator\.env')
# # Get the API key from the environment
# openai_api_key = os.getenv("OPENAI_API_KEY")

# # Set the API key explicitly in the openai module
# if openai_api_key is None:
#     raise ValueError("API key not found. Please check your .env file.")
# else:
#     openai.api_key = openai_api_key


# # Title generation
# def generate_title(topic, tone="engaging",  seo=False, include_emojis=False, title_char_limit=120, title_word_limit=15, num_suggestions=5):
 
#     if seo:
#         prompt = (
#             f"Act as an SEO expert and a YouTube marketer. Create an SEO-optimized YouTube title for {topic}. "
#             f"The title should be {tone} and optimized within {title_char_limit} characters and {title_word_limit} words. "
#         )
#     else:
#         prompt = (
#             f"Act as a YouTube marketer. Create a YouTube title for {topic}. "
#             f"The title should be {tone} and optimized within {title_char_limit} characters and {title_word_limit} words. "
#         )

#     if include_emojis:
#         prompt += " Add relevant emojis to enhance the title."

#     response = openai.Completion.create(
#         engine = "gpt-3.5-turbo-instruct",
#         prompt = prompt, 
#         max_tokens = title_word_limit * 2,  # adjustment of token limit based on words limit
#         n = num_suggestions +1   # add 5 titles with 1 main 
#     )   

#     titles = [choice['text'].strip() for choice in response.choices] 
#     main_title = titles[0] # these are input fields there is slicing 0 means first title as a main title bcz we take titles in list
#     suggestions = titles[1:]  # and here after 0 index all titles are suggestions

#     # generate descripton based on main title 
#     description = generate_description(main_title, descrip_char_limit=250, descrip_words_limit=50)
#     return main_title, suggestions , description

# # Auto Description generation
# def generate_description(title, descrip_char_limit=250, descrip_words_limit=50):
#     prompt = (
#             f"Please write a detailed and engaging description for a video titled: '{title}'. The description should include a concise summary of the video, key points discussed, and any important information that viewers should know. "
#             f"It is essential that the entire description is modified to strictly fit within the specified limits of {descrip_char_limit} characters and {descrip_words_limit} words.Make sure that desription perfectly fit within limit that user sets."
#             f"Description would be well written in good manner must end with full stop sign  . Do not wrap description into double qoutation. Avoid using double quotation mark. "
#             f"Please ensure that all content is crafted thoughtfully to maintain quality while respecting these constraints."
#         )
#     response = openai.Completion.create(
#             engine = "gpt-3.5-turbo-instruct",
#             prompt = prompt, 
#             max_tokens = descrip_words_limit * 2  # adjustment of token based on words
#         )
#     return response.choices[0].text.strip()





