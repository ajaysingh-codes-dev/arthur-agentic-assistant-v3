from agents.arthur import LocalArthur
from agents.arthur import Arthur

class ArthurAssistant:
    def __init__(self):
        self.arthur = Arthur()
        self.local_arthur = LocalArthur()

    def main(self):
        print("Arthur is running...")
        while True:
            user = input("\n You: ").lower()
            if user in ["exit", "quit"]:
                print("GoodBy")
                break
            if not user:
                continue

            response = self.arthur.model(user)
            print(response)
            if "rate limit" in response:
                print("Cloud limit reached. Switching to local model...")
                print("Type (cloud) to switch model")
                while True:
                    user = input("\n You: ").lower()
                    if user in ["exit", "quit"]:
                        print("GoodBy")
                        break
                    if user in ["cloud"]:
                        break
                    if not user:
                        continue

                    response = self.local_arthur.model(user)
                    print(response)



assisten = ArthurAssistant()
assisten.main()