def adder(a,b):
    return a+b

def main():
    print(adder(3,4))
    
if __name__ == "_main_":
    main()
    
def calculator(number,operator):
    if operator=="//" :
        return number // 2
    
    elif operator=="/":
        return  number/ 2
    
    elif operator=="+":
        return number+2
    
    elif operator=="-":
        return number-2
    
    elif operator=="*":
        return number*2
    
    elif operator=="%":
        return number%2
    
    
    print(calculator(2,4))