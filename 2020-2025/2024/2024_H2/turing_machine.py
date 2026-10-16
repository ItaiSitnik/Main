class turing_machine:
    def __init__(
        self,
        Q,
        delta,
        q0="q_0",
        F={"q_f"},
        Gamma={"0", "1", "b"},
        Sigma={"0", "1"},
        b="b",
    ):

        if q0 not in Q:
            raise ValueError(f"{q0 = } is not in {Q = }")

        if not F.issubset(Q):
            raise ValueError(f"{F = } is not a subset of {Q = }")

        if not Sigma.issubset(Gamma):
            raise ValueError(f"{Sigma = } is not in {Gamma = }")

        for (cur_state, cur_letter), (
            next_state,
            letter_to_write,
            movement,
        ) in delta.items():

            if cur_state not in (Q - F):
                raise ValueError(f"{cur_state = } is not in {Q - F = }")

            if cur_letter not in Gamma:
                raise ValueError(f"{next_state = } is not in {Gamma = }")

            if next_state not in Q:
                raise ValueError(f"{next_state = } is not in {Q = }")

            if letter_to_write not in Gamma:
                raise ValueError(f"{letter_to_write = } is not in {Gamma = }")

            if movement not in {"L", "R", "S"}:
                raise ValueError(f"{movement = } is not in {{L, R, S}}")

        self.Q = Q
        self.q0 = q0
        self.F = F
        self.Gamma = Gamma
        self.Sigma = Sigma
        self.b = b
        self.delta = delta

    def __get_content(self, tape):
        i = len(tape) - 1
        while i >= 0 and tape[i] == "b":
            i -= 1
        return "".join(tape[:i])

    def run(self, input, print_configuration=False):
        curr_state = self.q0
        i = 0
        tape = list(input) + ["b"] * 3 * len(input)

        counter = 0
        while curr_state not in self.F:
            if print_configuration:
                print(f"C{counter:<2}: [{curr_state}, {i}, {self.__get_content(tape)}]")
            counter += 1

            next_state, letter_to_write, movement = self.delta[curr_state, tape[i]]
            curr_state = next_state
            tape[i] = letter_to_write
            if movement == "L":
                i = max(0, i - 1)
            elif movement == "R":
                i = i + 1

        print(f"END CONFIG: [{curr_state}, {i}, {self.__get_content(tape)}]")
        return "".join(tape[:i])
