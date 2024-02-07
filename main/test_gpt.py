import time

from openai import OpenAI

client = OpenAI(api_key='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')


def gpt_request(text):
    time_start = time.time()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"Выдели основные плюсы и минусы по отзывам, представленные в тексте, и сформулируй ответ в "
                        f"форме структурированного списка, в нейтральной эмоциональной огласке, в ответе должны быть "
                        f"только пункты 'плюсы' и 'минусы' и никакого друго текста. Если есть повторяющиеся по смыслу "
                        f"пункты, то оставь только один. Текст: {text}"},
        ]
    )
    print(time.time() - time_start)

    return completion.choices[0].message.content
