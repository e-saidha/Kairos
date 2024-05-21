import os
from langchain_community.chat_models import ChatCohere
from langchain_core.output_parsers import StrOutputParser
import google.generativeai as genai
import replicate
import asyncio
import nest_asyncio
class LLM:
    def __init__(self, base_model) -> None:
        self.base_model = base_model

        if base_model == "Arctic-Instruct":
            # os.environ["REPLICATE_API_KEY"] = api_key
            # self.model = replicate.GenerativeModel("arctic-instruct")
            self.model = "snowflake/snowflake-arctic-instruct"   
            # os.environ["REPLICATE_API_KEY"] = api_key
            api_key = os.environ.get("REPLICATE_API_KEY")
                     
        elif base_model == "Gemini-Pro":
            os.environ["GOOGLE_API_KEY"] = api_key
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            self.model = genai.GenerativeModel("gemini-pro")

    def inference(self, prompts):
        if self.base_model == "Arctic-Instruct":
            response = ""  
            for event in replicate.stream(
                self.model,
                input={"prompt": prompts}
            ):
                if event.data:  # Check if the event has non-empty data
                    response += event.data
            
            # response = response.rstrip('{}')
            # print(response)  
            return response
        
        elif self.base_model == "Gemini-Pro":
            response = self.model.generate_content(prompt).text
        # elif self.base_model == "Cohere":
            # chain = self.model | StrOutputParser()
            # response = chain.invoke(prompt)
            return response


# USAGE
# LLM("Arctic-Instruct").inference("""
#                                  hello how are you?
#                                  """)
