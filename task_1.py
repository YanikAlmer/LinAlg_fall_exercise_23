def main():
    #defining text over the matrix
    input_text = ("Your input matrix")
    output_text =("the inverse of your matrix")
    
    matrix = get_input_matrix()
    if matrix is None:
        return
    #printing the inputed matrix
    print_matrix(input_text,matrix)

    check_matrix = check_inverse(matrix)

    
    if check_matrix:
        inverse = calculate_inverse(matrix)
        print_matrix(output_text,inverse)
    else: 
        raise ValueError("the matrix is singular")
        
#gets the matrix from the user and checks if it is a vaid matrix
def get_input_matrix():
    #get the input matrix
    input_matrix = input("type your square matrix in this format a b c;d e f;g h i\n")

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

def check_inverse(matrix): #with help of https://stackoverflow.com/questions/64807423/elimination-matrix-gauss-in-python
    #with gaussian elimination algorithm
    n = len(matrix)
    temp_matrix = [row[:] for row in matrix]
    for i in range(n):
        if temp_matrix[i][i] == 0:
            for j in range(i+1, n):
                if temp_matrix[j][i] != 0:
                    temp_matrix[i], temp_matrix[j] = temp_matrix[j], temp_matrix[i]
                    break
            else:
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
    

def print_matrix(Title, Matrix): #from https://integratedmlai.com/system-of-equations-solution/
    print(Title)
    for row in Matrix:
        print([round(x,2) for x in row])

main()