# trace-nfa

The nfa_sco.py program prompts the user to enter the name of the NFA file. Once the NFA data is loaded, the program will request the user to input a string to test. It will then display the total number of possible paths and the number of accepting paths on the screen.

## extra work
The extra work involved developing a Python script that simulates the behavior of a Non-deterministic Finite Automaton (NFA). The NFA is defined through a configuration file containing metadata (NFA name, states, symbols, start state, and accept states) and transition rules. The script is designed to:

1. Load an NFA configuration from a CSV file.
2. imulate the NFA on a given input string.
3. Track the number of total paths and accepting paths.
4. Output the results to a CSV file, including the full state sequences for accepting paths.

The extra work also includes handling epsilon transitions (~), which are transitions that occur without consuming an input symbol.



