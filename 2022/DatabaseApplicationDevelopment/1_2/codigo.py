from time import sleep

vacinas = ["Giardiase", "Raiva", "V8"]
contador = 0

print("\nPrograma de vacinação do PetShop PuppyBel\n")

while input("Existem animais a serem vacinados? (S/N)\n>>> ").lower() == "s":

    _ = 1
    contador += 1
    print(f"Vacinando animal número <{contador}>")
    for vacina in vacinas:
        print(f"Vacina <{_}> - {vacina} [OK]")
        _ += 1
        sleep(0.75)

    sleep(0.5)

print(f"\nTotal de animais vacinados com sucesso: {contador}\n")
