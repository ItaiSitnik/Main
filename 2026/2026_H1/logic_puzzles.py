import random
import json

def generate_complex_logic_puzzle():
    names = ["Alice", "Bob", "Charlie"]
    
    def get_random_complex_statement(speaker, others):
        o1, o2 = others
        # Using lambda functions to evaluate boolean statements strictly
        structures = [
            {
                "type": "conditional", 
                "text": f"If {o1} is innocent, then {o2} is the demon.", 
                # Logical Implication: P -> Q is equivalent to ~P or Q
                "eval": lambda d: (not (o1 != d)) or (o2 == d)
            },
            {
                "type": "xor", 
                "text": f"Exactly one of {o1} or {o2} is the demon.", 
                "eval": lambda d: (o1 == d) ^ (o2 == d)
            },
            {
                "type": "self_implication", 
                "text": f"If I am innocent, then {o1} is innocent too.", 
                "eval": lambda d: (not (speaker != d)) or (o1 != d)
            },
            {
                "type": "alignment_check", 
                "text": f"{o1} and {o2} do not share the same alignment.", 
                "eval": lambda d: (o1 == d) != (o2 == d)
            }
        ]
        return random.choice(structures)

    while True:
        statements = {}
        for speaker in names:
            others = [n for n in names if n != speaker]
            random.shuffle(others)
            statements[speaker] = get_random_complex_statement(speaker, others)
            
        valid_scenarios = []
        
        # Test every possible deterministic state
        for assumed_demon in names:
            scenario_is_valid = True
            
            for speaker, stmt in statements.items():
                # Evaluate the actual boolean truth of the statement in this reality
                statement_is_true = stmt["eval"](assumed_demon)
                
                # Rule: The demon always lies (False), others always tell the truth (True)
                expected_truthfulness = (speaker != assumed_demon)
                
                if expected_truthfulness != statement_is_true:
                    scenario_is_valid = False
                    break
                    
            if scenario_is_valid:
                valid_scenarios.append(assumed_demon)
                
        # Only return puzzles with a single, mathematically rigorous solution
        if len(valid_scenarios) == 1:
            return {
                "puzzle_type": "boolean_constraints",
                "characters": names,
                "statements": {k: v["text"] for k, v in statements.items()},
                "solution": valid_scenarios[0]
            }

if __name__ == "__main__":
    puzzle = generate_complex_logic_puzzle()
    print(json.dumps(puzzle, indent=4))