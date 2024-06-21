import openai


def get_emotion_and_sentiment(text):
    try:
        Sentiment = text.split('Sentiment: Sentiment:')[1].split('\n')[0].strip()
        Emotion = text.split('Emotions ')[-1].split("\n")[1:-1]
        Emotions = []
        for emotion in Emotion:
            Emotions.append(emotion.replace('-', '').strip())

        return Sentiment, Emotions
    except Exception as e:
        return "Neutral", []


def sentiment_and_emotion_analysis(transcription):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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
                               "also identify the language used in the query, in the end send the emotions like a list."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response.choices[0].message['content']

    except Exception as e:
        return {"No sentiment found"}
