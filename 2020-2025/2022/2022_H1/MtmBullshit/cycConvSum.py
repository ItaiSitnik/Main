N = 5
for j in range(0, N):
    print("j =",j,end=": ")
    for i in range(0, N):
        print((j-i)%N,end=", ")
    print()
