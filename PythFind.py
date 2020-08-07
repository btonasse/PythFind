import time
from console.utils import cls

class Grid():
	def __init__(self, rows, cols, goal, pos, walls=()):
		self.rows = rows
		self.cols = cols
		self.coords = dict()
		self.goal = goal 
		self.pos = pos 
		for x in range(self.rows):
			for y in range(self.cols):
				if x in [0, self.rows-1] or y in [0, self.cols-1]:
					self.coords[(x,y)] = '#'
				else:
					self.coords[(x,y)] = '.'
		self.coords[self.goal] = 'X'
		self.coords[self.pos] = '@'
		self.orig_grid = dict()
		self.path = []
		self.pqueue = {}
	
	def buildWalls(self, walls):
		for coord in walls:
			self.coords[(coord[0],coord[1])] = '#'
		self.orig_grid = {k:v for (k,v) in self.coords.items()}

	

	def printGrid(self, grid):
		toprint = ''
		for x in range(self.rows):
			line = ''
			for y in range(self.cols):
				line += grid[(x,y)]
			toprint += line + '\n'
		print(toprint, end='')
		return toprint
		

	def calcDistance(self, pos, goal):
		xdiff = abs(goal[0]-pos[0])
		ydiff = abs(goal[1]-pos[1])
		return xdiff+ydiff

	def findNeighbors(self, pos):
		neighs = []
		for x in [-1,0,1]:
			for y in [-1,0,1]:
				new = (pos[0]+x,pos[1]+y)
				if new != pos and self.coords[new] in ['.','X']:
					neighs.append(new)
		return neighs

	def isDiagonal(self, pos, neigh):
		xdiff = abs(neigh[0]-pos[0])
		ydiff = abs(neigh[1]-pos[1])
		if xdiff > 0 and ydiff > 0:
			return True

	def queueNeighbors(self, pos, goal, steps):
		if pos == goal:
			return False
		queue = dict()
		neighbors = self.findNeighbors(pos)
		for neigh in neighbors:
			queue[neigh] = {'cost':self.calcDistance(neigh, goal)+steps, 'via':pos}
			if self.isDiagonal(pos, neigh):
				queue[neigh]['cost'] += 0.1
		queue = dict(sorted(list(queue.items()), key=lambda x: x[1]['cost'], reverse=True)) 
		
		return queue

	def buildQueue(self, start, goal, steps=1):
		if start == goal:
			return True
		cands = self.queueNeighbors(start, goal, steps)
		for coord, value in cands.items():
			if coord not in self.pqueue.keys() or self.pqueue[coord]['cost'] > value['cost']:
				self.pqueue[coord] = value
				self.buildQueue(coord, goal, steps+1)

	def buildPath(self, lastcoord, start):
		if lastcoord == start:
			for coord in self.path:
				self.coords[coord] = '*'
			return 
		self.path.insert(0, lastcoord)
		self.buildPath(self.pqueue[lastcoord]['via'], self.pos)

	def findPath(self, start, goal, prnt=False):
		if prnt:
			self.printGrid(self.coords)
			print(f"Start: {start}. Goal: {goal}. Looking for path...\n")
		search_start = time.time()
		self.buildQueue(start,goal,1)
		search_end = time.time()
		elapsed = round(search_end-search_start, 4)
		try:
			self.buildPath(goal,start)
			if prnt:
				print("Final path:")
				self.printGrid(self.coords)
				print(f"Search time: {elapsed}s")
			return elapsed
		except KeyError:
			print(f"No valid path from {start} to {goal}")

	def printFrames(self, orig_grid, path, elapsed):
		cls()
		self.printGrid(orig_grid)
		orig_grid[self.pos] = '*'
		time.sleep(0.5)
		for step in path:
			cls()
			orig_grid[step] = '@'
			self.printGrid(orig_grid)
			orig_grid[step] = '*'
			time.sleep(0.5)
		print(f'Finished after {len(path)} steps! Search time: {elapsed}s')
			
			

wall1 = [(1, 12), (1, 13), (2, 12), (2, 13), (3, 12), (3, 13), (3, 14), (3, 15), (4, 15), (5, 12), (5, 13), (5, 14), (5, 15), (6, 12), (6, 13), (7, 12), (7, 13)]
wall2 = [(2,2),(2,3),(2,4),(2,5),(2,7),(2,8),(2,9),(2,10),(2,11),(2, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),(2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (8,13),(9, 13)]
wall3 = [(2,2),(2,3),(2,4),(2,5),(2,7),(2,8),(2,9),(2,10),(2,11),(2,12),(2,13),(2,14),(2,15),(2,16),(2,17),(3,17),(3,18),(3,19),(3,20),(2, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),(2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (8,13)]
if __name__ == '__main__':
	a = Grid(11,22, (2,18), (3,3))
	a.buildWalls(wall1)
	elapsed = a.findPath(a.pos, a.goal)
	a.printFrames(a.orig_grid, a.path, elapsed)
	
	'''
	print('\n\n')
	b = Grid(11,22, (2,18), (3,3))
	b.buildWalls(wall2)
	b.findPath(b.pos, b.goal, True)
	#b.printFrames(b.orig_grid, b.path)
	print('\n\n')
	c = Grid(11,22, (2,18), (3,3))
	c.buildWalls(wall3)
	c.findPath(c.pos, c.goal, True)
	#c.printFrames(c.orig_grid, c.path)
	'''
	
	
	

	

	input('')

