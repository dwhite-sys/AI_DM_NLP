import ollama
import spacy
from Modules.simplify import clear
from Modules.process_text import process_text, NLP
clear()


text = 'I hit the mailbox with the branch'

# *Basic* action matching, have a failsafe
while True:
    user_input = input('> ')
    analysis = NLP(user_input)
    print(process_text(user_input))
    for token in analysis:
        print(f"(Word: {token.text}), (Dep: {token.dep_}), (Head: {token.head.text}), (Head type: {token.head.pos_}) (Grandfather: {token.head.head})")