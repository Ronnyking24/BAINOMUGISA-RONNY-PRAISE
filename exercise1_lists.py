names = ["John", "Mary", "Paul", "Rita", "Tom"]
print(names[1])

names[0] = "James"
print(names[0])

names.append("Lily")
print(names)

names.insert(2, "Bathel")
print(names)

del names[3]
print(names)

print(names[-1])

new_list = ["one", "two", "three", "four", "five", "six", "seven"]
print(new_list[2:5])

countries = ["Uganda", "Kenya", "Tanzania", "Rwanda"]
countries_copy = countries.copy()
print(countries_copy)

for country in countries:
    print(country)

animals = ["zebra", "dog", "cat", "elephant", "antelope"]
asc = sorted(animals)
desc = sorted(animals, reverse=True)
print(asc)
print(desc)

print([a for a in animals if 'a' in a])

first_names = ["Anna", "Ben"]
second_names = ["Kato", "Moses"]
joined = first_names + second_names
print(joined)
