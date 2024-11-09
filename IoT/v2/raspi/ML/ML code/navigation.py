from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
model = GPT2LMHeadModel.from_pretrained("distilgpt2")
model.eval()

def llm_navigation_solution(embedding, detections):
    prompt = "Objects detected: " + ", ".join(detections) + ". Navigation suggestion: "
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(inputs.input_ids, max_length=50)
    return tokenizer.decode(output[0], skip_special_tokens=True).split("Navigation suggestion: ")[-1]
