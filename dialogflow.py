import os
from google.cloud import dialogflowcx_v3beta1 as dialogflow


class DialogflowCXAgent:
    def __init__(self, project_id, location, agent_id):
        """
        Initialize the Dialogflow CX client.
        
        Args:
            project_id (str): Google Cloud project ID.
            location (str): The location of the agent (e.g., "global", "us-central1").
            agent_id (str): The ID of the Dialogflow CX agent.
        """
        self.project_id = "pizza-delivery-444516"
        self.location = "global"
        self.agent_id = "d34d8823-076f-4bb7-a8ef-a5be5f469f0d"
        self.client = dialogflow.SessionsClient()
        
    def get_session_path(self, session_id):
        """Generate a session path for Dialogflow CX."""
        return f"projects/{self.project_id}/locations/{self.location}/agents/{self.agent_id}/sessions/{session_id}"

    def detect_intent_text(self, session_id, user_input, language_code="en"):
        """
        Send user input to Dialogflow CX and receive a response.
        
        Args:
            session_id (str): Unique identifier for the session (can be a user ID).
            user_input (str): The input text from the user.
            language_code (str): The language of the input text (default is 'en').

        Returns:
            str: The bot's response.
        """
        session_path = self.get_session_path(session_id)
        
        # Configure the request
        text_input = dialogflow.TextInput(text=user_input)
        query_input = dialogflow.QueryInput(text=text_input, language_code=language_code)
        
        try:
            response = self.client.detect_intent(
                request={"session": session_path, "query_input": query_input}
            )
            
            response_messages = response.query_result.response_messages
            bot_responses = [message.text.text[0] for message in response_messages if message.text]
            
            print(f"User Input: {user_input}")
            print(f"Bot Response: {' '.join(bot_responses)}")
            
            return ' '.join(bot_responses)
        
        except Exception as e:
            print(f"Error during detect_intent: {e}")
            return None


if __name__ == "__main__":
    # Replace these variables with your actual Dialogflow CX credentials
    GOOGLE_PROJECT_ID = "pizza-delivery-444516"
    AGENT_ID = "d34d8823-076f-4bb7-a8ef-a5be5f469f0d"
    LOCATION = "global"  # Or "us-central1", "europe-west1", etc.
    SESSION_ID = "user-1234"  # You can use a unique user ID for each session

    # Initialize the Dialogflow CX Agent
    dialogflow_agent = DialogflowCXAgent(
        project_id=GOOGLE_PROJECT_ID,
        location=LOCATION,
        agent_id=AGENT_ID
    )

    print("\n🗣️ Welcome to the AI Chatbot! Type 'exit' to end the chat.\n")

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break
        
        # Send the user's message to Dialogflow and receive a response
        response = dialogflow_agent.detect_intent_text(session_id=SESSION_ID, user_input=user_input)
        
        if response:
            print(f"🤖 Bot: {response}")
        else:
            print("🤖 Bot: Sorry, I didn't understand that.")
