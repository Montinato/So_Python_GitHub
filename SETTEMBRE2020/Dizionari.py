
rubrica = { 99 : 9999323424 , 00 : 9999980}

print("Stampo la rubrica ! ")
print (rubrica.items())


print("\n")



# for k in rubrica:
#     print("\n" +"Stampo le chiavi di rubrica: " + str(k) + "\n")
#     if indiceMax == None or rubrica[k] > indiceMax:
#         print("Stampo il valore di rubrica[k] = " + str(rubrica[k]) + "\n")
#         indiceMax = k
#         print("Stampo il valore di indiceMax = " + str(indiceMax) + "\n")
#     t = indiceMax       


# print("Stampo il valore di t = " + str(t) + "\n")

indiceMax = None
maxium = 0    

for k in rubrica:
    if rubrica[k] > maxium:
        indiceMax = k
        maxium = rubrica[k]
        print(str(indiceMax) + "\n")


          


print("Stampo il valore di indiceMax = " + str(indiceMax) + "\n")
        
