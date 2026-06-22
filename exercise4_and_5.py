i = 5
s = "apples"
print(str(i) + s)

txt = "      Hello,       Uganda!       "
no_spaces = txt.replace(' ', '')
print(no_spaces)

print(txt.upper())

print(txt.replace('U', 'V'))

y = "I am proudly Ugandan"
print(y[1:4])

x = "All \"Data Scientists\" are cool!"
print(x)

Shoes = {
    "brand": "Nick",
    "color": "black",
    "size": 40
}

print(Shoes["size"])

Shoes["brand"] = "Adidas"
Shoes["type"] = "sneakers"
print(list(Shoes.keys()))
print(list(Shoes.values()))

print("size" in Shoes)

for k, v in Shoes.items():
    print(k, v)

Shoes.pop("color", None)
print(Shoes)

Shoes.clear()
print(Shoes)

mydict = {"a": 1, "b": 2}
copy_dict = mydict.copy()
print(copy_dict)

nested = {
    "person1": {"name": "Ann", "age": 20},
    "person2": {"name": "Ben", "age": 22}
}
print(nested)
