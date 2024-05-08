import os
from google.cloud import storage
from vertexai.generative_models import GenerativeModel, Part
import vertexai

import vertexai.preview.generative_models as generative_models


# Initialize Vertex AI
vertexai.init(project="ps2server", location="us-central1")
print("Vertex AI initialized.")

# Setup Google Cloud Storage client
storage_client = storage.Client()
bucket = storage_client.bucket('match_pdf')
print("Google Cloud Storage client setup.")

async def process_message(text):
    print("Processing message...")
    # Use the specific model ID directly.
    model = GenerativeModel("gemini-1.5-pro-preview-0409")
    print("Model loaded: gemini-1.5-pro-preview-0409")

    # Configuration for the generation process.
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }
    print(f"Generation config: {generation_config}")

    # Define safety settings using enums for clarity.
    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    print(f"Safety settings: {safety_settings}")

    responses = model.generate_content(
        [text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True
    )
    print(responses)
    
    response_text = ""
    for response in responses:
        response_text += response.text
    
    return response_text

async def upload_file_to_gcs(user_id, file_path):
    print(f"Uploading {file_path} to Google Cloud Storage...")
    blob = bucket.blob(f'user_{user_id}/{os.path.basename(file_path)}')
    blob.upload_from_filename(file_path)
    print(f"File uploaded to gs://{bucket.name}/{blob.name}")
    return f"gs://{bucket.name}/{blob.name}"

async def process_pdf_file(user_id, file_path):
    print(f"Processing PDF file: {file_path}")
    model = GenerativeModel(model_name="gemini-1.5-pro-preview-0409")
    print("Model for PDF processing loaded.")
    pdf_uri = await upload_file_to_gcs(user_id, file_path)
    pdf_file = Part.from_uri(pdf_uri, mime_type="application/pdf")
    prompt = "Пожалуйста создай текст из этого PDF СДЕЛАЙ ЭТО НА РУССКОМ ЯЗЫКЕ"
    print(f"Generating content from PDF at {pdf_uri} with prompt: {prompt}")

    response = model.generate_content([pdf_file, prompt])
    print(response.text)
    return response.text
