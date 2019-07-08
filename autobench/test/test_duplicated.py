filename = raw_input('Please enter the filename: ')
file = open(filename, 'r')
processed_filename = 'processed_' + filename
processed = open(processed_filename, 'w')
row = file.read()
length = len(row)
new = list()
for i in range(0, (length+1)/6):
    new.append(row[i*6:i*6+5] + ' ' + row[i*6:i*6+5] + ' ')
final = ''.join(new)
str_length = len(final)
first_forth = final[:str_length/4+3]
second_forth = final[str_length/4+3:str_length/2-1]
third_forth = final[str_length/2:str_length/4*3+3]
forth_forth = final[str_length/4*3+3:]
processed.writelines(first_forth + '\n')
processed.writelines(second_forth + '\n')
processed.writelines(third_forth + '\n')
processed.writelines(forth_forth + '\n')
