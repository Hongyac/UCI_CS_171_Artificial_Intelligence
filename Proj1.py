'''
Created on Jan 17, 2021

@author: johns
'''
import CYKParse
import Tree

requestInfo = {
        'name': '',
        'time': '',
        'location': ''
}
haveGreeted = False

# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):
    sentenceTrees = { k: v for k,v in T.items() if k.startswith('S/0') }
    completeSentenceTree = max(sentenceTrees.keys())
    #print('getSentenceParse', completeSentenceTree)
    return T[completeSentenceTree]

# Processes the leaves of the parse tree to pull out the user's request.
def updateRequestInfo(Tr):
    global requestInfo
    lookingForLocation = False
    lookingForName = False
    for leaf in Tr.getLeaves():
        if leaf[0] == 'Adverb':
            requestInfo['time'] = leaf[1]
        if lookingForLocation and leaf[0] == 'Name':
            requestInfo['location'] = leaf[1]
        if leaf[0] == 'Preposition' and leaf[1] == 'in':
            lookingForLocation = True
        else:
            lookingForLocation = False
        if leaf[0] == 'Noun' and leaf[1] == 'name':
            lookingForName = True
        if lookingForName and leaf[0] == 'Name':
            requestInfo['name'] = leaf[1]

# This function contains the data known by our simple chatbot
def getTemperature(location, time):
    if location == 'Irvine':
        if time == 'now':
            return '68'
        elif time == 'tomorrow':
            return '70'
        else:
            return 'unknown'
    else:
        return 'unknown'

# Format a reply to the user, based on what the user wrote.
def reply():
    global requestInfo
    global haveGreeted
    if not haveGreeted and requestInfo['name'] != '':
        print("Hello", requestInfo['name'] + '.')
        haveGreeted = True
        return
    time = 'now' # the default
    if requestInfo['time'] != '':
        time = requestInfo['time']
    salutation = ''
    if requestInfo['name'] != '':
        salutation = requestInfo['name'] + ', '
    print(salutation + 'the temperature in ' + requestInfo['location'] + ' ' +
        time + ' is ' + getTemperature(requestInfo['location'], time) + '.')

# A simple hard-coded proof of concept.
def main():
    global requestInfo
    T, P = CYKParse.CYKParse(['hi', 'my', 'name', 'is', 'Peter'], CYKParse.getGrammarWeather())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'is', 'the', 'temperature', 'in', 'Irvine', 'now'], CYKParse.getGrammarWeather())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()
    
    T, P = CYKParse.CYKParse(['what', 'is', 'the', 'temperature', 'in', 'Pasadena', 'now'], CYKParse.getGrammarWeather())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()
    
#     T, P = CYKParse.CYKParse(['Will', 'tomorrow', 'be', 'hotter', 'than', 'today', 'in','Irvine'], CYKParse.getGrammarWeather())
#     sentenceTree = getSentenceParse(T)
#     updateRequestInfo(sentenceTree)
#     reply()
    
#     T, P = CYKParse.CYKParse(['Will', 'yesterday', 'be', 'hotter', 'than', 'tomorrow', 'in','Pasadena'], CYKParse.getGrammarWeather())
#     sentenceTree = getSentenceParse(T)
#     updateRequestInfo(sentenceTree)
#     reply()

main()