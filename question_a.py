#accepts tupples line1 and line2
def overlap(line1, line2):
    #sort the first line
    line1.sort() #sort just in case they are not aligned
    line2.sort() #sort just in case they are not aligned

    lines=[line1, line2] #make a list of the two numbers

    #sort them by the first value of each line
    lines.sort(key=sortIndex)    
    #if second index of line1 greater than first index of line2 then they overlap
    return "They overlap" if lines[0][1] > lines[1][0] else "NO overlap"

#custom sort order index - i.e sort is based on first element of list
def sortIndex(v):
    return v[0]


l1 = input("Enter line 1: a list of two numbers separated by space ")
l2 = input("Enter line 1: a list of two numbers separated by space ")
l1 = list(map(int, l1.split())) #split l1, cast its entries to int with map function and return a list of the integers
l2 = list(map(int, l2.split())) #split l1, cast its entries to int with map function and return a list of the integers

print (overlap(l1, l2))



