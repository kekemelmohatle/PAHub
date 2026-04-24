from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import Pipeline
from diffusers import StableDiffusionPipeline
import torch
import json
import os
import gradio as gr
import uvicorn
import threading
# Initialize FastAPI
app = FastAPI()
#--- CONFIGURATION & MODELS ---
HISTORY_FILE = "prompt_history.json"
USERS = {"admin": "password123", "kekeletso": "securepass"}

# Check for GPU, otherwise use CPU device = "cuda" if torch.cuda.is_avaible() else "cpu
torch_dtype = torch.float16 if device == "cuda" else torch.float32

# Load Models
text_model = pipeline("text-generation", model="facebook/opt-350m", device=device)
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch_dtype).to(device)

#--- DATA PERSISTENCE ---
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as F:
        prompt_history = json.load(f)
else:
   prompt_history = []

class GenerationRequest(BaseModel):
    task: str
    context: str = ""
    type: str
    username: str
    password: str

  # ---BACKEND LOGIG ---
  def authenticate(username, password):
      return USERS.get(username) == password
  @app.post("/generate")
  def generate(reg: generationRequest):
     if not authenticate(reg.username, reg.password):
        raise HTTPException(status_code=401, detail="Unauthorized")
     if reg.type == "text":
         prompt = f"Marketing task: {reg.task}\ncontext: {reg.context}\nAnswer:"
         output = text_model(prompt, max_length=120, do_sample=True)[0]["generated_text"]
      elif req.type == "image":
           # Guidance scale and steps help with CPU generation speed
           image = pipe(reg.task, height=256, width=256, num_inference_steps=20).images[0]
           image.save("output.png")
           output = "Image generated successfully."
       else:
          output = "Invalid type or Video not supported in this tier."
       entry = {"task": req.task, "context": req.context, "output": output, "type": req.type}
       prompt_history.append(entry)
       with open(HISTORY_FILE, "w") as f:
          json.dump(prompt_history, f, indent=2)
       return {"result": output}

  #--- GRADIO FRONTEND ---
  SERVER_URL = "http://localhost:8000"

 def marketing_ai_ui(task, context, output_type, username, password):
       payload = {
            "task": task,
            "context": context,
            "type": output_type
            "username": username,
            "password": password
       }
       try:
            response = requests.post(f"{SERVER_URL}/generate", json=payload)

            if response.status_code == 200:
                return response.json()["result"]
            else:
                return f"Error:{response.json().get("detail", "authentication failed")}"
       except Exception as e:
           return f"Connection Error: {str(e)}"
with gr.Blocks(theme=gr.themes.soft()) as demo:
    gr.Markdown("# PAHub: AI Marketing Suite")
        with gr.Row():
            user_ input = gr.textbox(label="Username")
            pass_input = gr.Textbox(label="password", type="password", type="password", placeholder="password123")

with gr.Row():
    with gr.Column():
        task = gr.textbox(label="campaign Goal", placeholder="e.g. Social media ads for a new coffee shop")
        context = gr.textbox(label="market context", placeholder="e.g. Trendy area, focus on organic beans")
        output_type = gr.Radio(["text", "image"], label="generate format", value="text")
        btn = gr.Button("generate marketing content", variant="primary")
    with gr.column():
        result = gr.textbox(label="AI output", lines=10)
        btn.click(marketing_ai_ui, inputs=[task, context, output_type, user_input, pass_input], outputs=result)
        gr.Markdown("""---
        ### System Dsclaimer
        *prototype marketing AI for demostration pursoses. Use professional judgement for final campaigns.*""")
  # --- RUNNER ---
  if _name_ =="_main_":
  # start FastAPI in a background thread threading.thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000), daemo=True).start()
  # Start Gradio on the port HUgging Face expects(7860)
  demo.launch(server_name="0.0.0.0", server_port=7860

            


        
