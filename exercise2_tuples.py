x = ("samsung", "iphone", "tecno", "redmi")
print("samsung")

print(x[-2])

lst = list(x)
lst[1] = "itel"
x = tuple(lst)
print(x)

x = tuple(list(x) + ["Huawei"])
print(x)

for item in x:
    print(item)

lst = list(x)
if lst:
    lst.pop(0)
x = tuple(lst)
print(x)

cities = tuple(["Kampala", "Entebbe", "Jinja", "Gulu"])
print(cities)
a, b, c, d = cities
print(a, b, c, d)

print(cities[1:4])

t1 = ("Ann", "Ben")
t2 = ("Kato", "Moses")
print(t1 + t2)

colors = ("red", "green")
print(colors * 3)

thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)
print(thistuple.count(8))
