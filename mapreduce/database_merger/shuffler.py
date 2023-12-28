import sys

def main():
    dictionnary = {}
    for line in sys.stdin:
        key, value = line.strip("\n").split("@")
        if key in dictionnary:
            dictionnary[key] += [value]
        else:
            dictionnary[key] = [value]

    for key, value in dictionnary.items():
        print(key + "@" + ";".join(value), flush = True)

if __name__ == "__main__":
    main()
