import os 
import sys

def writer(directory, filename, content):

	path = os.path.join(os.pardir, directory, filename)

	with open(path, "w") as f : 
		f.write(content)

	return f 


if __name__ == '__main__':

	directory = str(sys.argv[1])
	filename = str(sys.argv[2])

	file = writer(directory,filename,content)
	file.close()

