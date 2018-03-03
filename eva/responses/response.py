exQuestion = [{
    'entities': [{'type': 'DISCIPLINA', 'value': 'Infra de Software'}],
    'intent': 'horario_disciplina',
    'raw': 'hora Infra de Software'
}]

exResponse = [
    {
        'infos':[{'type':'horario', 'value':'5:30 pm'}, {'type':'disciplina', 'value':'infra de software'}],
        'template':'O horário da disciplina @disciplina é @horario.'
    }
]
def getResponsesModels(questions):
    # Connect to elastic search and stuff
    # Separate questions and send to Elastic Search
    # Learn elastic search
    return exResponse

"""
    Generate a response based on the intent, entities and model of response.

    @param questions
        @type [dict]
        List of dictionaries which represents a structured question with entities, intent and raw content of each question. Format:
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

def generateAnswer(questions):
    answers = []

    responsesModels = getResponsesModels(questions)

    for model in responsesModels:
        answer = model['template']
        for info in model['infos']:
            answer = answer.replace('@{}'.format(info['type']), info['value'])
        
        answers.append(answer)

    return answers

print(*generateAnswer(exQuestion))
