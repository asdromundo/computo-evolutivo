import os 
import sys

def writer(directory, filename, content):

	path = os.path.join(os.pardir, directory, filename)
	
	with open(path, "w") as f :
		f.writelines(content)
		#for c in content:  
			#f.write(c)
	f.close() 

def reader(directory,filename):

	path = os.path.join(os.pardir, directory, filename)

	data = []
	
	with open(path) as f:
		for line in f:
			data.append(line)

	return data 

def slice_string_by_character(string, character):
  """Slices a string by a specific character and saves the substrings in an array.

  Args:
    string: The string to slice.
    character: The character to slice the string by.

  Returns:
    A list of substrings.

  """
  substrings = []
  for i in range(len(string)):
    if string[i] == character:
      substrings.append(string[i+1:])

  return substrings

if __name__ == '__main__':

	directory = str(sys.argv[1])
	filename = str(sys.argv[2])

	content = ["Hola", "Como", "Estas"]

	file = writer(directory,filename,content)
	
	data = reader(directory,filename)
	for d in data : 
		print(d)
	print(len(data))
	print(data[0])

