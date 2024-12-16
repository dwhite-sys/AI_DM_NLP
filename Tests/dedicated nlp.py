import ollama
import spacy
from Modules.simplify import clear

nlp = spacy.load("en_core_web_sm")
clear()


text = 'I hit the mailbox with the branch'

# *Basic* action matching, have a failsafe

def process_relation(relationships, verb, source=None, source_type=None):
    if verb not in relationships.keys():
        relationships[verb] = {'instigator':'','target':''}
    else:
        if source:
            relationships[verb][source_type] = source

def process_text(text):
    process = nlp(text)
    relationships = {}
    for token in process:
        if token.dep_ == 'ROOT' or token.dep_ == 'xcomp':
            process_relation(relationships, token.text)
        elif token.dep_ == 'dobj':
            if token.head.dep_ == 'xcomp':
                for suspect in process:
                    if suspect.dep_ == 'dobj' and suspect.head == token.head.head:
                        process_relation(relationships, token.head.text, token.text, 'target')
                        process_relation(relationships, token.head.text, suspect.text, 'instigator')
            else:
                process_relation(relationships, token.head.text, token.text, 'target')
        elif token.dep_ == 'prep':
            for dependent in process:
                if dependent.head.text == token.text:
                    process_relation(relationships, token.head.text, dependent.text, 'instigator')
        elif token.dep_ == 'nsubj':
            process_relation(relationships, token.head.text, token.text, 'instigator')
    commands = []
    
    for i in relationships:
        if relationships[i]['instigator'] != '':
            commands.append(f'{relationships[i]['instigator']}:{i}:{relationships[i]['target']}')
        else:
            commands.append(f'{i}:{relationships[i]['target']}')
    return commands

while True:
    user_input = input('> ')
    commands = process_text(user_input)
    print(commands)