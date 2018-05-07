from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, connections, Q
import pprint

printer = pprint.PrettyPrinter(indent=4)
pp = printer.pprint

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
response_model = {
    "intent": "aulas_professor",
    "entities": [
        "PESSOA"
    ],
    "entities_mappings": {
        "PESSOA": "professor"
    },
    "search_parameters":{
        "professor": "id"
    },
    "template": "O professor @professor.id dá as seguintes cadeiras:\n[@professor.disciplinas,\t\n]"
}

def entities_types(entities):
    types = []
    for entity in entities:
        types.append(entity['type'])
    return types

client = Elasticsearch()
connections.create_connection(hosts=['localhost:9200'])
s = Search(using=client, doc_type="_doc")
search = s.index("cin_response_model")

types = entities_types(ex_question[0]['entities'])

query = Q('term', intent=ex_question[0]['intent']) & Q('match', entities=types[0])

res = search.query(query).execute()

response = res[0].to_dict()

pp (query.to_dict())


pp (response)

print ()

# mappings = response['entities_mappigns']
# response['entities_mappigns']
# for entity in ex_question['entities']:

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

mappings = response_model['entities_mappings']
search_params = response_model['search_parameters']
pp(search_params)

BOT_NAME = 'cin'

entity = ex_question[0]['entities'][0]

db_entity = mappings[entity['type']]    # professor
pp (db_entity)
index = BOT_NAME + "_" + db_entity      # cin_professor
param = search_params[db_entity]        # id

value = entity['value']                 # divanilson

search_db_entity = search.index(index).sort("_score")
query = Q("match", **{param : value})

pp(query.to_dict())

res = search_db_entity.query(query).execute()

print (res[0].to_dict())

entities = []

for entity in ex_question[0]['entities']:
    db_entity = mappings[entity['type']]    # professor
    index = BOT_NAME + "_" + db_entity      # cin_professor
    param = search_params[db_entity]        # param
    value = entity['value']                 # divanilson

    search_db_entity = search.index(index).sort("_score")
    query = Q("match", **{param : value})

    response_entity = search_db_entity.query(query).execute()

    entities.append(response_entity[0].to_dict())
print()
print ({
        'entities':entities,
        'template':response_model['template']
        })
{"template": "O professor @professor.id dá as seguintes cadeiras:\n[@professor.disciplinas,\t\n]", "entities": [{"disciplinas": ["Tópicos Acançados em PROCESSAMENTO DE SINAIS - Introd Proc Estocásticos", "SINAIS SISTEMAS PARAR ENGENHARIA DA COMPUTACAO"], "id": "Divanilson Campelo"}]}