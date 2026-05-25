def friedchiken(name):
    return"hello "+ name
print(friedchiken("Nikoloz Bagaturia"))


def fav_animal(animal_name , wich_animal):
    return wich_animal+animal_name
print(fav_animal("ჯიგარსონა","ჯორი"))

def even_or_odd(numbers):

    if  numbers % 2 == 0:
        return(numbers, "luwi")
    else:
        return(numbers, "kenti")

def S(widht,height):
    return widht*height
print(S(5,37))