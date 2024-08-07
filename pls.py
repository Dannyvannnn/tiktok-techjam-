from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory 


app = Flask(__name__)
CORS(app)


def load_model():
  
    os.environ["OPENAI_API_KEY"] = ""
    model = ChatOpenAI(model="gpt-3.5-turbo-1106")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a music recommender that recommends music when the user tells you their emotions.You may converse with the user. Only recommend one song",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    chain = prompt | model
    return chain

chatbotreply = load_model()

chat_history = ChatMessageHistory()


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    chat_history.add_user_message(user_message)
    chatbot_response = chatbotreply.invoke(
        {
            "messages": chat_history.messages,
        }
    )
    chat_history.add_ai_message(chatbot_response)
    # Print the response data
    print(chatbot_response.content)
    return jsonify(chatbot_response.content)


if __name__ == "__main__":
    app.run(debug=True)