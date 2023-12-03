import time
from concurrent.futures import ThreadPoolExecutor


class Foo:

    def __init__(self) -> None:
        super().__init__()
        self.x = 1


# Funkcja dla wątków
def wykonaj_operacje(element):
    print(f"Operacja na elemencie: {element}")
    time.sleep(1)
    print(f"Zakończono operację na elemencie: {element}")


# Kolekcja obiektów
moja_kolekcja = ['a', {"asd": 1}, Foo()]

# Użycie ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(wykonaj_operacje, moja_kolekcja)

print("Wszystkie wątki zakończyły działanie")

if __name__ == '__main__':
    pass
