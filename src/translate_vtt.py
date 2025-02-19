import json
import sys
import pysubs2
from openai import OpenAI
import os
from outlines import models,generate
from outlines.models.openai import OpenAIConfig
from pydantic import BaseModel,ConfigDict
from typing import List

class TranslatedSubtitle(BaseModel):
    translated:List[str]

def translate_vtt(input_file: str, output_file: str, target_language: str,model_name:str) -> None:
    try:
        # Load the subtitle file
        subs = pysubs2.load(input_file, encoding="utf-8")
    except Exception as e:
        print(f"Error loading subtitle file: {e}")
        sys.exit(1)

    # Collect all text entries
    texts = [evt.text for evt in subs]  

    # Prepare the JSON prompt for translation
    subtitles_json = json.dumps(texts, ensure_ascii=False)
    prompt = (
        f"Translate the following list of subtitle texts into {target_language}. "
        "Return a JSON array where each element is the translation corresponding to the input text, in the same order.\n\n"
        f"Subtitles: {subtitles_json}"
    )

    try:
        # Initialize the OpenAI client
        openai_api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("BASE_URL")
        client = OpenAI(api_key=openai_api_key, base_url=base_url)
        config = OpenAIConfig(model=model_name)
        model=models.openai(client, config)
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        sys.exit(1)

    max_retries = 3
    retries = 0
    translations = None
    while retries < max_retries:
        try:
            generate.json(model,TranslatedSubtitle)
            if not (isinstance(translations, list) and len(translations) == len(texts)):
                raise ValueError("Number of translations does not match the number of subtitle entries.")
            break
        except Exception as e:
            print(f"Attempt {retries+1} failed: {e}")
            retries += 1
            if retries==max_retries:
                print("Error: Max retries reached. Exiting.")
                sys.exit(1)

    # Update each subtitle event with the translated text
    for evt, translated_text in zip(subs, translations):
        evt.text = translated_text.strip()

    try:
        subs.save(output_file, format="vtt", encoding="utf-8")
        print(f"Translated subtitle file saved to: {output_file}")
    except Exception as e:
        print(f"Error saving translated file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Translate VTT subtitle file to target language."
    )
    parser.add_argument("input_file", nargs="?", default="downloads/test_1min.vtt", help="Input VTT file path.")
    parser.add_argument("output_file", nargs="?", default="downloads/test_1min_translated.vtt", help="Output VTT file path.")
    parser.add_argument("target_language", nargs="?", default="chinese", help="Target language for translation.")
    parser.add_argument("model_name", nargs="?", default="deepseek-r1-distill-llama-70b", help="Model name for translation.")
    args = parser.parse_args()

    translate_vtt(args.input_file, args.output_file, args.target_language,args.model_name)
