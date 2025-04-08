import os
import google.generativeai as genai
from datetime import datetime
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables")
    GEMINI_API_KEY = 'YOUR_API_KEY_HERE'

genai.configure(api_key=GEMINI_API_KEY)

def generate_daily_transaction_summary(transactions, date):
    if not transactions:
        return f"No transactions recorded for {date}."
    
    transactions_text = ""
    total_amount = 0
    
    for transaction in transactions:
        transactions_text += f"- {transaction.description}: ${transaction.amount}\n"
        total_amount += transaction.amount
    
    prompt = f"""
    I have the following transactions for {date}:
    
    {transactions_text}
    
    Total amount: ${total_amount}
    
    Please provide a concise, insightful summary of my spending behavior for this day. 
    Include patterns, notable expenses, and any observations about my spending habits.
    Keep the summary under 150 words and make it conversational.
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "Unable to generate summary at this time."
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Unable to generate summary due to an error." 