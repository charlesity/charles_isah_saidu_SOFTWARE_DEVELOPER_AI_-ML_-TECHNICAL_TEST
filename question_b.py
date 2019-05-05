#software library for version check

def version_check(v1, v2):
    #split the str by . them the resulting arrays together and cast result as int
    version1 = int("".join(v1.split(".")))
    version2 = int("".join(v2.split(".")))

    if version1 > version2:
        return "version "+str(v1)+" is greater than version "+ str(v2)
    elif version1 == version2:
        return "version "+str(v1)+ " and version "+str(v2)+" are the same"
    else:
        return "version "+str(v1)+" is less than version "+ str(v2)

# test
if __name__ == "__main__":
    print (version_check("1.5", "1.6"))
    print (version_check("1.8", "1.6"))
    print (version_check("1.5.3", "1.6.5"))
    print (version_check("1.5.3.0", "1.5.3.0"))
    print (version_check("0.1.5.3", "0.1.5.3"))
    print (version_check("0.1.5.3", "0.1.5.3.3"))