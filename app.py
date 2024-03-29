from dotenv import load_dotenv

load_dotenv()

import streamlit as st 
import os
from PIL import Image
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##function to load Gemini Pro Vision
model=genai.GenerativeModel("gemini-pro-vision")

 

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text


## conversion of the uploaded image--> bytes
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        ##read the file as bytes
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts

    else:
        raise FileNotFoundError("No file has been uploaded")   



st.set_page_config(page_title="Multilanguage invoice extractor")
st.header("Invoice Extractor")

input=st.text_input("Input:",key="input")
uploaded_file=st.file_uploader("Choose image....",type=['jpg','jpeg','png'])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)
## st.image--> to display the uploaded image


submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. We will upload an image
as invoices, and you'll have to answer any questions based on the uploaded image.
"""

##IF submit button is clicked
if submit:
    image_data=input_image_setup(uploaded_file)
    ##getting the image data
    response=get_gemini_response(input,image_data,input_prompt)
    st.subheader("Reponse is")
    st.write(response)
