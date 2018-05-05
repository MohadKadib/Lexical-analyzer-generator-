from pythonds.basic.stack import Stack
import nfaclasses1

def infixToPostfix(infixexpr):
    prec = {}
    prec["@"] = 4
    prec["#"] = 4
    prec["&"] = 3
    prec["|"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token not in "@#&|()" :
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] > prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return "".join(postfixList)

#print(infixToPostfix("(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)&((a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)|(0|1|2|3|4|5|6|7|8|9))*".replace("", " ")[1: -1]))
#print(infixToPostfix(" ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ) + | ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ) + & . & ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ) + & ( L | E & ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ) + ) "))

#########################################################################################

def postfixEval(postfixExpr,variables):
    operandStack = Stack()
    tokenList = postfixExpr.split()

    for token in tokenList:
        if token not in "@#&|":
            token_nfa = nfaclasses1.nfa.init_from_min(token,token,variables)
            operandStack.push(token_nfa)
        else:
            if token == "|":
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                result_nfa = nfaclasses1.nfa.init_or_nfa(operand1.name + operand2.name , operand1,operand2,variables)
                operandStack.push(result_nfa)
            elif token == "&":
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                result_nfa = nfaclasses1.nfa.init_and_nfa(operand1.name + operand2.name, operand1, operand2, variables)
                operandStack.push(result_nfa)
            elif token == "@":
                operand2 = operandStack.pop()
                result_nfa = nfaclasses1.nfa.init_star_nfa(operand2.name + "@",operand2,variables)
                operandStack.push(result_nfa)
            elif token == "#":
                operand2 = operandStack.pop()
                result_nfa = nfaclasses1.nfa.init_plus_nfa(operand2.name + "#",operand2,variables)
                operandStack.push(result_nfa)




    return operandStack.pop()




