height = int(input("Introduce a height: "))
mashNum = ""

for i in range(1, height+1):
    reversedMashNum = ""
    
    for j in reversed(mashNum):
        reversedMashNum += j 
          
    print(f" " * (height - i) + mashNum + str(i) + reversedMashNum)
    mashNum += str(i)