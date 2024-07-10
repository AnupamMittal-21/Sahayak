import openai


def get_emotion_and_sentiment(text):
    try:
        explanation = text.split('Explanation:')[1].split('\n')[0].strip()
        sentiment = text.split('Sentiment: Sentiment:')[1].split('\n')[0].strip()
    except:
        explanation = ""
        sentiment = "Neutral"

    try:
        emotion_list = text.split('Emotions')[-1].split("\n")[1:-1]
        emotions = []
        for emotion in emotion_list:
            emotions.append(emotion.replace('-', '').strip())

        return explanation, sentiment, emotions
    except Exception as e:
        return "", "Neutral", []


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
                               "also identify the language used in the query"
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
