import os
import openai
from openai import OpenAI
import pysubs2
import json
import time

# Set your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
if not api_key:
    raise ValueError("The API key is not set. Please set the 'OPENAI_API_KEY' environment variable.")

def translate_vtt(input_vtt, output_vtt, target_language, model_name):
    # Load the VTT file
    subs = pysubs2.load(input_vtt, encoding="utf-8")
    
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    system_prompt = (
        "You are a helpful assistant. Translate the following subtitles to {target_language}. "
        "Ensure the translation maintains the context and meaning of the original text, and preserve the original line separations. "
        "Return the translation as a JSON object with a key 'lines' that contains a list of translated lines in order."
    )
    retries = 3
    for attempt in range(retries):
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {'role': 'system', 'content': system_prompt.format(target_language=target_language)},
                    {'role': 'user', 'content': json.dumps({
                        "lines": [line.text for line in subs],
                        "target_language": target_language
                    })}
                ],
                response_format="json"
            )
            result_json = completion.model_dump_json()
            print(result_json)
            result = json.loads(result_json)
            if "lines" in result and isinstance(result["lines"], list):
                break
        except Exception:
            pass

        if attempt < retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
    else:
        raise ValueError("The model did not return a valid response after retries.")
   
    # Split the translated text back into lines
    translated_lines = result.split("\n")
    
    # Substitute the original lines with the translated lines
    for i, line in enumerate(subs):
        line.text = translated_lines[i]
    
    # Save the translated VTT file
    if output_vtt:
        subs.save(output_vtt)
    else:
        return subs
    

if __name__ == "__main__":
    input_vtt = 'downloads/test_1min.vtt'
    output_vtt = 'downloads/test_1min_translated.vtt'
    target_language = 'chinese'
    model_name = 'qwen2.5-7b-instruct-1m'
    translate_vtt(input_vtt, output_vtt, target_language, model_name)
