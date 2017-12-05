def getVariable(var):
    keys = {}
    with open('.env', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split('=')
            keys[line[0]] = line[1].replace('\n','')
    return (keys[var] if(var in keys.keys()) else None)