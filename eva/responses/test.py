from eva.utils.parser import parse
from eva.responses.response import Respondent


q = parse('professor de algoritmos de engenharia da computação')

res = Respondent()

print(res.answer(q))
