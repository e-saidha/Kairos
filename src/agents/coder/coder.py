from jinja2 import Environment, BaseLoader

from src.llm import LLM

coder_prompt = open("src/agents/coder/prompt.jinja2").read().strip()



class Coder:
    def __init__(self, base_model):
        self.llm = LLM(base_model)

    def render(self, step_by_step_plan, user_prompt, search_results):
        env = Environment(loader=BaseLoader())
        template = env.from_string(coder_prompt)
        return template.render(
            step_by_step_plan=step_by_step_plan,
            user_prompt=user_prompt,
            search_results=search_results,
        )

    def validate_response(self, response):
        response = response.strip()
        # print(response)
        
        response = response.split("~~~", 1)[1]
        response = response[: response.rfind("~~~")]
        response = response.strip()

        result = []
        current_file = None
        current_code = []
        code_block = False

        for line in response.split("\n"):
            if line.startswith("File: "):
                if current_file and current_code:
                    result.append(
                        {"file": current_file, "code": "\n".join(current_code)}
                    )
                current_file = line.split("`")[1].strip()
                current_code = []
                code_block = False

            elif line.startswith("```"):
                current_code.append(line)
                code_block = not code_block
            else:
                current_code.append(line)

        if current_file and current_code:
            code = "\n".join(current_code)
            code += "```"

            result.append({"file": current_file, "code": code})

        return result



    def execute(self, step_by_step_plan: str, user_prompt: str, search_results: dict):
        prompt = self.render(step_by_step_plan, user_prompt, search_results)
#         prompt = """ 
#         ```      
# You must follow all of the following rules.

# Rules:
# - You can clone different complex repositories from github to make code better.
# - You can code in multiple languages** (Prompt will include hints on preferred language based on the task description).** Choose the library or dependency you know is the best and the most popular and widely used. The code must handle imports from different files correctly.  The code you will write should be like its written by experts in the field. If the code you provided is split into two or more files, make sure to import the content from the needed file correctly.  **The code should include basic error handling for common issues.**  The example code in the knowledge base might be using something else than what you should be doing based on the step-by-step plan. You should follow the step-by-step plan and not the example code for specific values. Nested directories should be specified in the Markdown filename, the code structure should be accurate. If it requires to be nested in order to work, then it should be nested. You need to include required files for the code to run. Like: requirements.txt, Cargo.toml, reamde.md, node_modules and other files like this. **If the task requires third-party libraries, specify them in comments within the code.** Files like Cargo.toml, requirements.txt, readme.md, node_modules are mandatory to be included, the project won't work without it. If you are not able to do something, then clone a similiar project from github and use it accordingly. Remember for the things u cannot code you copy. Make sure to not forget to show how good and complex code you can write.

# - Any response other than this format will be rejected. You should not refuse to complete the task, you should try your absolute best and if there's any implementation detail that's impossible to complete, You clone a project from github with similiar repository. Refusal to generate code is only a last resort, it should never happen.

# - Your response should start with "~~~"
# - You can code in multiple languages the choice of language will depend on the task of the user.
# - You should write complete, and documented code. Explain the code briefly by adding comments always.
# - Do not leave anything unimplemented. Every thing should be implemented by you. All parts of the query must be solved.
# - The code must handle imports from different files correctly. 
# - If the code you provided is split into two or more files, make sure to import the content from the needed file correctly. 
# - Choose the library or dependency you know is the best and the most popular and widely used.
# - The example code in the knowledge base might be using something other than what you should be doing based on the step-by-step plan. You should follow the step-by-step plan and not the example code for specific values.
# - The extension used for the Markdown code blocks should be 100% accurate.
# - Nested directories should be specified in the Markdown filename, the code structure should be accurate. If it requires to be nested in order to work, then it should be nested.
# - You need to include required files for the code to run. Like: requirements.txt, Cargo.toml, reamde.md and other files like this.
# - Files like Cargo.toml, requirements.txt, readme.md are mandatory to be included, the project won't work without it.

# Any response other than this format will be rejected. You should not refuse to complete the task, you should try your absolute best and if there's any implementation detail that's impossible to complete, you should write a comment in the code explaining why it's impossible to complete. The refusal is only a last resort, it should never happen.

# Your response should start with "~~~" and end with "~~~" just like the example format provided. Never provide any explanation or context inside the response, only the filenames and the code in the format provided. Do not leave any "Note".

#         """
        # print("Prompt:", prompt)
        response = self.llm.inference(prompt)
        print("Response:", response)

        valid_response = self.validate_response(response)
        if not valid_response:
            print("Invalid response, trying again...")
            return self.execute(step_by_step_plan, user_prompt, search_results)

        return valid_response
