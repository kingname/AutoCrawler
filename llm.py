import os
from zhipuai import ZhipuAI


class LLM:
    def __init__(self):
        api_key = os.getenv('API_KEY')
        self.client = ZhipuAI(api_key=api_key)

    def text_chat(self, msgs):
        response = self.client.chat.completions.create(
            model='glm-4-plus',
            messages=msgs,
            temperature=0,
        )
        return response.choices[0].message.content

    def tool_call(self, msgs, tools, tool_choice='auto'):
        response = self.client.chat.completions.create(
            model='glm-4-plus',
            messages=msgs,
            temperature=0.1,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response.choices[0].message.content
