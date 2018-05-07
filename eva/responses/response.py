import re
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, connections, Q

ex_question = [
    {
        "entities": [
            {
                "value": "Divanilson",
                "type": "PESSOA"
            }
        ],
        "raw": "Disciplinas do professor Divanilson",
        "intent": "aulas_professor"
    }
]

ex_model = [
    {
        "entities": {
            "professor":{
                "id": "Divanilson",
                "apelidos": "",
                "disciplinas": [
                    "Sinais e Sistemas para Computação",
                    "IC",
                    "Estágio"
                ]
            }
        },
        "template": "O professor @professor.id dá as seguintes cadeiras:\n[@professor.disciplinas,\n]"
    }
]

BOT_NAME = "cin"

"""
    Get responses models based on input questions
    @param questions
        @type [dict]
        List of dictionaries which represents a structured questions with entities, intents and raw content of each question. Format:
            [
                {
                    "entities':[{'type':'...', 'value':'...'}, ...]
                    'intent':'...'
                    'raw':'...'
                },
                ...
            ]
    @return 
"""
# setup connection with ES and global search object
def ph(hits):
    print("hits: " + str(hits.total))
    for hit in hits:
        print(hit.to_dict())
    print()

connections.create_connection(hosts=['localhost:9200'])
search = Search(using=Elasticsearch(), doc_type='_doc')

def get_responses_models(questions):
    # setup models search object
    search_models = search.index(BOT_NAME+"_response_model")

    def entity_types(entities):
        types = []
        for entity in entities:
            types.append(entity['type'])
        
        return types

    def build_query(intent, entity_types=""):
        query = Q('term', intent=intent) & \
                Q('terms', entities=entity_types)
        
        return query

    models = []

    for question in questions:
        query = build_query(question['intent'], entity_types(question['entities']))
        # print (entity_types(question['entities']))
        # print (question)
        # print (query)

        response_model = search_models.query(query).execute()

        print(response_model.success())
        ph (response_model.hits)
        
        response_model = response_model.hits[0].to_dict()

        structured_response = get_structured_response(response_model, question)
        
        models.append(structured_response)

    return models

ex_question = [
    {
        "entities": [
            {
                "value": "Divanilson",
                "type": "PESSOA"
            }
        ],
        "raw": "Disciplinas do professor Divanilson",
        "intent": "aulas_professor"
    }
]
def get_structured_response(model, question):
    """
        Use values of entities from the question and map the values to the entities in the database.
        Then make a request to the db with the value and the actual entity
    """
    # print (model)
    mappings = model['entities_mapping']
    search_params = model['search_parameters']

    entities = []

    for question_entity in question['entities']:
        # print ('\n',mappings)
        # print (question_entity)
        
        if question_entity['type'] in mappings:
            db_entity = mappings[question_entity['type']]
        else:
            db_entity = question_entity['type'].lower()

        if db_entity in search_params:
            param = search_params[db_entity]
        else:
            param = 'id'

        index = BOT_NAME + "_" + db_entity
        value = question_entity['value']

        search_db_entity = search.index(index).sort("_score")
        query = Q("match", **{param : value})
        print(query)
        response_entity = search_db_entity.query(query).execute()
        ph(response_entity.hits)
        response_entity = response_entity[0].to_dict()
        response_entity = {db_entity:response_entity}
        entities.append(response_entity)

    return {
            'entities':entities,
            'template':model['template']
        }
    

def generate_answer(questions):
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
    def treat_regular_attributes(template, entities):
        answer = template
        regex = r"@([A-Za-z0-9]*)\.([A-Za-z0-9]*)"
        matches = re.finditer(regex, answer)

        for match in matches:
            entity, attribute_name = match.groups()
            print (entities)
            attribute_value = entities[entity][attribute_name]
            answer = answer.replace(match.group(), attribute_value)

        return answer
        
    def treat_list_attributes(template, entities):
        # TODO
        #  - Make "entities" entry on structured response obj be a list
        answer = template
        regex = r"\[@([A-Za-z0-9]*)\.(.[A-Za-z0-9]*),([A-Za-z0-9]*|[^A-Za-z0-9]+)\]"
        matches = re.finditer(regex, answer)
        print (*matches) # erase
        for match in matches:
            entity, attributes_list_name, separator = match.groups()
            attr_list = ''
            for attribute_value in entities[entity][attributes_list_name]:
                attr_list += attribute_value + separator

            answer = answer.replace(match.group(), attr_list)
        
        return answer
    
    answers = []
    responses_models = get_responses_models(questions)
    
    for model in responses_models:
        answer = model['template']
        answer = treat_list_attributes(answer, model['entities'])
        answer = treat_regular_attributes(answer, model['entities'])
        answers.append(answer)
    
    return '\n'.join(answers)

from eva.utils.parser import *

question = parse("Aulas do professor Divanilson")
answer = generate_answer(question)

print(answer)