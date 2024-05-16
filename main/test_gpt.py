import time

import g4f
from g4f.client import Client
from g4f.Provider import Blackbox
import google.generativeai as genai

client = Client()


def summarization_request(text):
    time_start = time.time()
    # completion = g4f.ChatCompletion.create(
    #     model="gpt-4",
    #     provider=g4f.Provider.Blackbox,
    #     messages=[{"role": "user",
    #                "content": f"Выдели основные плюсы и минусы по отзывам, представленные в тексте, и сформулируй ответ в "
    #                           f"форме структурированного списка, в нейтральной эмоциональной огласке, в ответе должны быть "
    #                           f"только пункты 'плюсы' и 'минусы' и никакого друго текста. Если есть повторяющиеся по смыслу "
    #                           f"пункты, то оставь только один. Текст: {text}"},
    #               ]
    # )

    genai.configure(api_key="AIzaSyADG59_gxwYcEyMItxsNCPHa9zYqFBBqRI")
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content(
        f"Выдели основные плюсы и минусы по отзывам, представленные в тексте, и сформулируй ответ в "
        f"форме структурированного списка, в нейтральной эмоциональной огласке, в ответе должны быть "
        f"только пункты 'плюсы' и 'минусы' и никакого друго текста. Если есть повторяющиеся по смыслу "
        f"пункты, то оставь только один. Текст: {text}")
    print(response.text)

    return response.text
