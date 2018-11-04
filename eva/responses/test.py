from eva.utils.parser import parse
from eva.responses.response import Respondent


q = parse('Aulas do professor Mello')
print("per:\n" + str(q[0]))

res = Respondent()

# cProfile.run("print(res.answer(q))", "anstats")

# p = pstats.Stats('anstats')

# p.sort_stats("cumulative").print_stats(20)
print(res.answer(q))
