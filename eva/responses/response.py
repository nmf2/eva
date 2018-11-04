import re
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, connections, Q, Index

import json


class Respondent:
    """
    Object to get answers for structured quesions.
        :param bot_name: (str) The name of the bot to be used as prefix for
        searches in Elasticsearch.
        :param hosts: ([str]) Database's host addresses. Defaults to
        ['localhost:9200'].
    """

    def __init__(self, hosts=['localhost:9200']):

        connections.create_connection(hosts=hosts)
        self.search = Search(using=Elasticsearch(), doc_type='_doc')

    def get_responses_models(self, questions):
        """
        Get response models from Elasticsearch based on the intent and
        entities from questions.
            :param questions: ([dict]) List of structured questions.
        """

        search_models = self.search.index("response_model")

        def entity_types(entities):
            types = []
            for entity in entities:
                types.append(entity['type'])

            return types

        def build_query(intent, entity_types=[]):
            query = Q('term', intent=intent)
            if (entity_types != []):
                query = query & Q('terms', **{"entities.keyword": entity_types})

            return query

        models = []

        for question in questions:
            query = build_query(
                question['intent'],
                entity_types(question['entities'])
                )
            search_models = search_models.query(query)
            print(json.dumps(search_models.to_dict(), indent=2))
            response_model = search_models.execute()
            print(json.dumps(response_model.to_dict(), indent=2))

            if (response_model.hits.total == 0):
                response_model = {"entities": [],
                                  "template":
                                  "Perdão, não entendi a pergunta :("
                                  }
                models.append(response_model)

            else:
                response_model = response_model.hits[0].to_dict()
                structured_response = self.get_structured_response(
                    response_model, question)
                models.append(structured_response)

        return models

    def get_structured_response(self, model, question):
        """
        Get entities needed to generate an answer for the question from
        Elasticsearch.
            :param model: (dict) A response model.
            :param quesion: (dict) A structured question.
        """

        mappings = model['entities_mapping']
        search_params = model['search_parameters']
        template = model['template']
        entities = {}

        print(json.dumps(question, indent=2))

        for question_entity in question['entities']:
            if question_entity['type'] in mappings:
                db_entity = mappings[question_entity['type']]
            else:
                db_entity = question_entity['type'].lower()

            if db_entity in search_params:
                param = search_params[db_entity]
            else:
                param = 'id'

            index = db_entity
            value = question_entity['value']

            if not Index(index).exists():
                continue

            search_db_entity = self.search.index(index).sort("_score")
            query = Q("match", **{param: value})
            search_db_entity = search_db_entity.query(query)
            print("query\n" + json.dumps(search_db_entity.to_dict(), indent=2))
            response_entity = search_db_entity.execute()
            print(response_entity.to_dict())
            if (response_entity.hits.total is 0):
                template = "Não consegui encontrar informações sobre " + \
                    question_entity['value'] + " :( "
            else:
                response_entity = response_entity[0].to_dict()
            response_entity = {db_entity: response_entity}
            entities.update(response_entity)

        return {
                'entities': entities,
                'template': template
            }

    def answer(self, questions):
        """
        Generate answers based on the intent, entities and model of response.
        The answer will be in plain text, ready to be delivered to the user.
            :param questions: ([dict]) List of structured questions
        """

        def treat_regular_attributes(template, entities):
            answer = template
            regex = r"@([A-Za-z0-9]*)\.([A-Za-z0-9]*)"
            matches = re.finditer(regex, answer)
            try:
                for match in matches:
                    entity, attribute_name = match.groups()
                    attribute_value = entities[entity][attribute_name]
                    print(attribute_value)
                    if type(attribute_value) == list:
                        continue
                    answer = answer.replace(match.group(), attribute_value)
            except:
                raise
                answer = "Perdão, não entendi que você quis dizer."
            return answer

        def treat_list_attributes(template, entities):
            # TODO
            #  - Make "entities" entry on structured response obj be a list
            answer = template
            # Don't break the regex string to prettify with '\'. Why? Errors.
            regex = r"\[@([A-Za-z0-9]*)\.(.[A-Za-z0-9]*),([A-Za-z0-9]*|[^A-Za-z0-9]+)\]"

            matches = re.finditer(regex, answer)
            for match in matches:
                try:
                    entity, attr_list_name, separator = match.groups()
                    print(' '.join((entity, attr_list_name, separator)))
                    attr_list = ''
                    for attribute_value in entities[entity][attr_list_name]:
                        attr_list += attribute_value + separator

                    answer = answer.replace(match.group(), attr_list)
                except:
                    answer = "Perdão, não entendi que você quis dizer."

            return answer

        answers = []
        responses_models = self.get_responses_models(questions)

        for model in responses_models:
            answer = model['template']
            answer = treat_list_attributes(answer, model['entities'])
            answer = treat_regular_attributes(answer, model['entities'])
            answers.append(answer)

        return '\n'.join(answers)
