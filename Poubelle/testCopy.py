from copy import copy,deepcopy

class OnlyInt:
    def __init__(self):
        self.a = 2
        self.b = 3

    def __str__(self):
        return "a "+ str(self.a)+" b " + str(self.b)

class MoreComplex:
    def __init__(self):
        self.c = 10
        self.d = OnlyInt()
    
    def __str__(self):
        return "c "+ str(self.c)+" d [" + str(self.d) +"]" 





print("obj1 = OnlyInt()")
obj1 = OnlyInt()

print("obj2 = obj1")
obj2 = obj1

print("obj3 = copy(obj1)")
obj3 = copy(obj1)

print("obj4 = deepcopy(obj1)")
obj4 = deepcopy(obj1)

print("obj1 = ",obj1)
print("obj2 = ",obj2)
print("obj3 = ",obj3)
print("obj4 = ",obj4)

print("obj1.a = 12")
obj1.a = 12
print("obj1 = ",obj1)
print("obj2 = ",obj2)
print("obj3 = ",obj3,"obj3 (copy(obj1) est bien indépendant")
print("obj4 = ",obj4,"obj4 (deepcopy(obj1) est bien indépendant")

print()
print()
print()

print("obj1 = MoreComplex()")
obj1 = MoreComplex()

print("obj2 = obj1")
obj2 = obj1

print("obj3 = copy(obj1)")
obj3 = copy(obj1)

print("obj4 = deepcopy(obj1)")
obj4 = deepcopy(obj1)

print("obj1 = ",obj1)
print("obj2 = ",obj2)
print("obj3 = ",obj3)
print("obj4 = ",obj4)

print("obj1.c = 12")
print("obj1.d.a = 24")
obj1.c = 12
obj1.d.a = 24
print("obj1 = ",obj1)
print("obj2 = ",obj2)
print("obj3 = ",obj3, "obj3 (copy(obj1) n'est pas entierement indépendant")
print("obj4 = ",obj4,"obj4 (deepcopy(obj1) est bien indépendant")

