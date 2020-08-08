

def parseMaze(path=None):
	try:
		with open(path) as file:
			rawmaze = file.read().splitlines()
	except:
		input("File doesn't seem to exist.")
		return False
	parsedmaze = []
	start = None
	goal = None
	for I, line in enumerate(rawmaze):
		parsedline = ''
		for i, char in enumerate(line):
			if char == '@':
				start = (I,i)
			elif char == 'X':
				goal = (I,i)
			
			if char in '+-|':
				parsedline += '#'
			elif char == ' ':
				parsedline += '.'
			else:
				parsedline += char
		parsedmaze.append(parsedline)
	return parsedmaze, start, goal

if __name__ == '__main__':
	path = ''
	while not path or len(path) < 4 or path[-4:] != '.txt':
		path = input('Which maze do you want to solve? (enter a txt file name)')
	x, y, z = parseMaze(path.strip())
	print(y, z)
	for line in x:
		print(line)
	input()


