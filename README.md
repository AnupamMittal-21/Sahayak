# Sahayak - Your Satisfaction, Our Priority.

---


## Overview
`Sahayak` : Virtual Customer Service is a web-based application designed to streamline customer support for `Amazon`. It replaces traditional chatbots by taking user input through voice and providing accurate responses based on the query. With support for multiple languages, it offers a simple and efficient way to help customers around the world.

#### Youtube Video Link: https://youtu.be/kjU2W9N35rs
#### Website Link: https://vcs-hackon-kohl.vercel.app/
#### About us Link: https://vcs-about-us.vercel.app/
#### PPT Link:https://drive.google.com/file/d/1qKQ3IkfksyHJlZvpb4gtmIOX0ZWIVr_x/view?usp=sharing
## Key Features

### 1. Automated Voice Call Assistant
Our application allows users to ask queries directly through voice input instead of typing, providing a more natural and efficient interaction compared to traditional chatbots.

![Screenshot (384)](https://github.com/Tushar-022/vcsHackon/assets/100035802/8089ce9d-80b8-42b9-a0bf-b3d24ec1518e)

### 2. Multilingual Support
Users can receive assistance in their native language simply by changing the language preference, making the service accessible to a global audience.

![image](https://github.com/Tushar-022/vcsHackon/assets/100035802/e5d25a1f-f7f3-4db6-b762-081f23b12c50)


### 3. Category-Based Queries
Users can quickly get answers by selecting a relevant category on the main page. Categories include AWS support, online retail, refund requests, Prime-related queries, and general inquiries.

![image](https://github.com/Tushar-022/vcsHackon/assets/100035802/6f7f0ec7-5f83-498b-ba52-c01398abcb2f)


### 4. Contextual Responses
Users can ask questions related to previous queries during the same call. They can also seek clarification on responses provided by our AI voice assistant, ensuring comprehensive and relevant answers.

### 5. Accent Adaptation
Our model offers different language accents based on user preference, enhancing the clarity and understanding of the responses.

### 6. Sentiment Annalysis
Our model generates responses based on the user's query, taking into account the user's current mood and sentiment.

## Architecture


![Architecture 1](https://github.com/Tushar-022/vcsHackon/assets/100035802/dadcf169-5c79-4bbd-996d-5d95c57faf77)




## Folder Structure

This project is divided into two main parts: the frontend and the backend.

### Frontend

The frontend is developed using `ReactJS` and `Redux Toolkit`. It is structured as follows:

![image](https://github.com/Tushar-022/vcsHackon/assets/100035802/d31bb650-2cf9-467d-bc2f-fab743ecba59)



### Backend

The backend is developed using Python with FastAPI. It handles the API endpoints, voice processing, and response generation. The structure is as follows:

![WhatsApp Image 2024-06-21 at 00 26 52_49a41884](https://github.com/Tushar-022/vcsHackon/assets/100035802/ed48c412-adc4-425c-9af5-215cb1806a29)

**Key Features:**

1. **Voice to Text Conversion and Sentiment Analysis:**  
   Utilizes OpenAI's Whisper for converting user voice input into text and analyzing sentiment to understand the user's query context.

2. **Query Similarity Search:**  
   Compares the current user query with previous queries to find the top similar ones using similarity search algorithms.

3. **Top K Similar Queries:**  
   Retrieves the top K similar queries based on the similarity score to find the most relevant past interactions.

4. **Integration with LLM Model:**  
   Fetches answers from a service database for the top similar queries and uses a Large Language Model (LLM) to generate responses.

5. **Text to Audio Conversion:**  
   Uses Amazon Polly to convert the text response into audio, delivering it based on the user's language and accent preference.

## Getting Started with Frontend
Follow these steps to set up and run the frontend of the project:

### Step 1: Clone the Repository

Clone the project repository to your local machine. Use the following command in your terminal:
```sh
 git clone https://github.com/Tushar-022/vcsHackon/tree/master/frontend.git
```
### Step 2: Navigate to the Project Directory
 ```sh
   cd hackon
   ```
### Step 3: Install the Dependencies
 ```sh
   npm install
   ```
### Step 4: Create .env file

Create a .env file in the root directory of the frontend project and add the following environment variables:
```sh
REACT_APP_API_KEY=your-api-key
REACT_APP_AUTH_DOMAIN=your-auth-domain
REACT_APP_PROJECT_ID=your-project-id
REACT_APP_STORAGE_BUCKET=your-storage-bucket
REACT_APP_MESSAGING_SENDER_ID=your-messaging-sender-id
REACT_APP_APP_ID=your-app-id
REACT_APP_MEASUREMENT_ID=your-measurement-id
REACT_APP_EMAIL_CONFIRMATION_REDIRECT=your-email-confirmation-redirect
FAST_REFRESH=true
```

### Step 5: Start the Development Server
Finally, start the development server by running:
```sh
   npm start
```
This command will start the application and open it in your default web browser at http://localhost:3000.

## Getting Started with Backend
Follow these steps to set up and run the backend of the project:

### Step 1: Clone the Repository

Clone the project repository to your local machine. Use the following command in your terminal:
```sh
 git clone https://github.com/AnupamMittal-21/HackOn.git
```
### Step 2: Navigate to the Project Directory
 ```sh
   cd vcsHackon/backend
   ```
### Step 3: Set Up a Virtual Environment
Setting up a virtual environment helps to isolate the project dependencies from your global Python environment:
 ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
### Step 4: Install the Required Dependencies

Install all the necessary dependencies listed in the requirements.txt file:
```sh
pip install -r requirements.txt
```

### Step 5: Run the Main Application
Finally, start the development server by running:
```sh
   python main.py
```

## Technologies Used
- React.js
- Redux Toolkit
- react-media-recorder
- react-formik
- Firebase
- Python
- FastAPI
- Whisper OpenAI (voice-to-text conversion and sentiment analysis)
- LLM (Large Language Model, for natural language processing)
- Amazon Polly (text-to-audio conversion)
- Chroma DB (used for embeddings or related functionalities)

## Website Images
### SignUp & SignIn 
![image](https://github.com/Tushar-022/vcsHackon/assets/100035802/01c2195c-8a1f-4625-9b87-e9057f79d35b)
![image](https://github.com/Tushar-022/vcsHackon/assets/100035802/1970e99a-b830-4926-91b2-5d2529940173)
### Home Page
![image](https://github.com/Tushar-022/vcsHackon/assets/100035802/360dd9c0-833a-4e5f-b560-6b1bba9712bf)
### Caller Service
![image](https://github.com/Tushar-022/vcsHackon/assets/100035802/fe6eddc4-c884-4a30-a533-5d8a06336b86)

### Our Services
![image](https://github.com/Tushar-022/vcsHackon/assets/100035802/92ccb3a6-d069-412c-90ac-9f878725f246)
### FAQs
![image](https://github.com/Tushar-022/vcsHackon/assets/100035802/1130f318-c1a7-4eb1-ba3d-b7455e84fec2)

### Admin Dashboard
![image](https://github.com/Tushar-022/vcsHackon/assets/100035802/356c2c65-9fe0-437b-b3cb-e90f0d298274)

### About Us
![image](https://github.com/Tushar-022/vcsHackon/assets/96460114/a353bdd1-6a50-41af-a3bd-7494804858c8)
![image](https://github.com/Tushar-022/vcsHackon/assets/96460114/63437f53-84bc-403f-a3ed-8c6ea6acb00a)




## Future Scope
In the future, we plan to integrate video solutions within our application. Users will be able to access video tutorials related to their queries. They can pause the video at any point and ask the virtual assistant about specific steps being implemented at that timestamp. Here’s how it will work:

- **Video Playback and Interaction**: Users can view instructional videos relevant to their queries within the application.
  
- **Timestamp Interaction**: Users can pause the video and ask the virtual assistant questions about the specific steps demonstrated at that moment.
  
- **Visual and Text Integration**: Implement image and video recognition capabilities to handle customer queries that involve visual data.
  
- **Enhanced Personalization**: Improve personalization algorithms by incorporating machine learning techniques that adapt to user preferences and behaviors in real-time.

## Conclusion
Sahayak, developed by Team Dynamo, enhances customer support through state-of-the-art AI and NLP technologies. It addresses current challenges and paves the way for future innovations in virtual customer service.
## About Team
For more information about our team members, please visit our LinkedIn profiles:

- [Sujal Singh](https://www.linkedin.com/in/sujal-singh-4a0b49223/)
- [Anupam Mittal](https://www.linkedin.com/in/anupam-mittal-702534223/)
- [Tushar Khandelwal](https://www.linkedin.com/in/tushar-khandelwal-58522722b/)
- [Apoorv Yash](https://www.linkedin.com/in/apoorv-yash-75b130230/)
---
