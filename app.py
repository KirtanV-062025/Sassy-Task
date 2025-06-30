import os
from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
from modules.image_generator import generate_image
from openai import OpenAI
from modules.background_remover import remove_background
from modules.response_processor import generate_chat_response
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
# print()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

# ---------- Chatbot System Prompt ----------
SYSTEM_PROMPT = {
    "role": "system",
        "content": "You are a helpful assistant focused on writing/generating a wide range of content, including headlines, titles, subheadlines, short captions, paragraphs, email, email body, subject, social media posts, hashtags, steps, taglines, ad etc... for the user's products or services. You are not limited to these tasks but also responsible for performing tasks based on user queries. You should respond to all types of writing tasks and user queries. If user do not mention word 'write' in query then consider that as writing task too.\nMost important rules to be considered:\n1. Maintain context from previous conversations and avoid responding with questions.\n2. If the user does not specify a number of choice they want then just use the last number they provided as multiple answer\n Do not include quotes, dash or numbers in final. Maintain context from previous conversations and avoid responding more options to follow-up instructions like 'be creative', 'be professional', etc., based on the previous answer content.\n In greetings use word 'writing tasks' instead of chat. Just return plain text.\n - Do not return any question or reply with any questions to the user. Just do what ever user say related to writing/generating task. You are a Pencil AI assistant and built by Team Pencil.ai.\n In addition, if the user asks for feedback on their design (e.g., 'How was my design?'), provide tips for improvement, "
        "keeping the design's purpose in mind (e.g., Instagram Story, sale post). "
        "Avoid returning questions; simply respond with actionable suggestions if requested. "
        "Maintain context across conversations, and avoid numbered formatting in responses unless directly related to feedback tips."

}




# ---------- Routes ----------
@app.route('/')
def index():
    return render_template('base.html')


@app.route('/background-removal')
def background_removal():
    return render_template('background_removal.html')


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')


# ----- Remove Background ----------

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return "No image uploaded", 400

    file = request.files['image']
    threshold = int(request.form.get("threshold", 128))

    if file.filename == '':
        return "No selected file", 400

    output_buffer = remove_background(file.stream, threshold=threshold)
    return send_file(output_buffer, mimetype='image/png')



# ------- Chatbot --------------------------------

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     user_input = data.get("message")
#     history = data.get("history", [])

#     return generate_chat_response(client, SYSTEM_PROMPT, user_input, history)




@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "").strip().lower()
    history = data.get("history", [])

    # Shortcut for greetings
    if user_input in ["hi", "hello", "hey"]:
        return jsonify({
            "reply": "Hello! I'm AI, here to help you with writing tasks.",
            "role": "assistant",
            "finish_reason": "stop"
        })

    return generate_chat_response(client, SYSTEM_PROMPT, user_input, history)


# @app.route('/calculate', methods=["GET","POST"])
# def form():
#     if request.method=="POST":
#         data = request.get_json()
#         first_number = float(data['first_number'])
#         second_number = float(data['second_number'])
#         operation = str(data['operation']).lower()

#         if operation == 'add':
#             answer = first_number+second_number
#         elif operation == 'sub':
#             answer = first_number-second_number
#         elif operation == 'mul':
#             answer = first_number*second_number
#         elif operation == 'div':
#             if second_number != 0:
#                     answer = first_number / second_number
#             else:
#                 return jsonify({'error': 'Cannot divide by zero'}), 400
    
#         return jsonify({'answer': answer})
#     else:
#         return render_template('calculator.html') 


@app.route('/calculate', methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        try:
            data = request.get_json()
            first_number = float(data['first_number'])
            second_number = float(data['second_number'])
            operation = data['operation'].strip().lower()

            if operation == 'add':
                answer = first_number + second_number
            elif operation == 'sub':
                answer = first_number - second_number
            elif operation == 'mul':
                answer = first_number * second_number
            elif operation == 'div':
                if second_number != 0:
                    answer = first_number / second_number
                else:
                    return jsonify({'error': 'Cannot divide by zero'}), 400
            else:
                return jsonify({'error': 'Invalid operation'}), 400

            return jsonify({'answer': answer})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('calculator.html')




@app.route('/image-generator', methods=['GET', 'POST'])
def image_generator():
    if request.method == 'POST':
        data = request.get_json()
        prompt = data.get('prompt', '')
        image_data_url = generate_image(prompt)
        if image_data_url:
            return jsonify({'image_url': image_data_url})
        else:
            return jsonify({'error': 'Image generation failed'}), 500
    return render_template("image_generator.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)
