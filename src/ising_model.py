import numpy as np 


# num_nums, num_colors = map(int,  
#     input('''Enter number of numbers to partition, 
#     and the number of colors to use: ''')
#     .split(' ')
#     ); 
num_nums, num_colors = 3, 2
x = 2*np.random.randint(low=0, high=2, size=[num_nums, num_colors]) - 1
print(f'Retrieved {num_nums, num_colors}')
print(x.T)
print(x.shape)

def hamiltonian(x: np.array) -> np.array: 
    N, n = x.shape
    term_A, term_B = 0, 0

    for c in range(n):  
        for i in range(N): 
            for j in range(N-i) :
                term_B = term_B + x[i][c]*x[j][c]*x[i+j,c]*np.abs(i-j)
    H = term_A + term_B
    return H


def decode(x: np.array) -> dict: 
    N, n = x.shape
    check_value = 1 + (n-1)*(-1)
    print(f'Check sum: {np.sum(x, axis=1)}')
    if ( np.sum(x, axis=1) != np.ones([n,1])*check_value ).any(): 
        print('Invalid coloring')
        return {} # an empty dictionary for now
    
    # Otherwise, we're good to decode: 
    coloring = dict.fromkeys(range(1,N+1),0)
    for i in range(N): 
        coloring[i+1] = int(np.where(x[i,:] > 0)[0])
    return coloring

print( hamiltonian(x) )
test_coloring = np.array( [[1,-1], [-1, 1]] ); 
print(decode(test_coloring))