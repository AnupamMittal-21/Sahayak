from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


def get_sentiment(user_query):
    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("bhadresh-savani/distilbert-base-uncased-emotion")
    model = AutoModelForSequenceClassification.from_pretrained("bhadresh-savani/distilbert-base-uncased-emotion")

    inputs = tokenizer(user_query, return_tensors='pt')

    # Perform emotion detection
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    predicted_emotion = torch.argmax(logits, dim=1)
    # print(predicted_emotion)


    # Map the prediction to emotion labels
    emotion_labels = ["admiration", "amusement", "anger", "annoyance", "approval", "caring",
                      "confusion", "curiosity", "desire", "disappointment", "disapproval",
                      "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
                      "joy", "love", "nervousness", "optimism", "pride", "realization",
                      "relief", "remorse", "sadness", "surprise", "neutral"]
    emotion = emotion_labels[predicted_emotion[0]]
    return emotion


import openai

def sentiment_and_emotion_analysis(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment and emotions of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible. Additionally, identify any specific emotions conveyed (e.g., happiness, sadness, anger, surprise, etc.) and provide brief explanations for each identified emotion."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message['content']

