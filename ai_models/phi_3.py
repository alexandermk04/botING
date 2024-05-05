import torch
import logging
import time
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from basic_functions import send_message

Logger = logging.getLogger(__name__)

class Phi3:
    model = None
    tokenizer = None
    pipe = None

    def __init__(self):
        torch.random.manual_seed(0)
        self.model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct", 
            device_map="cuda", 
            torch_dtype="auto", 
            trust_remote_code=True, 
        )
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )
    
    def format_message(self, messages):
        return [{"role": "user", "content": message} for message in messages]

    def generate(self, messages):
        generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            "temperature": 0.0,
            "do_sample": False,
        }
        start = time.time()
        output = self.pipe(self.format_messages(messages), **generation_args)
        Logger.info(f"Time taken for generation: {time.time() - start}")
        return output[0]['generated_text']

def prompt_chat(prompt, user_message):
    model = Phi3()
    messages = [prompt, user_message]
    return model.generate(messages)


async def phi_3_answer(recipient, user_message):
    phi_3 = Phi3()
    response = phi_3.generate([user_message])
    await send_message(recipient, response)