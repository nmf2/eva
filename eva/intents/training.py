from eva.intents.train import IntentClassifier
from eva.intents.classify import get_intent

classifier = IntentClassifier()
classifier.fit()
classifier.save('intent_test.model')

print(get_intent("A testar", model='intent_test.model'))
