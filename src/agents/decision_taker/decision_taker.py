import json
from jinja2 import Environment, BaseLoader
import ast
from src.llm import LLM

# decision_prompt = open("src/agents/decision_taker/prompt.jinja2").read().strip()
decision_prompt = open("C:/Users/Asus/Downloads/charity work/Athena/src/agents/decision_taker/prompt.jinja2").read().strip()


import json
import re

class DecisionTaker:
    def __init__(self, base_model) -> None:
        self.llm = LLM(base_model)

    def render(self, prompt: str) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(decision_prompt)

        return template.render(prompt=prompt)

    def validate_response(self, response):
        response = response.strip().replace("```json", "```")

        if response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()
            
        response = response.replace('{}', '')
        
        # print(response)
        data = json.loads(response)
        # print(data['function'])
        # print(type(data))

        # for key, value in response_dict.items():
        #     if "function" not in value or "args" not in value or "reply" not in value:
        #         print("Invalid response")

        return data

    def execute(self, prompt):
        rendered_prompt = self.render(prompt)
        response = self.llm.inference(rendered_prompt)
        valid_response = self.validate_response(response)

        while not valid_response:
            print("Looks like there is some problem with the agent, trying again....\n")
            return self.execute(prompt)

        return valid_response
