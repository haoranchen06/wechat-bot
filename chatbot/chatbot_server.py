#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2022/9/9 14:33
# @Author: chenhr33733
# @File: chatbot_server.py
# @Software: PyCharm
# @Copyright：Copyright(c) 2022 Hundsun.com, Inc.All Rights Reserved


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
device = torch.device("cuda:0")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
model.to(device)

# Let's chat for 5 lines
for step in range(5):
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(input(">> User:") + tokenizer.eos_token, return_tensors='pt').to(device)

    # append the new user input tokens to the chat history
    # bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens,
    chat_history_ids = model.generate(new_user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # pretty print last ouput tokens from bot
    print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)))
