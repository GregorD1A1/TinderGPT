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
    outputs = model.generate(**inputs, max_new_tokens=300, use_cache=True, eos_token_id=tokenizer.eos_token_id)#, temperature=0.5, do_sample=True)
    # returning generated output only
    response = tokenizer.batch_decode(outputs[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True)[0]
    messages = eval(response)
    return messages


if __name__ == "__main__":
    rule = "Kontynuuj flirtowanie."
    messages1 = """You: Cześć moja słodka dziewczyno
You: Urocze oczka ma Twój kocioł
You: Budujemy raziem hodowlę kotów i żyjemy resztę życia razem z naszą puchatą rodziną?
Girl: Cześć Grzegorz!
Girl: A dzięki, to kicia o imieniu  Mała
Girl: Hah no niezły pomysł 😀
Girl: Na pewno było by ciekawie
Girl: Ale Super ta Twoja fota profilowa"""
    messages2 = """You: Hej Nicol, to Ty ratujesz pieski? 🐶 Może byś się przydała mojemu ego - też trochę chore...😅 Ale uwaga, jestem bardziej złośliwy niż każdy york na świecie. 🤭
Girl: Te świnki też wyglądają kusząco
Girl: A jesteś równie niezniszczalny co york?
You: Nie, no daj spokój, gdzie mi z yorkami się równać
You: Zresztą jakbym chciał sobie nowego yorka kupić, musiałbym do Ameryki jechać, co nie?
Girl: Racja
Girl: Dlaczego chore ego?
Girl: Co mu dolega?
"""

    print(inference_tindebielik(messages2, rule))
