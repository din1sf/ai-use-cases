import streamlit as st
from PIL import Image
from openai import OpenAI
import base64


client = OpenAI()

st.title('Get selected text from image')

def process_image(base64_image):
    system_message = """
You are a helpful assistant. 
Your task is to extract the text that is surrounding with rectangle or ellipse shape from the image.
The text can be also selected with a color.
Only the text inside the shape will must be output in json format with key "text".
"""
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "system",
        "content": f"{system_message}" 
        },
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "Get the selected text from the image."}, 
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    max_tokens=2000,
    )
    result = response.choices[0].message.content
    return result


with st.expander('From camera'):
    st.write('Take a picture')
    picture = st.camera_input("Take a picture")

    if picture:
        st.image(picture)
        base64_image = base64.b64encode(picture.read()).decode('utf-8')
        if st.button('Process image', key='camera_button'):
            with st.spinner('Processing...'):
                result = process_image(base64_image)
                st.info(result)


with st.expander('From file'):
    st.write('Upload an image')
    uploaded_file = st.file_uploader("Choose an image...")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        uploaded_file.seek(0)
        base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')

        if st.button('Process image', key='upload_button'):
            with st.spinner('Processing...'):
                result = process_image(base64_image)
                st.info(result)
