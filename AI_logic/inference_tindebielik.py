from unsloth import FastLanguageModel
import os


current_dir = os.path.dirname(os.path.realpath(__file__))
with open(f'{current_dir}/prompts/writer_tindebielik.prompt', 'r') as file:
    prompt_template = file.read()

parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
model, tokenizer = FastLanguageModel.from_pretrained(f"{parent_dir}/tindebielik_lora")


def inference_tindebielik(messages, rule):
    prompt = prompt_template.format(tindebielik_rule = rule, messages = messages)
    prompt_chat_template = [{"role": "user", "content": prompt}]
    prompt = tokenizer.apply_chat_template(prompt_chat_template, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=300, use_cache=True, eos_token_id=tokenizer.eos_token_id)
    # returning generated output only
    response = tokenizer.batch_decode(outputs[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True)[0]
    messages = eval(response)
    return messages


if __name__ == "__main__":
    rule = "Kontynuuj flirtowanie."
    messages = """You: A co do koloru... hmmm... Czy to jest fiolet? Nie, może zielony? A może jesteś tajemnicza i nie masz ulubionego koloru? 🤔
You: No więc, opowiedz mi swoją historię życia, szczególnie te zapierające dech w piersiach, a może zaczniemy od ulubionego koloru? 😏
Girl: Czasem lubię irytować 😜
Girl: A kolor to czarny
Girl: Historia życia nudna, ale kiedyś dostałam udaru słonecznego XD
Girl: Teraz Ty 😂"""

    print(inference_tindebielik(messages, rule))
