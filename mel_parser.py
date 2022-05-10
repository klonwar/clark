from lark import Lark
from lark.lexer import Token
from lark.visitors import InlineTransformer

from mel_ast import *


parser = Lark('''
    %import common.NUMBER
    %import common.ESCAPED_STRING
    %import common.CNAME
    %import common.NEWLINE
    %import common.WS

    %ignore WS

    COMMENT: "/*" /(.|\\n|\\r)+/ "*/"
        |  "//" /(.)+/ NEWLINE
    %ignore COMMENT

    num: NUMBER  -> literal
    str: ESCAPED_STRING  -> literal
    ident: CNAME 
    ?type: ident -> type
        | map_type
    
    MAP : "map"
    
    ADD:     "+"
    SUB:     "-"
    MUL:     "*"
    DIV:     "/"
    MOD:     "%"
    AND:     "&&"
    OR:      "||"
    BIT_AND: "&"
    BIT_OR:  "|"
    GE:      ">="
    LE:      "<="
    NEQUALS: "!="
    EQUALS:  "=="
    GT:      ">"
    LT:      "<"


    call: ident "(" ( expr ( "," expr )* )? ")" 
    | ident "." ident "(" ( expr ( "," expr )* )? ")"
    | map_ref

    map_ref: (ident | call) braces* -> map_ref
    
    map_type: MAP "<" type "," type ">"
    
    ?braces: "[" expr "]"
    
    in: expr "in" ident -> in

    ?group: num | str
        | ident
        | call
        | "(" expr ")"
   
    ?mult: group
        | mult ( MUL | DIV | MOD ) group  -> bin_op

    ?add: mult
        | add ( ADD | SUB ) mult  -> bin_op

    ?compare1: add
        | add ( GT | LT | GE | LE ) add  -> bin_op

    ?compare2: compare1
        | compare1 ( EQUALS | NEQUALS ) compare1  -> bin_op

    ?logical_and: compare2
        | logical_and AND compare2  -> bin_op

    ?logical_or: logical_and
        | logical_or OR logical_and  -> bin_op

    ?expr: logical_or
        | in
    
    ?simple_assign : ident "=" expr -> assign
        
    ?var_decl_inner: ident
        | simple_assign

    vars_decl: type var_decl_inner ( "," var_decl_inner )*

    assign : ident "=" expr
    
    ?simple_stmt: assign
        | call

    ?for_stmt_list: vars_decl
        | ( simple_stmt ( "," simple_stmt )* )?  -> stmt_list
    ?for_cond: expr
        |   -> stmt_list
    ?for_body: stmt
        | ";"  -> stmt_list

    fun_decl: type ident "(" (param ("," param) *)* ")" composite
        | type ident "("(param ("," param) *)* ")" ";" 
    
    ?param_list: (param ("," param) *)*
    
    ?param: type ident
    
    return: "return" expr
    ?composite: "{" stmt_list "}"
    
    ?stmt: fun_decl
        | return ";"
        | vars_decl ";"
        | simple_stmt ";"
        | "if" "(" expr ")" stmt ("else" stmt)?  -> if
        | "for" "(" for_stmt_list ";" for_cond ";" for_stmt_list ")" for_body  -> for
        | "while" "(" expr ")" stmt -> while
        | composite
        
    stmt_list: (stmt";"*)*

    ?program: stmt_list
''', start='program')  # , parser='lalr')


class MelASTBuilder(InlineTransformer):
    def __getattr__(self, item):
        if isinstance(item, str) and item.upper() == item:
            return lambda x: x

        if item in ('bin_op', ):
            def get_bin_op_node(*args):
                op = BinOp(args[1].value)
                return BinOpNode(op, args[0], args[2],
                                 **{'token': args[1], 'line': args[1].line, 'column': args[1].column})
            return get_bin_op_node
        elif item in ('map_type', ):
            def get_map_type_node(*args):
                return TypeNode(args[0], (args[1], args[2]),
                                **{'token': args[0], 'line': args[0].line, 'column': args[0].column})
            return get_map_type_node
        elif item in ('type', ):
            def get_type_node(*args):
                return TypeNode(args[0],
                                **{'token': args[0], 'line': args[0].line, 'column': args[0].column})
            return get_type_node
        elif item in ('fun_decl', ):
            def get_func_decl_node(*args):
                if len(args) == 3:
                    return FunDeclNode(type_=args[0], name=args[1], params=(), func_body=args[-1],
                                       **{'token': args[0], 'line': args[0].line, 'column': args[0].column})
                return FunDeclNode(args[0], args[1], args[2:-1], args[-1],
                                   **{'token': args[0], 'line': args[0].line, 'column': args[0].column})
            return get_func_decl_node
        else:
            def get_node(*args):
                props = {}
                if len(args) == 1 and isinstance(args[0], Token):
                    props['token'] = args[0]
                    props['line'] = args[0].line
                    props['column'] = args[0].column
                    args = [args[0].value]
                cls = eval(''.join(x.capitalize() for x in item.split('_')) + 'Node')
                return cls(*args, **props)
            return get_node


def parse(prog: str) -> StmtListNode:
    prog = parser.parse(str(prog))
    # print(prog.pretty('  '))
    prog = MelASTBuilder().transform(prog)
    return prog
