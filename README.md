# use-tools
A simple project for enabling LLM agents to use tools.


### Prerequisites

#### Environment Setup
1. **Install Anaconda:**  
   Download Anaconda from [https://www.anaconda.com/](https://www.anaconda.com/).

2. **Create a Virtual Environment:**
   ```bash
   conda create -n agent_env python=3.11 pip
   ```
   
3. **Activate the Virtual Environment:**
   ```bash
   conda activate agent_env
   ```

### Clone and Navigate to the Repository
1. **Clone the Repo:**
   ```bash
   git clone https://github.com/john-adeojo/use-tools.git
   ```
2. **Navigate to the Repo:**
   ```bash
   cd /path/to/your-repo/use-tools
   ```

3. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

### Configure API Keys for use with OpenAI
1. **Open the `config.yaml`:**
   ```bash
   nano config.yaml
   ```
   - **OpenAI API Key:** Get it from [https://openai.com/](https://openai.com/)


## If you want to work with Ollama

### Setup Ollama Server
1. **Download Ollama:**
   Download [https://ollama.com/download](https://ollama.com/download)

2. **Download an Ollama Model:**
   ```bash
   curl http://localhost:11434/api/pull -d "{\"name\": \"llama3:instruct\"}"
   ```
Ollama [API documentation](https://github.com/ollama/ollama/blob/main/docs/api.md#list-local-models)

3. Navigate to the bottom of the `agent.py` script and uncomment the Ollama arguments and comment out the OpenAI arguments. 

### Configure API KEY
Weather and time tools requires an API from http://api.openweathermap.org to be setup for tools to function properly.

```shell
export WEATHER_API_KEY=<YOUR API KEY>
```

### Run Your Query In Shell
```bash
python -m agents.agent
```
Then enter your query.

### Get help
```bash
python -m agents.agent -h    
usage: agent.py [-h] [--notool] [--model MODEL]

Agent with tools

options:
  -h, --help     show this help message and exit
  --notool       Run the agent without any tools
  --model MODEL  Specify the model name
```

Example usage output:
```shell
$ python -m agents.agent --model qwen2:7b
Loaded tools:  ['basic_calculator', 'reverse_string', 'get_current_weather', 'get_local_time']
Using model:  qwen2:7b
Ask me anything: What is weather like in Shanghai
--------------------------------------------------------------------------------

Response from Ollama model:
{
  "tool_choice": "get_current_weather",
  "tool_input": "{\"city_name\": \"Shanghai\"}"
}
--------------------------------------------------------------------------------
Executed using get_current_weather function
[TOOL]:
Current weather in Shanghai [CN]: light intensity shower rain
Temperature: 30.25 °C
--------------------------------------------------------------------------------

Response from Ollama model:
The current weather conditions in Shanghai, China, include light intensity shower rain. The temperature is currently at 30.25 degrees Celsius.
--------------------------------------------------------------------------------
[AI]:
The current weather conditions in Shanghai, China, include light intensity shower rain. The temperature is currently at 30.25 degrees Celsius.
================================================================================
Ask me anything: What is the local time in Shanghai
--------------------------------------------------------------------------------

Response from Ollama model:
{
  "tool_choice": "get_local_time",
  "tool_input": {
    "city_name": "Shanghai"
  }
}
--------------------------------------------------------------------------------
Executed using get_local_time function
[TOOL]:
Current local time in Shanghai [CN]
Local Time: 2024-06-22 15:09:55 CST
--------------------------------------------------------------------------------

Response from Ollama model:
As of today, June 22nd, 2024 at 3:09 PM and 55 seconds, it is the current local time in Shanghai, China.
--------------------------------------------------------------------------------
[AI]:
As of today, June 22nd, 2024 at 3:09 PM and 55 seconds, it is the current local time in Shanghai, China.
================================================================================
Ask me anything: Reverse the string: Hello World
--------------------------------------------------------------------------------

Response from Ollama model:
{
  "tool_choice": "reverse_string",
  "tool_input": "{\"input_string\": \"Hello World\"}"
}
--------------------------------------------------------------------------------
[TOOL]:
The reversed string is: }"dlroW olleH" :"gnirts_tupni"{

.Executed using the reverse_string function.
--------------------------------------------------------------------------------

Response from Ollama model:
The reversed string is "dlroW olleH", which was obtained by executing the reverse_string function.
--------------------------------------------------------------------------------
[AI]:
The reversed string is "dlroW olleH", which was obtained by executing the reverse_string function.
================================================================================
Ask me anything: Tell me a joke about dog
--------------------------------------------------------------------------------

Response from Ollama model:
{
  "tool_choice": "no tool",
  "tool_input": "None"
}
--------------------------------------------------------------------------------
{'tool_choice': 'no tool', 'tool_input': 'None'}
--------------------------------------------------------------------------------

Response from Ollama model:
Sure, here's a classic one:

Why did the scarecrow win an award?

Because he was outstanding in his field. 

I hope you found that amusing! Let me know if you need another kind of joke or any other information.
--------------------------------------------------------------------------------
[AI]:
Sure, here's a classic one:

Why did the scarecrow win an award?

Because he was outstanding in his field. 

I hope you found that amusing! Let me know if you need another kind of joke or any other information.
================================================================================

```
