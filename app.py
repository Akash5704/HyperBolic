import requests
import time
import random
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)

# API Configuration - using environment variables for security
URL = "https://api.hyperbolic.xyz/v1/chat/completions"
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbmlrZXRqYWlzd2FyNDNAZ21haWwuY29tIiwiaWF0IjoxNzUwODc1NDQ4fQ.6KWMtQBb02G28JiSbmmu2a1OH4tYQUA0WtwhBPC24B8"

if not API_KEY:
    logging.error("HYPERBOLIC_API_KEY environment variable not set!")
    exit(1)

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# List of 100 unique questions
questions = [
    "What's the best way to learn programming?",
    "How does quantum computing work?",
    "What are some healthy breakfast ideas?",
    "Can you explain blockchain technology?",
    "What's the weather like on Mars?",
    "How do I improve my photography skills?",
    "What are the benefits of meditation?",
    "How does artificial intelligence work?",
    "What's the history of the internet?",
    "Can you suggest some good books to read?",
    "What's the meaning of life?",
    "How do I make a perfect cup of coffee?",
    "What are the latest space discoveries?",
    "How can I stay motivated to exercise?",
    "What's the future of electric cars?",
    "How do I start a small business?",
    "What are some fun weekend activities?",
    "Can you explain the theory of relativity?",
    "What's the best way to learn a language?",
    "How does the stock market work?",
    "What's the best way to save money?",
    "How do I plan a trip abroad?",
    "What are the effects of climate change?",
    "How does Wi-Fi actually work?",
    "What's the history of video games?",
    "How can I improve my public speaking?",
    "What's the science behind rainbows?",
    "How do I grow indoor plants successfully?",
    "What are the benefits of drinking water?",
    "How does cryptocurrency mining work?",
    "What's the history of chocolate?",
    "How can I reduce stress in my life?",
    "What are some tips for better sleep?",
    "How do solar panels generate electricity?",
    "What's the best way to cook steak?",
    "How does the human brain process memory?",
    "What are some must-visit places in Europe?",
    "How do I start investing in stocks?",
    "What's the difference between viruses and bacteria?",
    "How can I make my home more eco-friendly?",
    "What's the history of the Olympic Games?",
    "How do I train a dog effectively?",
    "What are the benefits of yoga?",
    "How does 3D printing work?",
    "What's the best way to learn guitar?",
    "How do airplanes stay in the air?",
    "What are some creative writing tips?",
    "How does the immune system fight diseases?",
    "What's the future of space travel?",
    "How can I improve my time management?",
    "What's the history of pizza?",
    "How do I create a budget?",
    "What are the benefits of recycling?",
    "How does virtual reality work?",
    "What's the best way to study for exams?",
    "How do I make homemade bread?",
    "What are the causes of global warming?",
    "How does GPS technology work?",
    "What's the history of photography?",
    "How can I boost my creativity?",
    "What are some tips for healthy eating?",
    "How do self-driving cars function?",
    "What's the best way to learn cooking?",
    "How does the moon affect tides?",
    "What are some fun science experiments?",
    "How do I start a podcast?",
    "What's the history of democracy?",
    "How can I improve my drawing skills?",
    "What are the benefits of journaling?",
    "How does nuclear energy work?",
    "What's the best way to plan a party?",
    "How do I maintain a car properly?",
    "What are some tips for traveling cheap?",
    "How does the internet of things work?",
    "What's the history of coffee?",
    "How can I learn to code faster?",
    "What are the benefits of team sports?",
    "How do black holes form?",
    "What's the best way to declutter my home?",
    "How does machine learning differ from AI?",
    "What are some tips for gardening?",
    "How do I make a good first impression?",
    "What's the history of the English language?",
    "How can I stay productive working from home?",
    "What are the benefits of learning history?",
    "How does the human eye see color?",
    "What's the best way to train for a marathon?",
    "How do I start a blog?",
    "What are some unusual animal facts?",
    "How does sound travel through the air?",
    "What's the history of fashion?",
    "How can I improve my negotiation skills?",
    "What are the benefits of mindfulness?",
    "How do I build a simple website?",
    "What's the best way to learn math?",
    "How does evolution work?",
    "What are some tips for reducing waste?",
    "How do I choose a good wine?",
    "What's the future of renewable energy?"
]

# Statistics tracking
stats = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'start_time': datetime.now()
}

def send_chat_request(question, max_retries=3):
    """Send API request with retry logic"""
    data = {
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(URL, headers=HEADERS, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            answer = result['choices'][0]['message']['content']
            stats['successful_requests'] += 1
            return answer
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))  # Exponential backoff
            else:
                stats['failed_requests'] += 1
                return f"Error after {max_retries} attempts: {str(e)}"
        except Exception as e:
            stats['failed_requests'] += 1
            return f"Unexpected error: {str(e)}"

def log_statistics():
    """Log current statistics"""
    uptime = datetime.now() - stats['start_time']
    success_rate = (stats['successful_requests'] / max(stats['total_requests'], 1)) * 100
    
    logging.info(f"=== STATISTICS ===")
    logging.info(f"Uptime: {uptime}")
    logging.info(f"Total requests: {stats['total_requests']}")
    logging.info(f"Successful: {stats['successful_requests']}")
    logging.info(f"Failed: {stats['failed_requests']}")
    logging.info(f"Success rate: {success_rate:.2f}%")
    logging.info(f"==================")

def run_chat_bot():
    """Main bot loop - runs continuously"""
    logging.info("Starting 24/7 automated chat bot...")
    logging.info(f"Total questions available: {len(questions)}")
    
    cycle_count = 0
    
    while True:
        try:
            cycle_count += 1
            logging.info(f"Starting cycle {cycle_count}")
            
            # Create a copy of questions for this cycle
            available_questions = questions.copy()
            random.shuffle(available_questions)  # Randomize order each cycle
            
            for i, question in enumerate(available_questions, 1):
                stats['total_requests'] += 1
                
                logging.info(f"Cycle {cycle_count}, Question {i}/100: {question}")
                answer = send_chat_request(question)
                logging.info(f"Answer received: {answer[:100]}...")  # Log first 100 chars
                
                # Log statistics every 10 questions
                if i % 10 == 0:
                    log_statistics()
                
                # Random delay between 60-120 seconds
                delay = random.uniform(60, 120)
                logging.info(f"Waiting {delay:.1f} seconds before next question...")
                time.sleep(delay)
            
            logging.info(f"Completed cycle {cycle_count}. Starting new cycle...")
            
            # Brief pause between cycles
            time.sleep(300)  # 5 minutes between cycles
            
        except KeyboardInterrupt:
            logging.info("Bot stopped by user")
            break
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {str(e)}")
            logging.info("Waiting 60 seconds before retrying...")
            time.sleep(60)
    
    log_statistics()
    logging.info("Chat bot stopped")

# Health check endpoint for deployment platforms
def health_check():
    """Simple health check function"""
    return {
        'status': 'healthy',
        'uptime': str(datetime.now() - stats['start_time']),
        'total_requests': stats['total_requests'],
        'success_rate': (stats['successful_requests'] / max(stats['total_requests'], 1)) * 100
    }

if __name__ == "__main__":
    run_chat_bot()
