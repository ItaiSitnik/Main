import random

from turing_machine import turing_machine

Q = {"q_0", "q^0", "q^00", "q", "q_Y", "q_N", "q_f"}
Gamma = {"0", "1", "*", "Y", "N", "b"}
delta = {
    ("q_0", "0"): ("q^0", "*", "R"),
    ("q_0", "1"): ("q", "*", "R"),
    ("q_0", "b"): ("q_f", "N", "R"),
    ("q^0", "0"): ("q^00", "0", "R"),
    ("q^0", "1"): ("q", "1", "R"),
    ("q^0", "b"): ("q_N", "b", "S"),
    ("q^00", "0"): ("q_Y", "0", "S"),
    ("q^00", "1"): ("q", "1", "R"),
    ("q^00", "b"): ("q_N", "b", "S"),
    ("q", "0"): ("q^0", "0", "R"),
    ("q", "1"): ("q", "1", "R"),
    ("q", "b"): ("q_N", "b", "S"),
    ("q_Y", "0"): ("q_Y", "Y", "L"),
    ("q_Y", "1"): ("q_Y", "Y", "L"),
    ("q_Y", "*"): ("q_f", "Y", "R"),
    ("q_N", "0"): ("q_N", "N", "L"),
    ("q_N", "1"): ("q_N", "N", "L"),
    ("q_N", "b"): ("q_N", "N", "L"),
    ("q_N", "*"): ("q_f", "N", "R"),
}

M = turing_machine(Q=Q, Gamma=Gamma, delta=delta)
output = M.run("00101000110", print_configuration=True)
print(f"{output = }")

for _ in range(20):
    print(f"--------------------")
    input = "".join(random.choice("01") for _ in range(10))
    output = M.run(input)
    print(f"{input} -> {output}")
