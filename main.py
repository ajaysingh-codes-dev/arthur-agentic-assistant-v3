from tools.tool_control import TimeStamp
from agents.arthur import LocalArthur
from agents.arthur import Arthur

arthur = Arthur()
local_arthur = LocalArthur()

while True:
    user = input("you: ")
    print(arthur.model(user))
