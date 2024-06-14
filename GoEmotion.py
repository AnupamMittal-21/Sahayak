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
    print(predicted_emotion)


    # Map the prediction to emotion labels
    emotion_labels = ["admiration", "amusement", "anger", "annoyance", "approval", "caring",
                      "confusion", "curiosity", "desire", "disappointment", "disapproval",
                      "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
                      "joy", "love", "nervousness", "optimism", "pride", "realization",
                      "relief", "remorse", "sadness", "surprise", "neutral"]
    emotion = emotion_labels[predicted_emotion[0]]
    return emotion