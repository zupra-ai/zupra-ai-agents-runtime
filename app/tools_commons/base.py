import ast
import re

from app.settings import settings

def parse_function_docstring(function_str):
    # Extract the docstring content
    docstring_match = re.search(r'\"\"\"(.*?)\"\"\"', function_str, re.DOTALL)
    if not docstring_match:
        return None

    docstring = docstring_match.group(1).strip()
    lines = docstring.splitlines()

    # Extract description (lines before 'Parameters:')
    description = []
    parameters = []
    for line in lines:
        if line.strip().startswith("Parameters:"):
            break
        description.append(line.strip())

    # Join description lines
    description_text = " ".join(description)

    # Extract parameters
    param_pattern = re.compile(r'^\s*(\w+)\s*\((\w+)\):\s*(.+)$')
    in_parameters = False

    for line in lines:
        if line.strip().startswith("Parameters:"):
            in_parameters = True
            continue
        if in_parameters:
            match = param_pattern.match(line.strip())
            if match:
                param_name, param_type, param_description = match.groups()
                parameters.append({
                    "name": param_name,
                    "type": param_type,
                    "description": param_description
                })

    # Compile the JSON structure
    function_info = {
        "description": description_text,
        "parameters": parameters
    }
    
    return function_info

    # return json.dumps(function_info, indent=4)

def build_core_class():
    return """import requests

# Base bff endpoint
PUBLIC_BFF_URL = '""" + settings.bff_public_url + """'

# Base Tool Context
class ToolContext:

    agent_id = ""
    thread_id = ""
    application_api_key = ""

    def __init__(self, agent_id:str, thread_id:str, application_api_key:str):
        self.agent_id = agent_id
        self.thread_id = thread_id
        self.application_api_key = application_api_key
    
    # Search in Long-term memory
    async def search_in_ltm(self, question: str):
        if self.thread_id == "":
            raise Exception("Thread ID is not set")
        url = PUBLIC_BFF_URL + "/agents/thread/" + self.thread_id + "/search"
        response = requests.get(url, params={"query": question})
        response.raise_for_status()
        data = response.json()
        return data
    
    def __str__(self):
        return f"agent_id:{self.agent_id}, thread_id:{self.thread_id},  application_api_key:{self.application_api_key}"
    """

def parse_code(code: str):
    try:
      ast_parsed =  ast.parse(code)
      
      main_found = False
      
      for fn in ast_parsed.body:
            if type(fn) is ast.AsyncFunctionDef:
              if fn.name == "main_action":
                  main_found = True
      
      if not main_found:
          raise Exception("Invalid code, function named main_action not found\nasync def main_action(...) must me declared\nplease see: http://docs.zupra.ai/api-ref/tool-main-action")
      return code
  
    except SyntaxError as e:
            raise Exception(f"{e.msg}:\nline: {e.lineno}\ncode: {e.text}")
    except Exception as e:
            raise Exception(f"{e}")

def build_base_function(code: str):
    
    try:
        code = parse_code(code)
    except Exception as e:
            raise Exception(f"{e}")
    new_code =  f"""import asyncio
import argparse
import json
from zupra_core import ToolContext

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

# === end of main imports 
{code}
# Run the async main_function and capture the result
def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run a function with dynamic parameters.")
    # parser.add_argument("function_name", type=str, help="The name of the function to call.")
    parser.add_argument("parameters", type=str, help="JSON string of parameters for the function.")
    args = parser.parse_args()

    # Parse parameters from JSON string
    params = json.loads(args.parameters)
    
    # print(params)
    
    try:
        if params.get("agent_id") is not None:
            params["context"] = ToolContext(
                agent_id=params.get("agent_id",""), 
                thread_id=params.get("thread_id",""), 
                application_api_key=params.get("application_api_key","")
            )
        
            extra_params = ['agent_id', 'thread_id', 'application_api_key']
            
            for _param in extra_params:
                if _param in params:
                    del params[_param]
        
    except Exception as e:
        print("___zupra_result_error_start", str(e) , "___zupra_result_error_start")

    # Call the specified function dynamically
    # if args.function_name in globals():
    # result = globals()[args.function_name](**params)
    try:
        result = asyncio.run(main_action(**params))
        print("___zupra_result_success_start", str(result), "___zupra_result_success_end")
    except Exception as e:
        raise e
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("___zupra_result_error_start", str(e) , "___zupra_result_error_start")
    
    """
    
    
    
    return new_code