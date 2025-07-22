import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_default_device("cpu")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)


def phrase_generator(phrase: str) -> str:
    transform_task = f'Make a joke or meme out of the phrase "{phrase}". This joke or meme should be no longer than 10 words.'
    inputs = tokenizer(transform_task, return_tensors="pt", return_attention_mask=False)
    outputs = model.generate(**inputs, max_length=200)
    text = tokenizer.batch_decode(outputs)[0]
    return text.replace(transform_task, '').replace(f'## INPUT\n{phrase}\n##OUTPUT', '').replace("\n", "").replace("<|endoftext|>", "").strip()

