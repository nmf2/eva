import re
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

ex_question = [
    {
    'raw': 'Cadeiras de Divanilson', 
    'entities': [{'value': 'Divanilson', 'type': 'DISCIPLINA'}], 
    'intent': 'aulas_professor'
    }
]

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

class Response:
    BOT_NAME = ""
    def __init__(self, bot_name):
        BOT_NAME = bot_name
    
    """
        Get responses models based on input questions
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
        @return 
    """
    def get_responses_models(self, questions):
        def run_query(query):

            pass
        for question in questions:
            try:
                query = question.entity_query
            except:
                pass
            
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
    def generate_answer(self, questions):
        def treat_regular_attributes(template, entities):
            answer = template
            regex = r"@([A-Za-z0-9]*)\.([A-Za-z0-9]*)"
            matches = re.finditer(regex, answer)

            for match in matches:
                entity, attribute_name = match.groups()
                attribute_value = entities[entity][attribute_name]
                answer = answer.replace(match.group(), attribute_value)

            return answer
            
        def treat_list_attributes(template, entities):
            answer = template
            regex = r"\[@([A-Za-z0-9]*)\.(.[A-Za-z0-9]*),([A-Za-z0-9]*|[^A-Za-z0-9]+)\]"
            matches = re.finditer(regex, answer)

            for match in matches:
                entity, attributes_list_name, separator = match.groups()
                attr_list = ''
                for attribute_value in entities[entity][attributes_list_name]:
                    attr_list += attribute_value + separator

                answer = answer.replace(match.group(), attr_list)
            
            return answer
        
        answers = []
        responses_models = self.get_responses_models(questions, )
        
        for model in responses_models:
            answer = model['template']
            answer = treat_list_attributes(answer, model['entities'])
            answer = treat_regular_attributes(answer, model['entities'])
            answers.append(answer)
        

        return '\n'.join(answers)