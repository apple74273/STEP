#!/usr/bin/env python
# coding: utf-8

# In[1]:


class MyStack:
    def __init__(self):
        self.stack = []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        if len(self.stack) == 0:
            return None
        return self.stack.pop()
    def peek(self):
        return self.stack[-1]
    def length(self):
        return len(self.stack)


# In[2]:


#! /usr/bin/python3

# Read a number (including a decimal point if they have any) and creates and returns a token
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


# In[3]:


# Read a plus sign and creates and returns a token
def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


# In[4]:


# Read a minus sign and creates and returns a token
def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


# In[5]:


# Read a multiply sign and creates and returns a token
def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


# In[6]:


# Read a division sign and creates and returns a token
def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


# In[7]:


# Read an open parenthesis and creates and returns a token
def read_open_parenthesis(line, index):
    token = {'type': 'OPEN'}
    return token, index + 1


# In[8]:


# Read an close parenthesis and creates and returns a token
def read_close_parenthesis(line, index):
    token = {'type': 'CLOSE'}
    return token, index + 1


# In[9]:


# Read alphabets, determines which functions is it, and creates and returns a token
def read_alphabet(line, index):
    start = index
    while index < len(line) and line[index].isalpha():
        index += 1
    end = index    
    type = line[start:end]
    
    label = None
    
    if type == 'abs':
        label = 'ABS'
    elif type == 'int':
        label = 'INT'
    elif type == 'round':
        label = 'ROUND'
    else:
        print('Invalid command found from '+start+" to "+end)
        exit(1)
        
    token = {'type':'FUNCTION', 'label': label}
    
    return token, index


# In[10]:


