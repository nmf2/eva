from eva.entities.train import IOBTagger
from eva.entities.tag import entity_dict
from eva.utils import IOBReader

"""
    How to train a new entity.
    Place training phrases in eva/eva/data in a file ending in .iob
    Use IOBReader to read() all .iob files in the previous folder
"""

rd = IOBReader()  # Object to read .iob files in eva/eva/data
rd.read()  # Read all files

"""
    This attr is a list of all sententences in the file represented like this:
        [(word, pos_tag, iob_tag),...]
"""
rd.iob_sents

"""
    Since the IOBTagger requires the training sentences to be in the format:
        [((word, pos_tag), iob_tag)...]
    The for loop converts the formats
"""

data = []
for s in rd.iob_sents:
    temp = []
    for (w, t, l) in s:
        temp.append(((w, t), l))
    data.append(temp)

"""
    Train the tagger with the data and save the model in a file called
    'test.model' in the current directory. This file has to be put in 
    $EVA_PATH/models to be used by the parser.
"""

tgr = IOBTagger()
tgr.train(data, 'test.model')

"""
    After moving test.model to $EVA_PATH/models specify the models to be used
    in the entity recognition by adding the dictionary as a parameter of the
    entity_dict function
"""

sents = ["A testar"]
ent = entity_dict(*sents, **{'iobmodel': 'test.model'})

# Print all entities
for e in ent:
    print(e)
