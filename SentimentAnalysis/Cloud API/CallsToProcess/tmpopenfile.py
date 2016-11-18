call_text = open('1.txt', 'r')
ret = []

customertext = []

for line in call_text:
  if line[:9] == 'Customer:':
	customertext.append(line[9:])
customertext = ''.join(map(str, customertext))

print(customertext)
print(len(customertext))