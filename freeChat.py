import sys, os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))


import pyperclip
from flowlauncher import FlowLauncher
from freeGPT import AsyncClient
from asyncio import run
import datetime
import subprocess

class freeChat(FlowLauncher):
    def query(self, query):
        output = []
        if len(query.strip()) == 0:
            output.append(
                {"Title": "Hi! Lets talk", "IcoPath": "icons/robot.ico"}
            )

        else:
            try:
                ans = run(self.freeGPT(query))
            except Exception:
                output.append(
                    {
                        "Title": "Error: GPT Not Responding",
                        "IcoPath": "icons/error.png",
                    }
                )
                return output

            output.append(
                {
                    "Title": "Click to copy",
                    "SubTitle": f"{ans}",
                    "IcoPath": "icons/copy.png",
                    "JsonRPCAction": {"method": "copy", "parameters": [f"{ans}"]},
                }
            )

            output.append(
                {
                    "Title": "Click to write the answer to a file",
                    "SubTitle": f"{ans}",
                    "IcoPath": "icons/write.png",
                    "JsonRPCAction": {"method": "write_to_file", "parameters": [f"{ans}"]},
                }
            )

            output.append(
                {
                    "Title": "Click to view the story",
                    "SubTitle": f"{ans}",
                    "IcoPath": "icons/history.png",
                    "JsonRPCAction": {"method": "show_to_file", "parameters": [f"{ans}"]},
                }
            )

        return output

    async def freeGPT(self, querry):
        prompt = querry
        resp = await AsyncClient.create_completion("gpt3", prompt)
        return resp

    def show_to_file(text, ans):
        process = subprocess.Popen(r'notepad.exe chat_history.txt')
        process.wait()

    def write_to_file(text, ans):
        with open("chat_history.txt", "a") as file:
            file.write("----------------------Date: {}\n".format(datetime.date.today()))
            file.write("---------------------Time: {}\n".format(datetime.datetime.now().strftime("%H:%M:%S")))
            file.write("\n")
            file.write(ans)
            file.write("\n")

    def copy(self, ans):
        pyperclip.copy(ans)

if __name__ == '__main__':
    freeChat()