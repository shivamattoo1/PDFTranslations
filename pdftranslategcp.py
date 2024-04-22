import json
import os
from google.cloud import translate_v3
from google.oauth2 import service_account
import logging

# Setup logging
logging.basicConfig(filename='/workspaces/PDFTranslations/translation_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Translation Client
credentials_path = "/workspaces/PDFTranslations/secure-granite-418218-cb900be2db79.json"
try:
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = translate_v3.TranslationServiceClient(credentials=credentials)
except Exception as e:
    logging.error(f"Failed to create translation client: {e}")
    raise SystemExit(e)

project_id = "secure-granite-418218"
location = "global"
parent = f"projects/{project_id}/locations/{location}"

# Path to the directory containing JSON files
base_directory_path = '/workspaces/PDFTranslations/6638565086221494895'

def translate_text(text, target_language="pa"):
    """Translate text to the target language."""
    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": "en",
                "target_language_code": target_language
            }
        )
        return response.translations[0].translated_text
    except Exception as e:
        logging.error(f"Error during translation: {e}")
        return None

def process_files(directory_path):
    """Recursively process JSON files and translate text in subdirectories."""
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                logging.info(f"Processing file: {file_path}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    extracted_text = data.get('text')
                    if extracted_text:
                        translated_text = translate_text(extracted_text)
                        if translated_text:
                            output_file_path = os.path.join(root, f"{os.path.splitext(filename)[0]}_translated.txt")
                            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                                output_file.write(translated_text + '\n')
                            logging.info(f"Saved translation to {output_file_path}")
                    else:
                        logging.warning(f"No text found in file: {file_path}")
                except Exception as e:
                    logging.error(f"Failed to process file {file_path}: {e}")

if __name__ == "__main__":
    process_files(base_directory_path)
    logging.info("All files processed.")
