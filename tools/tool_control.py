from datetime import datetime, date
import inspect
import pyautogui

class TimeStamp:
    @staticmethod
    def get_datetime():
        """Get current date and time."""
        current_date = date.today().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"Current time: {current_time} | Current_date: {current_date}"
    
class OpenApplication():
    @staticmethod
    def open_app(name: str) -> str:
        print(f"OPEN_APP CALLED -> {name}")
        a = input(f"do you really want to open {name}: ")
        if a == "yes":
            print(f"opening {name}")
            try:
                pyautogui.hotkey("win", "s")
                pyautogui.write(name, interval=0.05)
                pyautogui.press("enter")
                return "app open success"
            except Exception as e:
                return str(e)
        else:
            return "permission deined"
        

class ToolCall(TimeStamp, OpenApplication):
    def __init__(self):
        super().__init__()
        self.tool_list = [self.get_datetime, self.open_app]
        self.tools = {"get_datetime": self.get_datetime,
                      "open_app": self.open_app}

    def execute_tool(self, tool_name: str, args: dict) -> str:
        if tool_name not in self.tools:
            return "Unknown Tool Name! "
        try:
            tool = self.tools[tool_name]
            sig = inspect.signature(tool)
            clean_args = {k: v for k, v in args.items()
                            if k in sig.parameters}
            return tool(**clean_args)
        except Exception as e:
            return f"tool execution error: {e}"
        

if __name__ == "__main__":
    a = TimeStamp()
    print(a.get_datetime())
        