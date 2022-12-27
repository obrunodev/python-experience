from typing import Dict, List, Optional


# Example 01
def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


# Example 02
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age


# Usando módulo typing
def process_items(items: List[str]):
    for idx, item in enumerate(items, start=1):
        print(idx, "-", item.capitalize())


def process_values(prices: Dict[str, float]):
    for item_name, item_price in prices.items():
        print(f"{item_name}: R$ {str(item_price).replace('.', ',')}")


def say_hi(name: Optional[str] = None):
    if name:
        print(f"Hi {name}!")
    else:
        print("Hello world!")


print(get_full_name("Bruno", "Pianca"))
print(get_name_with_age("Bruno", 26))
process_items(["Alicate", "Martelo", "Fita isolante"])
process_values({"produto 1": 10.0, "produto 2": 15.0, "produto 3": 17.9})
say_hi()
say_hi("Bruno")


# Exemplo com classe como tipo
class Person:
    def __init__(self, name: str):
        self.name = name.title()


def get_person_name(one_person: Person):
    return one_person.name


bruno = Person("Bruno")
print(get_person_name(bruno))

