def main():
    #defining text over the matrix
    input_text = ("Your input matrix")
    output_text =("the solution to the system Ax=b is: \n")
    
    matrix = get_input_matrix()
    if matrix is None:
        return
    #printing the inputed matrix
    print_matrix(input_text,matrix)
    #get the vector b from the user
    input_b = get_input_b()
    print_matrix(input_text,input_b)#print the input b

    #check if the matrix and the vector is in a valid format
    check_matrix = check_inverse(matrix)
    check_vector =check_b(input_b,matrix)
    
    #if the vector or the matrix has a invalid format a error will be raised, if the input is valid Ax=b will be calculated
    if check_matrix:
        inverse = calculate_inverse(matrix)
        if check_vector:
            value_x = multiply_A_inverse_b(inverse, input_b)
            print_matrix(output_text,value_x)
        else:
            raise ValueError("your input vector b is not in the right format")
    else: 
        raise ValueError("the matrix is singular")

    

    
        
#gets the matrix from the user and checks if it is a vaid matrix
def get_input_matrix():
    #get the input matrix
    input_matrix = input("type your square matrix in this format a b;c d: ")

    matrix = []

    try:
        split_matrix = input_matrix.split(';') #convert string into rows
        # Split each row by spaces and convert each element to an integer
        matrix = [list(map(int, row.split())) for row in split_matrix]
        
        # Check if the matrix is square
        num_rows = len(matrix)
        for row in matrix:
            if len(row) != num_rows:
                print("The matrix is not square. Please enter a square matrix.")
                return None
        
        return matrix
    except ValueError:
        print("A Value Error occurred. Please ensure all inputs are integers and try again.")
        return None
    except:
        print(f"An error occurred. Please try again.")
        return None

#get the input vector b form the user
def get_input_b():
    input_b = input("input a vector b in the format a b c d (make sure the lenght of the column of the vector matches the lenght of the rows of the matrix):\n")
    string = input_b.split()#make a list out of the string

    b =[float(num) for num in string] #converte string into integers

    return b

#check if the vector b is valid
def check_b(b, matrix):
    if len(b) == 0:
        return False
    elif len(b) != len(matrix):
        return False
    elif not isinstance(b, list):
        return False
    else:
        return True


def check_inverse(matrix): #with help of https://stackoverflow.com/questions/64807423/elimination-matrix-gauss-in-python
    #with gaussian elimination algorithm
    n = len(matrix)
    temp_matrix = [row[:] for row in matrix]
    for i in range(n):
    
        # Make the diagonal contain all non-zero elements
        if temp_matrix[i][i] == 0:
            for j in range(i+1, n):
                if temp_matrix[j][i] != 0:
                    # Swap rows
                    temp_matrix[i], temp_matrix[j] = temp_matrix[j], temp_matrix[i]
                    break
            else:
                # We found a zero column
                return False
        
        # Make all elements below the pivot in this column to be zero
        for j in range(i+1, n):
            ratio = temp_matrix[j][i] / temp_matrix[i][i]
            for k in range(n):
                temp_matrix[j][k] -= ratio * temp_matrix[i][k]
    
    # If we made it here without finding a zero column, the matrix is non-singular
    return True


def calculate_inverse(matrix):
    n = len(matrix)

    #create the identity matrix (from https://stackoverflow.com/a/73966587)
    identity = [[0] * i + [1] + [0] * (n - i - 1) for i in range(n)]
    #create a augmented matrix
    augmented = [row + identity_row for row, identity_row in zip(matrix, identity)]
    #gauss elimination
    for i in range(n):
        # Make the diagonal contain all non-zero elements
        for j in range(i+1, n):
            if augmented[j][i] != 0:
                # Swap rows
                augmented[i], augmented[j] = augmented[j], augmented[i]
                break
        #make diagonal contain 1's
        diagonal = augmented[i][i]
        for j in range(2*n):
            augmented[i][j] /= diagonal
        
        #make all elements below and above the pivot 0
        for j in range(n):
            if j != i:
                scaler = augmented[j][i]
                for k in range(2*n):
                    augmented[j][k] -= scaler * augmented[i][k]

    #get the inverse out of the augmented matrix
    inverse = [row[n:] for row in augmented]
    return inverse

#from https://stackoverflow.com/questions/28253102/python-3-multiply-a-vector-by-a-matrix-without-numpy, 19.11.23
def multiply_A_inverse_b(inverse, b):
    value_x=[] #initialising a empty list
    for i in range(len(inverse)): #iterates through each row of the matrix inverse
        total = 0
        for j in range(len(inverse[i])): #iterates through the vector b
            total +=inverse[i][j]*b[j] #multipys each element of of the row r[j] with the emelent of the vector b[j] 
        value_x.append(total)

    return value_x

#print out the matrix with its description
def print_matrix(Title, matrix): #from https://integratedmlai.com/system-of-equations-solution/
    print(Title)
    if isinstance(matrix[0], list):  # Check if matrix is a list of lists (i.e., a matrix)
        for row in matrix:
            print([round(x, 2) if isinstance(x, float) else x for x in row])
    else:  # It's a single list (i.e., a vector)
        print([round(x, 2) if isinstance(x, float) else x for x in matrix])
main()