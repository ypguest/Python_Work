import re
AA = '[donghu,V03],[donghu1,V04],[donghu1,V04]'
a = re.split('//[|//]', AA)
print(a)