# Divide a line into different tokens and create a list of tokens
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_open_parenthesis(line, index)
        elif line[index] == ')':
            (token, index) = read_close_parenthesis(line, index)
        elif line[index].isalpha():
            (token, index) = read_alphabet(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# In[11]:


# identify a sequence closed by parenthesis and call the calculate_next_sequence function to calculate the value of the sequence
# it also calls check_functions function to apply the function if there is any
def evaluate(tokens):
    stack = MyStack()
    answer = 0
    index = 0
    
    tokens.insert(0, {'type': 'OPEN'}) #dummy token
    tokens.append({'type': 'CLOSE'}) #dumy token
    while index < len(tokens):
        if (tokens[index]['type']=='CLOSE'):
            (answer, stack, tokens, index) = calculate_next_sequence(tokens, stack, index)
            if stack.length()!=0:
                (answer, stack) = check_functions(stack, answer)
                
            tokens.insert(index, {'type': 'NUMBER', 'number': answer})
            
        stack.push(tokens[index])
            
        index += 1
    return answer


# In[12]:


# check whether there is a function or not, and apply it if there is
def check_functions(stack, answer):
    token = stack.peek()
    if token['type']=='FUNCTION':
        stack.pop()
        if token['label']=='ABS':
            if (answer<0):
                answer*=-1
        elif token['label']=='INT':
            absolute_value = answer
            if (answer<0):
                absolute_value *= -1
            absolute_value //= 1
            if (answer<0):
                absolute_value *= -1
            answer = absolute_value
        elif token['label']=='ROUND':
            decimal = answer % 1
            if (decimal>=0.5):
                answer+=1
            answer -= decimal
                
    return answer, stack


# In[13]:


# create a list of tokens in between parenthesis, call a function to calculate its value, and update the list of tokens and stack
def calculate_next_sequence(tokens, stack, index):
    previous_token = stack.pop()
    temp_tokens = []
    length = 2
    while (previous_token['type']!='OPEN'):
        temp_tokens.append(previous_token)
        previous_token = stack.pop()
        length += 1
    temp_tokens.reverse()
            
    (tokens, index) = delete_tokens(tokens, length, index)
    
    answer = calculate(temp_tokens)
    
    return answer, stack, tokens, index


# In[14]:


# delete a sequence of tokens for a given length and update a index correspondingly
def delete_tokens(tokens, length, index):
    for i in range (length):
        tokens.pop(index-i)
    index -= length-1
    return tokens, index


# In[15]:


# calculate a value of the given list of tokens
def calculate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1

    #first go through all multiplications and divisions
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLY' and tokens[index-2]['type']=='NUMBER':
                product = tokens[index-2]['number']*tokens[index]['number']
                (tokens, index) = delete_tokens(tokens, 3, index)
                tokens.insert(index, {'type': 'NUMBER', 'number': product})
            elif tokens[index - 1]['type'] == 'DIVIDE' and tokens[index-2]['type']=='NUMBER':
                quotient = tokens[index-2]['number']/tokens[index]['number']
                (tokens, index) = delete_tokens(tokens, 3, index)
                tokens.insert(index, {'type': 'NUMBER', 'number': quotient})
        index += 1
        
    #second go through all remaining additions and subtractions
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


# In[16]:


# test whether the value got from this program is the same as the expected value
def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# In[17]:


# Add more tests to this function :)
# function to run the tests
def run_test():
    print("==== Test started! ====")
    print()
    print ("==== Test cases for homework 1 ====")
    # pre-existed test cases
    test("1+2")
    test("1.0+2.1-3")
    
    #test cases for inputting a single number
    test ("123.456789")
    test ("-5.2")
    
    #test cases for addition
    test ("1.1+1.9")
    test ("1234.5+67.89")
    
    #test cases for using negative numbers
    test ("1+-5")
    test ("-2+4")
    
    #test cases for subtraction
    test ("1.5-1.0")
    test ("0.5-3.4")
    
    #test cases for mixing addition and subtraction
    test ("1.5+2.0-1.4")
    test ("2.9-4.2+9.7")
    
    #test cases for multiplication
    test ("1.5*5.5")
    test ("3.0*2.0")
    
    #test cases for division
    test ("6.0/2.0") #no remainder
    test ("1.0/3.0") #create repeating decimals
    
    #test cases for mixing multiplication and division
    test ("12*3.6/4")
    test ("60.5/5*2")
    
    #test cases for mixing all four types of calculations
    test ("3.0+4*2-1/5")
    test ("2.5*1.4+1/5+9/5-2/4")
    
    print()
    print ("==== Test cases for homework 3 ====")
    print()
    
    #test cases for one pair of parenthesis
    test ("(1)")
    test ("(1+1)")
    test ("(2-1)")
    test ("(2*3)")
    test ("(4/2)")
    
    #test cases for multiple pairs of parenthesis
    test ("(3.0+4*(2-1))/5")
    test ("(1+1)*(2+2)")
    test ("(4-2)/(4*4)")
    test ("(4/2)+(2-5)")
    
    #test cases for the use of more pairs of parenthesis than necessary
    test ("(((((-5+2)))))")
    
    print()
    print("==== Test cases for homework 4")
    print()
    
    #test cases for using each function only
    test ("abs(-1.4)")
    test ("abs(2.5)")
    test ("int(1.2345)")
    test ("int(2)")
    test ("round(1.4999999)")
    test ("round(1.5000000)")
    
    #test cases for repeating each function
    test ("abs(abs(3.4))")
    test ("int(int(2.3))")
    test ("round(round(1.5))")
    
    #test cases for combining all three functions
    test ("abs(int(2.5))")
    test ("int(abs(-8.3))")
    test ("int(round(2.4))")
    test ("round(int(28.3))")
    test ("round(abs(5.6))")
    test ("abs(round(24.2))")
    test ("int(round(abs(-12.49)))")
    
    #test cases for combining all three functions with addition, subtraction, multiplication, and division
    test ("12*abs(int(round(-1.55)+abs(int(-2.3+4))))")
    test ("abs(round(2.49999+1.0)+int(abs(5*(3+5)*2))/abs(-5/2))")
    
    print()
    print("==== Test finished! ====\n")


# In[18]:


run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)


# In[ ]:




