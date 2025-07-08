# LL(1) Parser

A Python-based LL(1) parser that computes first and follow sets, builds a parse table, and parses input strings for context-free grammars.

## Features
- **First Sets**: Computes the first sets for all non-terminals in the grammar.
- **Follow Sets**: Computes the follow sets for all non-terminals based on the grammar and first sets.
- **Parse Table**: Constructs an LL(1) parse table, detecting conflicts if the grammar is not LL(1).
- **Input Parsing**: Parses input strings using the parse table, with error correction for invalid inputs.
- **Tokenization**: Supports terminals like `id`, `+`, `*`, `(`, `)`, and single alphabetic characters.
- **Interactive Input**: Allows users to define grammar rules and input strings interactively.

## Requirements
- Python 3.6+
- No external libraries are required.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. No additional dependencies are needed, as the script uses only standard Python libraries.

## Usage
1. Run the script:
   ```bash
   python ll1_parser.py
   ```
2. Enter grammar rules in the format `NonTerminal -> Production1 | Production2` (e.g., `E -> T E'`). Use `''` for epsilon productions. Press Enter twice to finish.
3. The program computes and displays the first and follow sets.
4. If the grammar is LL(1), it displays the parse table.
5. Enter an input string to parse (e.g., `id + id * id`).
6. The program outputs the parsing steps and whether the input is accepted or rejected.

### Example
```
Enter grammar rules (empty line to end):
E -> T E'
E' -> + T E' | ''
T -> F T'
T' -> * F T' | ''
F -> ( E ) | id

First sets:
E: { (, id }
E': { $, + }
T: { (, id }
T': { $, *, + }
F: { (, id }

Follow sets:
E: { $, ) }
E': { $, ) }
T: { $, ), + }
T': { $, ), + }
F: { $, ), *, + }

Parse Table:
M[E, (] = T E'
M[E, id] = T E'
M[E', +] = + T E'
M[E', $] = ''
M[E', )] = ''
M[T, (] = F T'
M[T, id] = F T'
M[T', *] = * F T'
M[T', $] = ''
M[T', +] = ''
M[T', )] = ''
M[F, (] = ( E )
M[F, id] = id

Enter an input string to parse: id + id * id

Parsing Steps:
Stack               Input               Action
['$', 'E']          id + id * id $      Output E -> T E'
['$', 'E', 'T']     id + id * id $      Output T -> F T'
['$', 'E', 'T', 'F'] id + id * id $      Output F -> id
['$', 'E', 'T', 'id'] id + id * id $      Match
['$', 'E', 'T']     + id * id $         Output T' -> ''
['$', 'E']          + id * id $         Output E' -> + T E'
['$', 'E', '+']     + id * id $         Match
['$', 'E', 'T']     id * id $           Output T -> F T'
['$', 'E', 'T', 'F'] id * id $           Output F -> id
['$', 'E', 'T', 'id'] id * id $           Match
['$', 'E', 'T']     * id $              Output T' -> * F T'
['$', 'E', 'T', '*'] * id $              Match
['$', 'E', 'T', 'F'] id $                Output F -> id
['$', 'E', 'T', 'id'] id $                Match
['$', 'E', 'T']     $                   Output T' -> ''
['$', 'E']          $                   Output E' -> ''
['$']               $                   Match
Input string successfully parsed.
accept
```

## Project Structure
- `ll1_parser.py`: Main script containing the LL(1) parser implementation.
- `requirements.txt`: Empty, as no external dependencies are required.
- `.gitignore`: Specifies files and directories to ignore in version control.

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License.