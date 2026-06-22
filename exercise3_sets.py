beverages = set(["tea", "coffee", "juice"])
beverages.update(["water", "soda"])
print(beverages)

mySet = {"oven", "kettle", "microwave", "refrigerator"}
print("microwave" in mySet)

mySet.discard("kettle")
print(mySet)

for item in mySet:
    print(item)

s = set(["a", "b", "c", "d"])
lst = ["x", "y"]
s.update(lst)
print(s)

ages = {20, 30}
first_names = {"Ann", "Ben"}
print(ages.union(first_names))
