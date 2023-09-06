import gradio as gr
import requests
import json
import os

api_url = os.getenv("PROXY_API_URL")
#api_url = "http://localhost:5000/dialogue"


def use_requests(api_url,user_input,url,version,key,engine,tokens):
    apimessagerequest  = {}
    azure_headers  =  {}
    azure_headers["OPENAI_API_BASE"] = url
    azure_headers["OPENAI_API_VERSION"] = version
    azure_headers["OPENAI_API_KEY"] = key
    azure_headers["OPENAI_DEPLOYMENT_NAME"] = engine
    azure_headers["OPENAI_API_TOKENS"] = tokens
   
    apimessagerequest['headers'] = azure_headers
    apimessagerequest['message'] = user_input
    print("********************")
    print(apimessagerequest)
    print("********************")
    
    apimessageresponse = requests.post(api_url, json = apimessagerequest)
    json_response = json.loads(apimessageresponse.text)
    completion = json_response['answer']
    
    return completion



def input_display(message, history,url,version,key,engine,tokens):
    response = use_requests(api_url,message,url,version,key,engine,tokens)
    return response

# demo = gr.ChatInterface(input_display)

demo = gr.ChatInterface(
    input_display,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Discussion start here ...", container=False, scale=7),
    title="Passenger Journey Assistant",
    description="Ask PJA any question",
    theme="soft",
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
    additional_inputs=[
                            gr.Textbox("https://openai-sandbox-gs.openai.azure.com", label="OPENAI_API_BASE"), 
                            gr.Textbox("2023-05-15", label="OPENAI_API_VERSION"),
                            gr.Textbox("Your secret here", label="OPENAI_API_KEY"),
                            gr.Textbox("gpt35-turbo-deployment", label="OPENAI_DEPLOYMENT_NAME"),
                            gr.Slider(10, 100)
                        ]
    )

demo.launch()


