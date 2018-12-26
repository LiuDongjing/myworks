import numpy as np
for c in range(1000):
    N = 0
    exp = ''
    if np.random.choice([True, False]):
        N = np.random.randint(1, 20)
        for k in range(N):
            op = np.random.choice(['+', '*'])
            num = np.random.randint(0, 10**9)
            exp += ' '+str(np.random.choice([op, num]))
    else:
        N = np.random.choice(range(1, 20, 2))
        for k in range(N):
            t = None
            if k%2 == 0:
                t = np.random.randint(0, 10**9)
            else:
                t = np.random.choice(['+', '*'])
            exp += ' '+str(t)
    print(N)
    print(exp)
