import openai
import os


def get_response_from_llm(user_query, sentiment, previous_queries, previous_responses,
                          service_database_answers, service_database_questions, language):
    # Combine the input data into a structured format
    input_data = f"""
    Current Query: {user_query}
    User Sentiment: {sentiment}
    Language: {language}

    NOTE THAT: Write the response in the given language only.
    If the user query is in English, then the response should be in English only.

    Previous Queries and Responses:
    """
    for i, (query, response) in enumerate(zip(previous_queries, previous_responses)):
        input_data += f"\nPrevious Query {i + 1}: {query}\nPrevious Response {i + 1}: {response}\n"

    input_data += "\nService Database Questions and Answers:"
    for i, (question, answer) in enumerate(zip(service_database_questions, service_database_answers)):
        input_data += f"\nService Question {i + 1}: {question}\nService Answer {i + 1}: {answer}\n"

    input_data += """Please provide a detailed response in a step-by-step format, considering the sentiment of the 
    user. The response should adjust the text to reflect the sentiment so that it can be spoken using Amazon Polly. 
    Use the rule-based questions and answers to frame your response primarily. If the query is not related to 
    customer or Amazon-related matters, respond with "Please ask again or contact support for further assistance." 
    Ensure the response is concise enough to be spoken within 40 seconds, and do not end the conversation abruptly."""

    try:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response_llm = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_data}
            ],
            max_tokens=300,  # Adjust the token limit to ensure conciseness
            temperature=0.5
        )

        # Extract and print the response
        answer = response_llm.choices[0].message['content'].strip()
        print(answer)

        return answer
    except Exception as e:
        print(f"Some Error occurred while getting response from LLM : {e}")
        return ""
