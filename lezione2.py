lista_numeri=[4,5,6,7,9]
def sum_list(lista_numeri):
    somma=0
    for i in range(len(lista_numeri)):
        somma=somma+lista_numeri[i]
    return somma
print(sum_list(lista_numeri))

    