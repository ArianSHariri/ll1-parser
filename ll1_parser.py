def compute_first(grammar, non_terminals, terminals):
    first = {nt: set() for nt in non_terminals}

    def first_of(symbol):
        if symbol in terminals:
            return {symbol}
        if symbol == "''":
            return {"''"}

        result = set()
        for rule in grammar.get(symbol, []):
            for part in rule.split():
                part_first = first_of(part)
                result.update(part_first - {"''"})
                if "''" not in part_first:
                    break
            else:
                result.add("''")
        return result

    for nt in non_terminals:
        first[nt] = first_of(nt)
    return first

def compute_follow(grammar, non_terminals, terminals, first):
    follow = {nt: set() for nt in non_terminals}
    start_symbol = list(grammar.keys())[0]
    follow[start_symbol].add('$')

    while True:
        updated = False
        for nt in non_terminals:
            for rule in grammar.get(nt, []):
                rule_parts = rule.split()
                for i, part in enumerate(rule_parts):
                    if part in non_terminals:
                        next_first = set()
                        for next_symbol in rule_parts[i + 1:]:
                            if next_symbol in terminals:
                                next_first.add(next_symbol)
                                break
                            next_first.update(first[next_symbol] - {"''"})
                            if "''" not in first[next_symbol]:
                                break
                        else:
                            next_first.update(follow[nt])
                        if not next_first.issubset(follow[part]):
                            follow[part].update(next_first)
                            updated = True
        if not updated:
            break
    return follow

def compute_parse_table(grammar, non_terminals, terminals, first, follow):
    parse_table = {nt: {} for nt in non_terminals}

    for nt in non_terminals:
        for rule in grammar[nt]:
            rule_first = set()

            for symbol in rule.split():
                symbol_first = first[symbol] if symbol in non_terminals else {symbol}
                rule_first.update(symbol_first - {"''"})
                if "''" not in symbol_first:
                    break
            else:
                rule_first.add("''")

            for terminal in rule_first:
                if terminal != "''":
                    if terminal in parse_table[nt]:
                        return None  # Conflict detected
                    parse_table[nt][terminal] = rule

            if "''" in rule_first:
                for terminal in follow[nt]:
                    if terminal in parse_table[nt]:
                        return None  # Conflict detected
                    parse_table[nt][terminal] = rule

    return parse_table

def tokenize_input(input_string):
    tokens = []
    i = 0
    while i < len(input_string):
        if input_string[i].isspace():  # Ignore spaces
            i += 1
            continue
        if input_string[i:i+2] == "id":  # Match 'id' as a single token (if needed)
            tokens.append("id")
            i += 2
        elif input_string[i] in "+*()":  # Match other terminal symbols
            tokens.append(input_string[i])
            i += 1
        elif input_string[i].isalpha():
            tokens.append(input_string[i])
            i += 1
        else:
            raise ValueError(f"Unexpected character '{input_string[i]}' in input string.")
    return tokens

def parse_input_string(input_string, parse_table, start_symbol, terminals):
    stack = ["$"]
    stack.append(start_symbol)

    input_string.append("$")
    pointer = 0
    error_corrected = False

    print("\nParsing Steps:")
    print(f"{'Stack':<20}{'Input':<20}{'Action':<20}")

    while stack:
        top = stack[-1]
        current_input = input_string[pointer]

        print(f"{str(stack):<20}{' '.join(input_string[pointer:]):<20}", end="")

        if top == current_input:
            stack.pop()
            pointer += 1
            print("Match")
        elif top in terminals or top == "$":
            print("Error: Unexpected symbol")
            return "Error"
        elif current_input in parse_table[top]:
            stack.pop()
            production = parse_table[top][current_input]
            print(f"Output {top} -> {production}")
            for symbol in reversed(production.split()):
                if symbol != "''":
                    stack.append(symbol)
        else:
            print("Error: No rule for symbol")
            error_corrected = True
            stack.pop()

    if pointer == len(input_string) and not stack:
        if error_corrected:
            print("Input string accepted with error correction.")
        else:
            print("Input string successfully parsed.")
        return "accept"
    else:
        print("Error: Input string not fully consumed.")
        return "Error"

def main():
    print("Enter grammar rules (empty line to end):")
    grammar = {}
    non_terminals = set()
    terminals = set()

    while True:
        line = input().strip()
        if not line:
            break
        head, productions = map(str.strip, line.split('->'))
        non_terminals.add(head)
        grammar.setdefault(head, []).extend(prod.strip() for prod in productions.split('|'))

    for head, rules in grammar.items():
        for rule in rules:
            for symbol in rule.split():
                if not symbol.isupper() and symbol != "''" and symbol not in non_terminals:
                    terminals.add(symbol)

    first = compute_first(grammar, non_terminals, terminals)
    follow = compute_follow(grammar, non_terminals, terminals, first)

    print("\nFirst sets:")
    for nt, f_set in first.items():
        print(f"{nt}: {{ {', '.join(sorted(f_set))} }}")

    print("\nFollow sets:")
    for nt, f_set in follow.items():
        print(f"{nt}: {{ {', '.join(sorted(f_set))} }}")

    parse_table = compute_parse_table(grammar, non_terminals, terminals, first, follow)

    if parse_table is None:
        print("\nGrammar is not LL(1)")
    else:
        print("\nParse Table:")
        for nt, rules in parse_table.items():
            for terminal, production in rules.items():
                print(f"M[{nt}, {terminal}] = {production}")

        input_string = input("\nEnter an input string to parse: ").strip()
        tokens = tokenize_input(input_string)
        result = parse_input_string(tokens, parse_table, list(grammar.keys())[0], terminals)
        print(result)

if __name__ == "__main__":
    main()