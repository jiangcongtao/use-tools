import requests
import json
import os
from utils.get_keys import load_config

# Load configuration

class OllamaModel:
    def __init__(self, model, system_prompt, temperature=0, stop=None, debug_mode = False):
        """
        Initializes the OllamaModel with the given parameters.

        Parameters:
        model (str): The name of the model to use.
        system_prompt (str): The system prompt to use.
        temperature (float): The temperature setting for the model.
        stop (str): The stop token for the model.
        """
        self.model_endpoint = "http://localhost:11434/api/generate"
        self.temperature = temperature
        self.model = model
        self.system_prompt = system_prompt
        self.headers = {"Content-Type": "application/json"}
        self.stop = stop
        self.debug_mode = debug_mode

    def generate_text(self, prompt):
        """
        Generates a response from the Ollama model based on the provided prompt.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        dict: The response from the model as a dictionary.
        """
        payload = {
            "model": self.model,
            "format": "json",
            "prompt": prompt,
            "system": self.system_prompt,
            "stream": False,
            "temperature": self.temperature,
            "stop": self.stop
        }
        
        if self.debug_mode:
            print("PAYLOAD", payload)
        
        try:
            request_response = requests.post(
                self.model_endpoint, 
                headers=self.headers, 
                data=json.dumps(payload)
            )
            
            if self.debug_mode:
                print("REQUEST RESPONSE", request_response)
            request_response_json = request_response.json()
            response = request_response_json['response']
            response_dict = json.loads(response.strip())
            print('-'*80)
            print(f"\nResponse from Ollama model:\n{response.strip()}")
            print('-'*80)
            return response_dict
        except requests.RequestException as e:
            response = {"error": f"Error in invoking model! {str(e)}"}
            return response

    def generate_text2(self, prompt):
        """
        Generates a response from the Ollama model based on the provided prompt.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        str: The response from the model as a text.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": self.system_prompt,
            "stream": False,
            "temperature": self.temperature,
            "stop": self.stop
        }
        
        if self.debug_mode:
            print("PAYLOAD", payload)
        
        try:
            request_response = requests.post(
                self.model_endpoint, 
                headers=self.headers, 
                data=json.dumps(payload)
            )
            
            if self.debug_mode:
                print("REQUEST RESPONSE", request_response)
            request_response_json = request_response.json()
            response = request_response_json['response'].strip()
    
            print('-'*80)
            print(f"\nResponse from Ollama model:\n{response}")
            print('-'*80)
            return response
        
        except requests.RequestException as e:
            response = {"error": f"Error in invoking model! {str(e)}"}
            return response