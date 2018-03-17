import re
import bunch

ex_question = [{
    'entities': [{'type': 'DISCIPLINA', 'value': 'Infra de Software'}],
    'intent': 'horario_disciplina',
    'raw': 'hora Infra de Software'
}]

ex_model = [
    {
        "entities": {
            "professor":{
                "nome": "Neto",
                "apelidos": "",
                "disciplinas": [
                    "Física para Computação",
                    "IC",
                    "Estágio"
                ]
            }
        },
        "template": "O professor @professor.nome  dá as seguintes cadeiras:\n[@professor.disciplinas,\n]"
    }
]

def get_responses_models(questions):
    # Connect to elastic search and stuff
    # Separate questions and send to Elastic Search
    # Learn elastic search
    return ex_model

"""
    Generate a response based on the intent, entities and model of response.

    @param questions
        @type [dict]
        List of dictionaries which represents a structured questions with entities, intents and raw content of each question. Format:
            [
                {
                    'entities':[{'type':'...', 'value':'...'}, ...]
                    'intent':'...'
                    'raw':'...'
                },
                ...
            ]
    @return [string]
    
"""

def treat_list_of_attributes(template, entities):
    answer = template
    regex = r"\[@([A-Za-z0-9]*)\.(.[A-Za-z0-9]*),([A-Za-z0-9]*|[^A-Za-z0-9]+)\]"
    lists = re.finditer(regex, answer)

    for list_ in lists:
        entity, attributes_list_name, separator = list_.groups()
        attr_list = ''
        for attribute in entities[entity][attributes_list_name]:
            attr_list += attribute + separator

        answer = answer.replace(list_.group(), attr_list)
    
    return answer

def treat_regular_attributes(template, entities):
    answer = template
    regex = r"@([A-Za-z0-9]*)\.([A-Za-z0-9]*)"
    matches = re.finditer(regex, answer)

    for match in matches:
        entity, attribute_name = match.groups()
        attribute = entities[entity][attribute_name]
        answer = answer.replace(match.group(), attribute)

    return answer

def generate_answer(questions):
    answers = []
    responses_models = get_responses_models(questions)

    for model in responses_models:
        answer = model['template']
        answer = treat_list_of_attributes(answer, model['entities'])
        answer = treat_regular_attributes(answer, model['entities'])
        answers.append(answer)

    return '\n'.join(answers)