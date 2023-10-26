from transformers import AutoTokenizer, AutoModelForCausalLM, AdamW
import transformers
import torch
import numpy as np
from torch.optim import lr_scheduler
import torch.optim as optim
from accelerate import Accelerator
import os
import json
import jsonlines
import pandas as pd
import gradio as gr


from torch.utils.data import Dataset as Dataset2

from datasets import load_dataset, Dataset, Features, Value

from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model, PeftModel, PeftConfig

title = "🤖응답하라 챗봇🤖"
description = "특정 도메인에 특화된 챗봇"
examples = [["특허란 무엇인가요?"], ["자동차에 관한 특허는 무엇이 있나요?"], ]

def gen(input, history):
    gened = model.generate(
        **tokenizer(
            f"##질문:{input}\n##답변:",
            return_tensors='pt',
            return_token_type_ids=False
        ).to('cuda'),
        max_new_tokens=256,
        no_repeat_ngram_size=6,
        # top_p=0.8,
        temperature=0.7,
        early_stopping=True,
        # num_return_sequences=5,
        do_sample=True,
        eos_token_id=2,
        pad_token_id=2
    )
    # print(gened[0])
    return tokenizer.decode(gened[0])
    
    
model_root = "./LoRA"
model_name = 'poly-pretrained'

# config = LoraConfig(
#     r=8,
#     lora_alpha=32, # 32
#     target_modules=["query_key_value"],
#     lora_dropout=0.05,
#     bias="none",
#     task_type="CAUSAL_LM"
# )

config = PeftConfig.from_pretrained(model_root)
tokenizer = AutoTokenizer.from_pretrained('EleutherAI/polyglot-ko-1.3b')
model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path, device_map={"":0})
# model.eval()
model = PeftModel.from_pretrained(model, model_root)

# model = prepare_model_for_kbit_training(model)
# model = get_peft_model(model, config)

model.eval()
model.config.use_cache = True  # silence the warnings. Please re-enable for inference!

"""
while 1:
    ques = input('질문:')
    if ques == '1': break
    gen(ques)
"""
demo = gr.ChatInterface(
    fn=gen, 
    title=title,
    description=description,
    examples=examples,
    theme="xiaobaiyuan/theme_brief",
    )
    
if __name__ == "__main__":
    demo.launch(share=True)   