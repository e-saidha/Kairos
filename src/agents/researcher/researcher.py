import json

from jinja2 import Environment, BaseLoader

from src.llm import LLM


researcher_prompt = open("src/agents/researcher/prompt.jinja2").read().strip()


class Researcher:
    def __init__(self, base_model):
        self.llm = LLM(base_model)

    def render(self, step_by_step_plan, contexutal_keywords):
        env = Environment(loader=BaseLoader())
        template = env.from_string(researcher_prompt)
        return template.render(
            step_by_step_plan=step_by_step_plan, contexutal_keywords=contexutal_keywords
        )

    def validate_response(self, response):
        # response = response.strip().replace("```json", "```")
        # # print(response)
        # if response.startswith("```") and response.endswith("```"):
        #     response = response[3:-3].strip()
        # # print(response)
        
        # response = response.replace('{}', '')
        # response = json.loads(response)
        # # print(response)

        
        # response = {k.replace("\\", ""): v for k, v in response.items()}
        # # print(response)
        response = response.strip().replace("```json", "```")

        if response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()
            
        response = response.replace('{}', '')
        
        print("response from researcher",response)
        data = json.loads(response)
        # print(data['function'])
        # print(type(data))

        # for key, value in response_dict.items():
        #     if "function" not in value or "args" not in value or "reply" not in value:
        #         print("Invalid response")

        print("data",data)
        return data
    
        
        if "queries" not in response and "ask_user" not in response:
            return False
        else:
            return {"queries": response["queries"], "ask_user": response["ask_user"]}

    def execute(self, step_by_step_plan, contextual_keywords):
        contextual_keywords = ", ".join(
            map(lambda k: k.capitalize(), contextual_keywords)
        )
        prompt = self.render(step_by_step_plan, contextual_keywords)

        response = self.llm.inference(prompt)

        # print("from researcher", response)
        valid_response = self.validate_response(response)
        print("from researcher valid", valid_response)
        while not valid_response:
            print("Invalid response from the researcher agent, trying again...")
            return self.execute(step_by_step_plan, contextual_keywords)

        return valid_response