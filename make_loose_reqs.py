
with open('App/requirements.txt', 'r') as f:
    lines = f.readlines()

with open('App/requirements_loose.txt', 'w') as f:
    for line in lines:
        # Keep everything but strip version
        package = line.split('==')[0].strip()
        if package:
            f.write(package + '\n')
