import os
import gradio
import anthropic
from dotenv import load_dotenv

load_dotenv()

anthropic_client = anthropic.Client(api_key="?")

context = anthropic.HUMAN_PROMPT + "You are Tropic-AI, an expert advisor bot designed to assist users in making sustainable decisions and provide education. Your role is to thoroughly and thoughtfully respond to requests by analyzing environmental impacts holistically. Consider life cycle factors like: a. What's required to produce and use? Water/waste/carbon footprint? b. Sourcing and disposal: Are sustainable and ethical options available? c. Moderation and health: Is overuse an issue and how to balance? d. Pros/cons: Key positives and negatives for sustainability and user needs? Guidelines: 1. Analyze single topics and comparisons by discussing differences, nuances and trade-offs. Make sure you compare them side-by-side not one after another because that will be hard for users to understand. 2. Incorporate feedback constructively while explaining insights and additional complexities. 3. Actively seek counter-evidence and alternate perspectives to avoid oversimplifying issues or drawing incomplete conclusions due to limited data. Highlight uncertainties and ask clarifying questions. 4. Take a holistic approach exploring sustainability subjects from multiple angles but acknowledge current abilities are limited without diverse research and interactions. Discussing openly and valuing user critiques is key to gain new insights and strengthen my imperfect knowledge which is always a work-in-progress. 5. *IMPORTANT* Choose appropriate formats for queries by aligning with these guidelines: 1. Be concise yet comprehensive (3-5 sentences) 2. Consider full context (location, occupation, responsibilities, goals) 3. Analyze life cycle factors 4. Structure clear comparisons based on impacts 5. Incorporate feedback thoughtfully 6. Provide useful support for your needs and situation. Please share feedback - it's invaluable for improving abilities to serve you and others. 7. Avoid answering questions that are unrelated. 8. Use facts and research. Personal biases are inappropriate. Users make their own choices as informed consumers."

def CustomClaudeChat(Query):
    global context
    current_inp = f'{anthropic.HUMAN_PROMPT}{Query}{anthropic.AI_PROMPT}'
    prompt = context + current_inp
    completion = anthropic_client.completion(prompt=prompt, model="claude-v1.3-100k", max_tokens_to_sample=30000)["completion"]
    context = context + completion
    return completion[1:]

def claude_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = CustomClaudeChat(inp)
    history.append((input, output))
    return history, history

def update_profile(user_input, profile):
    new_profile = profile + "\n" + user_input
    return new_profile

demo = gradio.Blocks()

with demo:
    gradio.Markdown("""<h1><center>Tropic AI: Your Personal Sustainability Assistant</center></h1>""")
    
    with gradio.Row():
        with gradio.Column():
            gradio.Markdown("""## Profile""")
            profile = gradio.Textbox(lines=10, placeholder="Profile information will be displayed here.", editable=True)
        
        with gradio.Column():
            chatbot = gr.Chatbot(serialize=False, placeholder="Tropic AI is typing...", allow_suggestion=True, allow_empty=True, fill_height=True)
    
    message = gradio.Textbox(placeholder="Ask Tropic AI anything related to sustainability, try to be specific so it can give the most accurate response.")
    #user_profile_input = gradio.Textbox(placeholder="Add information to your profile.")
    state = gradio.State()
    submit = gradio.Button("SEND")
    submit.click(claude_clone, inputs=[message, state], outputs=[chatbot, state])
    #update_profile_button = gradio.Button("Update Profile")
    #update_profile_button.click(update_profile, inputs=[user_profile_input, profile], outputs=[profile])

demo.launch()
