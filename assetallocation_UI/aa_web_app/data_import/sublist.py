

def sublist():
    a = [[0, 1, 2], [1, 2, 4], [4, 6, 7]]
    t = []
    sum = 0

    for j in range(len(a[0])):
        for i in range(len(a)):
            sum += a[i][j]
        t.append(sum)
        sum = 0

    print()

if __name__ == '__main__':
    sublist()