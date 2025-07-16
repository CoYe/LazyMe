import os

from attrs import define
from openai import OpenAI


@define
class GPTHandler:
    _api_key: str | None = None
    setting: str = ("You are a helpful senior software developer oriented on "
                    "high speed efficient errorless python code. Your responses are "
                    "in json format.")

    @property
    def api_key(self) -> str:
        return self._api_key or os.environ['GPT_API_KEY']

    def ask_gpt(self, prompt, setting):
        client = OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            model="o1",
            #response_format={"type": "json_object"},
            messages=[
                {"role": "system",
                 "content": setting or self.setting},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
