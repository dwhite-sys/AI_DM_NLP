import spacy
spacy.prefer_gpu()
NLP = spacy.load("en_core_web_sm")

def process_relation(relationships, verb, source=None, source_type=None):
    if verb not in relationships.keys():
        relationships[verb] = {'instrument':'','target':''}
    if source:
        relationships[verb][source_type] = source
            
def process_text(text):
    process = NLP(text)
    relationships = {}
    for token in process:
        # Check if it's a verb
        if token.dep_ == 'ROOT' or token.dep_ == 'xcomp' or token.dep_ == 'ccomp' or token.dep_ == 'advmod' or token.dep_ == 'conj':
            process_relation(relationships, token.head.text)
            # This would make sure "up" in "pick up" is added or "out" in "take out"
            for suspect in process:
                if suspect.dep_ == 'prt':
                    process_relation(relationships, token.text, suspect.text, 'particle')
        # Check if it's a noun
        elif token.dep_ == 'dobj' or token.dep_ == 'npadvmod':
            if token.head.dep_ == 'xcomp':
                complex = False
                for suspect in process:
                    if suspect.dep_ == 'dobj'or suspect.dep_ == 'nsubjpass':
                        if suspect.head == token.head.head:
                            process_relation(relationships, token.head.text, token.text, 'target')
                            process_relation(relationships, token.head.text, suspect.text, 'instrument')
                            complex = True
            # "I hit the mailbox using the branch"
            elif token.head.dep_ == 'advcl':
                complex = False
                for suspect in process:
                    if suspect.dep_ == 'dobj':
                        if suspect.head == token.head.head:
                            process_relation(relationships, suspect.head.text, token.text, 'instrument')
                            process_relation(relationships, suspect.head.text, suspect.text, 'target')
                            complex = True
                if complex == False:
                    process_relation(relationships, token.head.text, token.text, 'target')
            else:
                process_relation(relationships, token.head.text, token.text, 'target')
        # an example here would be "with the branch", with the preposition "with" being used to tag "branch"
        elif token.dep_ == 'prep':
            for dependent in process:
                if dependent.head.text == token.text:
                    process_relation(relationships, token.head.text, dependent.text, 'instrument')
        # Additional way of processing pobj the same way you do dobj
        elif token.dep_ == 'pobj':
            complex = False
            if token.head.dep_ == 'prep':
                for suspect in process:
                    'nsubjpass'
                    if suspect.dep_ == 'compound' or suspect.dep_ == 'ROOT' and suspect.head == token.head.head:
                        process_relation(relationships, suspect.text, token.text, 'instrument', )
                        complex = True
            else:
                for suspect in process:
                    if suspect.dep_ == 'dobj' and suspect.head == token.head.head:
                        process_relation(relationships, suspect.head.text, suspect.text, 'target')
                        complex = True
                    if complex == False:
                        process_relation(relationships, token.head.text, token.text, 'target')
        elif token.dep_ == 'amod' or token.dep_ == 'compound':
            for suspect in process:
                if suspect.dep_ == 'ROOT':
                    process_relation(relationships, token.text)
                    process_relation(relationships, token.text, suspect.text, 'target')
                


    commands = []
    for i in relationships:
        action = i
        if 'particle' in relationships[i]:
            # action = pick, particle = up -> action = pick up
            action = f'{action} {relationships[i]['particle']}'
        if relationships[i]['instrument'] != '':
            commands.append(f'{relationships[i]['instrument']}:{action}:{relationships[i]['target']}')
        else:
            commands.append(f'{action}:{relationships[i]['target']}')
    return commands