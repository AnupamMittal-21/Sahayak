import openai
from dotenv import load_dotenv
import os

load_dotenv()


def get_response_from_llm(user_query, sentiment, previous_queries, previous_responses, previous_sentiments,
                          service_database_answers):
    # Combine the input data into a structured format
    input_data = f"""
    Current Query: {user_query}
    User Sentiment: {sentiment}

    Previous Queries and Responses:
    """

    for i, (query, response) in enumerate(zip(previous_queries, previous_responses)):
        input_data += f"\nPrevious Query {i + 1}: {query}\nPrevious Response {i + 1}: {response}\n Previous Sentiment {i + 1}: {previous_sentiments[i]}\n"

    input_data += "\nService Database Answers:\n"

    for i, answer in enumerate(service_database_answers):
        input_data += f"\nService Answer {i + 1}: {answer}\n"

    input_data += "\nPlease provide a detailed response in a step-by-step format that does not exceed 1 minute of speaking time."

    try:
        # Call the OpenAI API with the prepared input data
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response_llm = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_data}
            ],
            max_tokens=300,  # Adjust the token limit to ensure conciseness
            temperature=0.7
        )

        # Extract and print the response
        answer = response_llm.choices[0].message['content'].strip()
        print(answer)

        return answer
    except Exception as e:
        print(f"Error in getting response from LLM : {e}")
        return ""


# # Example usage:
# user_query = "How do I reset my password?"
# sentiment = "Frustrated"
# previous_queries = ["Why can't I log in?", "How to recover my account?"]
# previous_responses = ["Try resetting your password.", "Follow the account recovery steps."]
# previous_sentiments = ["Frustrated", "happy"]
# service_database_answers = [
#     "To reset your password, go to the login page and click 'Forgot Password'.",
#     "Enter your registered email address to receive a password reset link.",
#     "If you don't receive the email, check your spam folder or contact support."
# ]
#
# response = get_response_from_llm(user_query, sentiment, previous_queries, previous_responses, previous_sentiments,
#                                  service_database_answers)
# print("Generated Response:", response)
