i_string="my name is jovani georgo but everybody calls me georgo".split(" ")
print(i_string)

for i in i_string:
    print(i)
    
    

join_string="lomi".join(i_string)
print(join_string)

my_list = ["davit", "Davit", "DAVIT", "1234", "Davit's"]


for i in my_list:
    print(i)
    
    

if "Davit" .isupper():
    print("upper")
    
elif "davit" .islower():
    print("lower")
    
elif "1234" .isdigit():
    print("digit")
    
elif "Davit" .istitle():
    print("title")