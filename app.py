from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__, static_folder='static')

# Load DialoGPT model and tokenizer
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Chat history to maintain context
chat_history_ids = None

@app.route('/')
def home():
    return render_template('index.html', title="Home")

@app.route('/projects')
def projects():
    return render_template('projects.html', title="Projects")

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact")

# Chatbot route
@app.route('/chat', methods=['POST'])
def chat():
    global chat_history_ids
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({"response": "Please enter a valid input."})

    # Tokenize user input and append to chat history
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    chat_history_ids = input_ids if chat_history_ids is None else torch.cat([chat_history_ids, input_ids], dim=-1)

    # Generate response
    response_ids = model.generate(chat_history_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Update chat history
    chat_history_ids = response_ids
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
