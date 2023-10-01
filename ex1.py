# Open the file and read text as a list
with open('file_to_read.txt', 'r') as f:
    read_data = f.read()
words = read_data.lower().split(' ')

# Count the number of 'terrible' and print
num_terrible = read_data.lower().count('terrible')
print(num_terrible)

# Check every 'terrible' and change them
i = 1
for index, word in enumerate(words):
    if 'terrible' in word:
        if i % 2 == 1:
            words[index] = word.replace('terrible', 'pathetic')
        else:
            words[index] = word.replace('terrible', 'marvellous')
        i += 1

# Create a new text
new_text = ' '.join(words)
# print(new_text)
with open('result.txt', 'w') as f2:
    f2.write(new_text)
    f2.write(f'The number of \'terrible\' is {num_terrible}')
