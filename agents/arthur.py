import json
from ollama import chat
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from tools.tool_control import ToolCall

class LocalArthur(ToolCall):

    def __init__(self):
        super().__init__()
        self.assistant = "llama3.2:3b"
        self.memory_path = os.path.join("memory", "local_memory.json")
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    self.messages = json.load(f)
            except Exception as e:
                self.messages = []
        else:
            self.messages = []
        
        if not self.messages:
            sp_path = os.path.join("memory", "system_prompt.txt")
            with open(sp_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()
            self.messages.append({"role":"system",
                                "content":system_prompt})

    def model(self, user_input: str)-> str:
        
        self.messages.append({"role":"user",
                              "content":user_input})
        
        response = chat(model=self.assistant,
                        messages=self.messages)
        
        self.messages.append({"role":"assistant",
                             "content":response.message.content})

        self.manage_memory()
        
        return response.message.content
    
    def save_memory(self):
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=4)


    def manage_memory(self):
        if len(self.messages) > 20:
            self.messages = [self.messages[0]] + self.messages[-19:]
            self.save_memory()
        else :
            self.save_memory()

class Arthur(ToolCall):
    load_dotenv()

    def __init__(self):
        super().__init__()
        self.apis = [os.getenv("MY_API_KEY_1"),
                     os.getenv("MY_API_KEY_2"),
                     os.getenv("MY_API_KEY_3"),
                     os.getenv("MY_API_KEY_4")]
        
        self.index_value = 0
        self.client = genai.Client(api_key=self.apis[self.index_value])
        self.assistant = "gemini-2.5-flash"
        self.chat_history_path = os.path.join("memory","api_model_memory.json")
        try:
            if os.path.exists(self.chat_history_path):
                with open(self.chat_history_path, "r", encoding="utf-8") as f:
                    self.chat_history = json.load(f)
            else:
                self.chat_history = []
        except Exception as e:
            self.chat_history = []

        self.sp_path = os.path.join("memory", "api_arthur_sp.txt")
        if os.path.exists(self.sp_path):
            with open(self.sp_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = ""

        self.config = types.GenerateContentConfig(system_instruction=self.system_prompt,
                                                  tools=self.tool_list)

    def switch_keys(self) -> bool:
        self.index_value += 1
        if self.index_value >= len(self.apis):
            return False
        self.client = genai.Client(api_key=self.apis[self.index_value])
        return True
    
    def model(self, user_input):
        self.chat_history.append({"role":"USER",
                                  "parts":[{"text":user_input}]})
        while True:
            try:
                response = self.client.models.generate_content(
                    model= self.assistant,
                    config=self.config,
                    contents=self.chat_history
                )

                self.chat_history.append({
                    "role":"MODEL",
                    "parts":[{"text": response.text}]
                })
                self.manage_memory()

                return response.text
            
            except Exception as e:
                if "429" in str(e):
                    if self.switch_keys():
                        continue
                    return "All API keys exhausted (rate limit reached)"
                return f"Error {e}"
        
    def save_memory(self):
        with open(self.chat_history_path, "w", encoding="utf-8") as f:
            json.dump(self.chat_history, f, indent=4)
    
    def manage_memory(self):
        try:
            self.chat_history = self.chat_history[-20:]
            self.save_memory()
        except Exception as e:
            return str(e)