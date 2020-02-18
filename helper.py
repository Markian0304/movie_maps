def read_file(path):
    """
    (str) -> (list)
    Return list of lines from file
    """
    try:
        with open(path, "r") as f:
            return f.read().split('\n')
    except Exception as ex:
        print(ex)
        exit()

def films(lines_list, year, country):
    """
    (list, int, string) -> list
    Возвращает список с названиями фильмов, снятыми в указанный год
    в указанной стране
    """
    result = []
    for line in lines_list:
        if '(' not in line:
            continue
        y = line[line.index('(')+1:line.index(')')]
        if y.isdecimal() and year == int(y):
            name = line[:line.index('(')]    
            part = line.strip().split('\t')
            if '(' in part[-1]:
                adress = part[-2]
            else:
                adress = part[-1]
            try:
                if country == adress.split()[-1]:
                    result.append((name, adress))
            except Exception as ex:
                pass
                
    return result


if __name__ == '__main__':
    ls = read_file('locations.list')
    for i in films(ls, 1999, 'Ukraine')[:5]:
        print(i)

