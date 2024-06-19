import openai


def sentiment_and_emotion_analysis(transcription):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "As an AI with expertise in language and emotion analysis, your task is to analyze the "
                               "sentiment and emotions of the following text. Please consider the overall tone of the "
                               "discussion, the emotion conveyed by the language used, and the context in which words "
                               "and phrases are used. Indicate whether the sentiment is generally positive, negative, "
                               "or neutral, and provide brief explanations for your analysis where possible. "
                               "Additionally, identify any specific emotions conveyed (e.g., happiness, sadness, "
                               "anger, surprise, etc.) and provide brief explanations for each identified emotion, "
                               "also identify the language used in the query"
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response.choices[0].message['content']

    except openai.error.OpenAIError as e:
        return {"Error": f"OpenAI API error: {e}"}

    except Exception as e:
        return {"Error": str(e)}
