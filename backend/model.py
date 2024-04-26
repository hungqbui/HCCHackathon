from transformers import pipeline
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold 

gemini_api = "AIzaSyCbHdHoBgfs958jOQODX_a7IwKkteoqUBA"

genai.configure(api_key=gemini_api)

llm = genai.GenerativeModel('gemini-pro')

SAFETY = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
}

def get_image_caption(image_url):
    captioner = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
    caption = captioner(image_url)

    return caption[0]['generated_text']

def describe_image(image_caption):
    prompt = f"""
    Given the image caption "{image_caption}", describe the image in more detail in 100 words. This is likely to be an image of a food item, provide the name of the dish, espcially the origins of the dish and the culture, and any other relevant information. If it is not a food item, tell the user that you can only provide information on food items so. Do not say that your input is a caption.

    Your response should be in the following format and strictly in this format only:
    {{
        "name": "Name of the dish",
        "origin": "Origins of the dish",
        "description": "Description of the dish talk about the cultural value of the dish and any other relevant information"
    }}
"""
    
    response = llm.generate_content(prompt, safety_settings=SAFETY)

    return response.text.replace("`", "")

def generate_query(input, position):
    prompt = f"""
    Construct a JSON object that contains some good keywords for a google search about the following information: {input}. The user is located in {position}. The JSON object should be in the following format and strictly in this format only:
    START OF FORMAT
    {{
        "query": [Some search terms here i.e 'where to eat...'"], 
    }}
    END OF FORMAT
    The "query" fields are the words that you think would be relevant to find more information about the food.
"""
    
    response = llm.generate_content(prompt, safety_settings=SAFETY)

    return response.text
    
