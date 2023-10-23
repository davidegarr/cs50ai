# Problem Set 60: Parser
In this project, context-free grammar is employed to parse English sentences, thus understanding their structure. Parsing is vital in natural language processing to comprehend a sentence's meaning and extract information, especially noun phrases, which offer insights into the sentence's theme.

Two functions and one global variable were implemented:
1. Function "preprocess": It takes a sentence as its input, tokenizes it, converts it to lowercase, and returns a list of alphabetic words while excluding any non-alphabetic characters like punctuation or numbers.
2. Function "np_chunk": The function accepts a syntax tree of a sentence and returns a list of all the noun phrase chunks in that sentence.
3. Global variable "NONTERMINALS":  It holds the context-free grammar rules.