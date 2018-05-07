__all__=['convert_entities']

def convert_entities(questions, mapping_model):
    """
        Map entities of each question in the questions list.
    """
    converted_questions = []
    for question in questions:

        converted_question = question
        intent = question['intent']
        entities = question['entities']
        
        converted_entities = []

        for entity in entities:
            if entity['type'] in mapping_model.keys():
                entity['type'] = mapping_model[entity['type']]
            else:
                entity['type'] = entity['type'].lower()
            converted_entities.append(entity)
        
        converted_questions.append(converted_question)

    return converted_questions

q = [{'entities': [{'value': 'Divanilson', 'type': 'PESSOA'}], 'intent': 'aulas_professor', 'raw': 'Disciplinas do professor Divanilson'}]

print (convert_entities(q,None))