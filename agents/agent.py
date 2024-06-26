from termcolor import colored
from prompts.prompts import agent_system_prompt_template
from models.openai_models import OpenAIModel
from models.ollama_models import OllamaModel
from tools.basic_calculator import basic_calculator
from tools.reverser import reverse_string
from tools.weather import get_current_weather, get_local_time
from toolbox.toolbox import ToolBox
import os
import argparse

class Agent:
    def __init__(self, tools, model_service, model_name, stop=None, debug_mode=False):
        """
        Initializes the agent with a list of tools and a model.

        Parameters:
        tools (list): List of tool functions.
        model_service (class): The model service class with a generate_text method.
        model_name (str): The name of the model to use.
        """
        self.tools = tools
        self.model_service = model_service
        self.model_name = model_name
        self.stop = stop
        self.debug_mode = debug_mode

    def prepare_tools(self):
        """
        Stores the tools in the toolbox and returns their descriptions.

        Returns:
        str: Descriptions of the tools stored in the toolbox.
        """
        toolbox = ToolBox()
        toolbox.store(self.tools)
        tool_descriptions = toolbox.tools()
        return tool_descriptions

    def think(self, prompt):
        """
        Runs the generate_text method on the model using the system prompt template and tool descriptions.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        dict: The response from the model as a dictionary.
        """
        tool_descriptions = self.prepare_tools()
        agent_system_prompt = agent_system_prompt_template.format(tool_descriptions=tool_descriptions)

        if self.debug_mode:
            print("SYSTEM PROMPT: ")
            print(agent_system_prompt)
        # Create an instance of the model service with the system prompt

        if self.model_service == OllamaModel:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0,
                stop=self.stop,
                debug_mode=self.debug_mode
            )
        else:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0,
                debug_mode=self.debug_mode
            )

        # Generate and return the response dictionary
        agent_response_dict = model_instance.generate_text(prompt)
        return agent_response_dict
    
    def generate(self, prompt):
        """
        Runs the generate_text method on the model using the system prompt and user prompt.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        answer: The response from the model as a dictionary.
        """

        agent_system_prompt = "You're a helpful assistant"

        if self.debug_mode:
            print("SYSTEM PROMPT: ")
            print(agent_system_prompt)
        # Create an instance of the model service with the system prompt

        if self.model_service == OllamaModel:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0,
                stop=self.stop,
                debug_mode=self.debug_mode
            )
        else:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0,
                debug_mode=self.debug_mode
            )

        # Generate and return the response dictionary
        response = model_instance.generate_text2(prompt)
        return response

    def work(self, prompt):
        """
        Parses the dictionary returned from think and executes the appropriate tool.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        The response from executing the appropriate tool or the tool_input if no matching tool is found.
        """
        agent_response_dict = self.think(prompt)
        if isinstance(agent_response_dict, dict): 
            tool_choice = agent_response_dict.get("tool_choice")
            tool_input = agent_response_dict.get("tool_input")

            for tool in self.tools:
                if tool.__name__ == tool_choice:
                    response = tool(tool_input).strip()

                    print(colored(f"[TOOL]:\n{response}", 'cyan'))
                    return response

            print(colored(agent_response_dict, 'cyan'))
        else:
            print(colored(tool_input, 'cyan'))
        return None


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent with tools")
    parser.add_argument("--notool", action="store_true", help="Run the agent without any tools")
    parser.add_argument("--model", type=str, default="", help="Specify the model name")

    args = parser.parse_args()
    if args.notool:
        tools = []
        print('No tools are loaded!')
    else:
        tools = [basic_calculator, reverse_string, get_current_weather, get_local_time]
        print('Loaded tools: ',  [tool.__name__ for tool in tools])

    # Uncomment below to run with OpenAI
    # model_service = OpenAIModel
    # model_name = 'gpt-3.5-turbo'
    stop = None

    # Uncomment below to run with Ollama
    model_service = OllamaModel
    if args.model:
        model_name = args.model
    else:
        model_name = os.environ.get('MODEL', 'phi3:latest')
    # model_name = 'llama3:instruct'
    # stop = "<|eot_id|>"
    print('Using model: ', model_name)

    debug_mode = False
    debug_env = os.environ.get('DEBUG', '').lower()
    if debug_env in ['1', 'true', 'yes']:
        debug_mode = True

    agent = Agent(tools=tools, model_service=model_service, model_name=model_name, stop=stop, debug_mode=debug_mode)

    while True:
        print(colored("Ask me anything: ", 'yellow'), end="")
        prompt = input()
        if prompt.lower() == "exit":
            break
    
        tool_response = agent.work(prompt)
        if tool_response is None:
            response = agent.generate(prompt)
        else:
            response = agent.generate(f"Rewrite the text and output in the human natural language.\TEXT:{tool_response}")
 
        print(colored(f"[AI]:\n{response}", 'cyan'))
        print('=='*40)
