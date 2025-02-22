import requests
import streamlit as st
from typing import Optional, Dict, Any, Generator
import json

# API Configuration
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_ENDPOINT = "https://api.sambanova.ai/v1/chat/completions"
MODEL_ID = "DeepSeek-R1-Distill-Llama-70B"
API_KEY = os.getenv("SAMBANOVA_API_KEY", "")  # Get API key from environment variable

class SambanovaChat:
    def __init__(self, api_key: str = API_KEY, model_id: str = MODEL_ID):
        """Initialize Sambanova chat client"""
        self.api_key = api_key
        self.model_id = model_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate_response(self, message: str, inference_config: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Generate a complete response using Sambanova Cloud"""
        response_text = ""
        for chunk in self.generate_stream(message, inference_config):
            response_text += chunk
        return response_text

    def generate_stream(self, message: str, inference_config: Optional[Dict[str, Any]] = None) -> Generator[str, None, None]:
        """Generate a streaming response using Sambanova Cloud"""
        if inference_config is None:
            inference_config = {"temperature": 0.7}

        payload = {
            "stream": True,
            "model": self.model_id,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful Romanian language learning assistant"
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        try:
            with requests.post(
                API_ENDPOINT,
                headers=self.headers,
                json=payload,
                stream=True
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        chunk = line.decode('utf-8')
                        if chunk.startswith('data: '):
                            chunk_data = chunk[6:]
                            if chunk_data != '[DONE]':
                                try:
                                    chunk_obj = json.loads(chunk_data)
                                    if 'choices' in chunk_obj and len(chunk_obj['choices']) > 0:
                                        delta = chunk_obj['choices'][0].get('delta', {})
                                        content = delta.get('content', '')
                                        if content:
                                            yield content
                                except json.JSONDecodeError as e:
                                    st.error(f"Error decoding JSON: {str(e)}")
                                    continue
                                except Exception as e:
                                    st.error(f"Unexpected error: {str(e)}")
                                    continue
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            yield ""


if __name__ == "__main__":
    # Replace with your actual API key
    api_key = "your-api-key-here"
    chat = SambanovaChat(api_key)
    while True:
        user_input = input("You: ")
        if user_input.lower() == '/exit':
            break
        for chunk in chat.generate_stream(user_input):
            print(chunk, end='', flush=True)
        print()
