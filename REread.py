import nfaclasses1
import infixtopostfix
import dfaclasses1
import copy
from collections import OrderedDict


f = open("lexical.txt")
#print(f.read())
lines = f.readlines()
f.close()

keywords= []
punctuations = []
regexp = OrderedDict()
regdef = OrderedDict()

for x in lines:
    if x[0] not in ("{","[")  :
        i =0
        while (i<len(x)):

            if x[i] in (":") :
                newexp = x[i+1:-1]
                for k,v in regdef.items() :
                    newexp=newexp.replace(k,v)

                regexp.update({x[0:i-1]:newexp})
                break
            elif x[i] in ("=") :
                regdef.update({x[0:i - 1]: x[i + 1:-1]})
                break
            else :
                i=i+1

    elif x[0] == "{" :
        min_keywords =x.split(" ")
        del min_keywords[0]
        del min_keywords[-1]
        keywords.extend(min_keywords)
        #print(keywords)

    elif x[0] == "[" :
        min_punctuations =x.split(" ")
        del min_punctuations [0]
        del min_punctuations [-1]
        punctuations.extend(min_punctuations)
        #print (punctuations)



state_counter =0

print regexp
print regdef
print (keywords)
print (punctuations)

###############################################################################################
for k,v in regexp.items():
    regexp[k] =v.replace("0-9","(0|1|2|3|4|5|6|7|8|9)")

for k,v in regexp.items():
    regexp[k] = v.replace("a-z|A-Z","(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)")
print regexp
#############################################################################################
for k,v in regexp.items():
    regexp[k]= infixtopostfix.infixToPostfix(v.replace("", " ")[1: -1])

print regexp

##################################################################################################

nfas_dictionary = OrderedDict()
variables = nfaclasses1.global_variables()

keywords_dict = OrderedDict()
punct_dict = dict.fromkeys(punctuations,nfaclasses1.nfa)
print punct_dict


for x in keywords :
    keywords_dict.update( {x.replace("&","") : infixtopostfix.infixToPostfix(x.replace("", " ")[1: -1]) })
print keywords_dict

for k,v in regexp.items():
    nfas_dictionary.update(        {k   :   infixtopostfix.postfixEval(v.replace("", " ")[1: -1],variables)}   )

for k,v in punct_dict.items():
    nfas_dictionary.update({k:infixtopostfix.postfixEval(k.replace("", " ")[1: -1],variables)})

for k,v in keywords_dict.items():
    nfas_dictionary.update({k:infixtopostfix.postfixEval(v.replace("", " ")[1: -1],variables)})




print nfas_dictionary

##################################################################################################
dfa_variables = dfaclasses1.global_dfa_variables()

dfas_dictionary = OrderedDict()
for k,v in nfas_dictionary.items():
    dfas_dictionary[k]=dfaclasses1.dfa(v,dfa_variables,variables)

print dfas_dictionary

##################################################################################################

p =open("program.txt")
codes = p.readlines()
p.close()
temp_dfas_dictionary = copy.deepcopy(dfas_dictionary)
temp_dfas_keys = list(temp_dfas_dictionary.keys())
print temp_dfas_dictionary
print temp_dfas_keys
current_state_dictionary = OrderedDict()
current_state_dictionary.fromkeys(temp_dfas_dictionary.keys(),int)
for k in temp_dfas_keys:
    current_state_dictionary[k]=copy.copy(temp_dfas_dictionary[k].start_dfa_state_number)

outputfile =open("output.txt","w")

for line in codes:#loop on lines
    line = line[:-1]
    line = line + " "
    new_token = True
    final_state_token = {}
    ioi = 0
    while ioi < len(line) : #loop on char



        if new_token == True:#reset current state dictionary if new token
            final_state_token = {}
            for k, v in current_state_dictionary.items():
                current_state_dictionary[k] = copy.copy(dfas_dictionary[k].start_dfa_state_number)
            temp_dfas_keys = list(temp_dfas_dictionary.keys())



        for current_key in temp_dfas_keys[:] :# loop on dfas


            if line[ioi] in dfa_variables.world_dfa_states[current_state_dictionary[current_key]].dfa_transitions: #if input matches a transition on the dfa


                for n,o in dfa_variables.world_dfa_states.items():        #change dfa current state
                    if o.nfa_states ==dfa_variables.world_dfa_states[current_state_dictionary[current_key]].dfa_transitions[line[ioi]]:
                        current_state_dictionary[current_key] =copy.copy(n)
                        break




            elif current_state_dictionary[current_key] in temp_dfas_dictionary[current_key].final_dfa_states: # if input doesnt match a transition but current state is final
                final_state_token.update({current_key : ioi-1  })
                temp_dfas_keys.remove(current_key)


            else:    # if input doesnt match a transition on the dfa
                temp_dfas_keys.remove(current_key)

        if temp_dfas_keys == [] : #no longer prefix can be matched
            new_token = True
            if line[ioi] != ' ':
                ioi = final_state_token[final_state_token.keys()[0]]

            outputfile.write(final_state_token.keys()[0] +"\n")






        else:
            new_token= False

        if line[ioi] == ' ':
            new_token= True

        ioi += 1


















