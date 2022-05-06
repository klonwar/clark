import os

from . import parser
from . import semantic
from . import msil


def execute(prog: str) -> None:
    prog = parser.parse(prog)

    print('ast:')
    print(*prog.tree, sep=os.linesep)
    print()

    print('semantic_check:')
    try:
        scope = semantic.prepare_global_scope()
        prog.semantic_check(scope)
        print(*prog.tree, sep=os.linesep)
    except semantic.SemanticException as e:
        print('Ошибка: {}'.format(e.message))
        return
    print()

    '''
    print('msil:')
    try:
        gen = msil.CodeGenerator()
        gen.start()
        prog.msil(gen)
        gen.end()
        print(*gen.code, sep=os.linesep)
    except semantic.SemanticException as e:
        print('Ошибка: {}'.format(e.message))
        return
    print()
    '''
