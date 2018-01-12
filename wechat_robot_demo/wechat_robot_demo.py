# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

# chatbot = ChatBot('myBot')
"""
database:指定所创建的chat bot所使用的数据集是database.json， 如果这个database.json不存在，会自动创建
input_adapter :指定输入和输出终端adapter
output_adapter :输入终端adapter则是打印出chat bot的应答信息
logic_adapter : 
只读模式

ChatterBot是会对每个输入的语句进行学习的。如果想要使得你已经训练过的bot不再继续学习输入的语句，可以通过以下方式进行设置，
x在初始化的时候将read_only设置为true。
"""
chatbot = ChatBot("Norman", read_only=False)

chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.set_trainer(ListTrainer)
chatbot.train(["嗨，渡边君，真喜欢我?","那还用说","那么，可依德我两件事?","三件也依得",])

# 使用中文语料库训练它
chatbot.train("chatterbot.corpus.chinese")
chatbot.train("chatterbot.corpus.english.greetings")
# 使用英文语料库训练它
# chatbot.train("chatterbot.corpus.english")


# 开始对话
while True:
    try:
        print(chatbot.get_response(input(":::")))
    except(KeyboardInterrupt, EOFError, SystemExit):
        break