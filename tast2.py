from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import wikipedia  # For querying Wikipedia
import requests   # For making HTTP requests
from bs4 import BeautifulSoup  # For web scraping

# Create a chatbot instance
bot = ChatBot('MyBot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(bot)

# Train the chatbot based on the English corpus
trainer.train("chatterbot.corpus.english")

def perform_task(query):
    if 'search wikipedia for' in query.lower():
        search_query = query.lower().replace('search wikipedia for', '')
        try:
            return wikipedia.summary(search_query, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found. Try to be more specific: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return "Sorry, no matching results found on Wikipedia."
    elif 'weather in' in query.lower():
        city = query.lower().replace('weather in', '').strip()
        url = f"https://www.google.com/search?q=weather+in+{city}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_info = soup.find("div", attrs={"id": "wob_dc"}).text.strip()
        return f"Weather in {city.capitalize()}: {weather_info}"
    else:
        return "I'm sorry, I cannot perform that task right now."

# Start interacting with the chatbot
print("Welcome! Type 'exit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    
    bot_response = bot.get_response(user_input)
    if 'search wikipedia for' in user_input.lower() or 'weather in' in user_input.lower():
        bot_response = perform_task(user_input)
    print(f"Bot: {bot_response}")
