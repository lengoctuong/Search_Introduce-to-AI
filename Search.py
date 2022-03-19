from turtle import *


# ============================== GLOBAL CONSTANTS/VARIABLES ==============================
# Setup Color
GRAY = 'gray'
BLUE = 'blue'
WHITE = 'white'
BLACK = 'black'
PURPLE = 'purple'
GREEN = 'green'
POLYGONS_COLOR_1 = ['brown', 'yellow', 'orange', 'red', 'violet', 'pink']
POLYGONS_COLOR_2 = ['#CC6600', '#FFFF99', '#FFCC99', '#FF9999', '#FFCCFF', '#FF3399']

# Setup others Constants/Variables
TITLE = 'SEARCH SIMULATION'
LENGTH_UNIT = 15
SOURCE_LABEL = 'S'
GOAL_LABEL = 'G'
INPUT_FILE_NAME = 'input.txt'
ENCODE_FORMAT = 'utf-8'

WIDTH, HEIGHT = 0, 0
SOURCE_COORDINATE = ()
GOAL_COORDINATE = ()
NUM_POLYGONS = 0
POLYGONS = []
PATH_COST = 1


# ============================== SUB FUNCTIONS ==============================
# Read Input File
def read_input_file(fileName):
	global WIDTH, HEIGHT, NUM_POLYGONS, SOURCE_COORDINATE, GOAL_COORDINATE
	file = open(fileName, mode='r', encoding=ENCODE_FORMAT)

	# Read Width/Height
	firstLine = file.readline()
	mazeSize = firstLine.split()
	WIDTH, HEIGHT = int(mazeSize[0]), int(mazeSize[1])

	# Read Source/Goal Coordinate
	secondLine = file.readline()
	sourceGoal = secondLine.split()
	SOURCE_COORDINATE = (int(sourceGoal[0]), int(sourceGoal[1]))
	GOAL_COORDINATE = (int(sourceGoal[2]), int(sourceGoal[3]))

	# Read Number of Polygons
	NUM_POLYGONS = int(file.readline())

	# Read Obstacles
	for i in range (NUM_POLYGONS):
		line = file.readline()
		polygon = line.split()
		temp = []

		for j in range (len(polygon)//2):
			temp.append((int(polygon[2 * j]), int(polygon[2 * j + 1])))
		POLYGONS.append(temp)

# Draw Rectangle
def rectangle(width, height):
	pen.setheading(0)
	pen.down()
	pen.forward(width)
	pen.right(90)
	pen.forward(height)
	pen.right(90)
	pen.forward(width)
	pen.right(90)
	pen.forward(height)
	pen.right(90)

# Fill Color for a Block
def fill_block(coordinate, color):
	pen.up()
	pen.goto(LENGTH_UNIT * coordinate[0], LENGTH_UNIT * (coordinate[1] + 1))

	pen.fillcolor(color)
	pen.begin_fill()
	rectangle(LENGTH_UNIT, LENGTH_UNIT)
	pen.end_fill()

# Mark a symbol for a Block
def mark_block(coordinate, symbol, color):
	pen.up()
	pen.goto(LENGTH_UNIT * coordinate[0] + 5, LENGTH_UNIT * coordinate[1])
	pen.pencolor(color)
	pen.write(symbol, False, align='left')
	pen.pencolor(BLACK)

# Draw and fill color for Source and Goal
def drawFillColorSourceGoal(sourceState, sourceLabel, goalState, goalLable, blockColor, labelColor):
	fill_block(sourceState, blockColor)
	mark_block(sourceState, sourceLabel, labelColor)
	fill_block(goalState, blockColor)
	mark_block(goalState, goalLable, labelColor)

# Add new Obstacles between two Obstacles and Fill Color it
def add_obstacles(obstacle1, obstacle2, polygons, color):
	deltaWidth, deltaHeight = obstacle2[0] - obstacle1[0], obstacle2[1] - obstacle1[1]
	x, y = obstacle1[0], obstacle1[1]

	# Cross move
	while (x != obstacle2[0] and y != obstacle2[1]):
		if deltaWidth > 0 and deltaHeight > 0:
			x = x + 1
			y = y + 1
		elif deltaWidth > 0 and deltaHeight < 0:
			x = x + 1
			y = y - 1
		elif deltaWidth < 0 and deltaHeight > 0:
			x = x - 1
			y = y + 1
		else:
			x = x - 1
			y = y - 1

		if ((x, y) != obstacle2):
			polygons.append((x, y))
			fill_block((x, y), color)

	# Vertical/Horizontal Move
	if x == obstacle2[0] and y < obstacle2[1]:
		for i in range(y + 1, obstacle2[1]):
			polygons.append((x, i))
			fill_block((x, i), color)

	if x == obstacle2[0] and y > obstacle2[1]:
		for i in range(obstacle2[1] + 1, y):
			polygons.append((x, i))
			fill_block((x, i), color)

	if y == obstacle2[1] and x < obstacle2[0]:
		for i in range(x + 1, obstacle2[0]):
			polygons.append((i, y))
			fill_block((i, y), color)

	if y == obstacle2[1] and x > obstacle2[0]:
		for i in range(obstacle2[0] + 1, x):
			polygons.append((i, y))
			fill_block((i, y), color)


# ============================== CLASS & MAIN FUNCTIONS ==============================
# Class:Problem is problem of task
class Problem:
	def __init__(self, width, height, sourceState, model, goalState, pathCost):
		self.width = width
		self.height = height
		self.sourceState = sourceState
		self.model = model
		self.goalState = goalState
		self.pathCost = pathCost

	# Calculate actions can have from one state
	def actions(self, state):
		actionsLst = []
		if self.result(state, 'up') != (-1, -1):
			actionsLst.append('up')
		if self.result(state, 'right') != (-1, -1):
			actionsLst.append('right')
		if self.result(state, 'down') != (-1, -1):
			actionsLst.append('down')
		if self.result(state, 'left') != (-1, -1):
			actionsLst.append('left')

		return actionsLst

	# Calculate result of new state by action
	def result(self, state, action):
		# Calculate result of new state by action
		childX, childY = 0, 0
		if action == 'up':
			if state[1] == HEIGHT - 1:
				childX, childY = -1, -1
			else:
				childX, childY = state[0], state[1] + 1
		elif action == 'right':
			if state[0] == WIDTH - 1:
				childX, childY = -1, -1
			else:
				childX, childY = state[0] + 1, state[1]
		elif action == 'down':
			if state[1] == 1:
				childX, childY = -1, -1
			else:
				childX, childY = state[0], state[1] - 1
		elif action == 'left':
			if state[0] == 1:
				childX, childY = -1, -1
			else:
				childX, childY = state[0] - 1, state[1]
		else:
			childX, childY = -1, -1

		# New state at obstacle -> invalid state, assigned = (-1, -1)
		if (childX, childY) in self.model:
			childX, childY = -1, -1

		return (childX, childY)

# Class::Node for each position
class Node:
	def __init__(self, state = (), parent = 0, action = '', pathCost = 0):
		self.state = state
		self.parent = parent
		self.action = action
		self.pathCost = pathCost

# Move to new node with action 'action'
def child_node(problem, parent, action):
	childNode = Node(problem.result(parent.state, action), parent, action, parent.pathCost + problem.pathCost)
	return childNode

# Check whether node have in frontier
def nodeHaveInFrontier(node, frontier):
	for e in frontier:
		if node.state == e.state:
			return 1

	return 0

# Calculate manhattan distance between two node
def HeuristicFunction(node, goalState):
	return abs(goalState[0] - node.state[0]) + abs(goalState[1] - node.state[1])

# Calculate evaluation between two node
def EvaluationFunction(node, goalState):
	return node.pathCost + HeuristicFunction(node, goalState)

# Pop node with min evaluation of frontier
def popMinEvaluation(search, goalState, frontier):
	temp = Node()
	min = 2147483647

	if len(frontier) == 0:
		return temp

	if search == 'BFS':
		min = frontier[0]
	else:
		for i in range(len(frontier)):
			if search == 'UCS' and frontier[i].pathCost < min:
				min = frontier[i].pathCost
			if search == 'GBFS' and HeuristicFunction(frontier[i], goalState) < min:
				min = HeuristicFunction(frontier[i], goalState)
			if search == 'ASS' and EvaluationFunction(frontier[i], goalState) < min:
				min = EvaluationFunction(frontier[i], goalState)

	if search == 'BFS':
		temp = frontier[0]
		frontier.remove(frontier[0])
	else:
		for i in range(len(frontier)):
			if search == 'UCS' and frontier[i].pathCost == min or search == 'GBFS' and HeuristicFunction(frontier[i], goalState) == min or search == 'ASS' and EvaluationFunction(frontier[i], goalState) == min:
				temp = frontier[i]
				frontier.remove(frontier[i])
				break

	return temp

# Check whether a node have in frontier and node in frontier have higher evaluation this node
def nodeHaveInFrontierWithHigherEvaluation(search, node, goalState, frontier):
	for e in frontier:
		if node.state == e.state and (search == 'UCS' and node.pathCost < e.pathCost or search == 'ASS' and EvaluationFunction(node, goalState) < EvaluationFunction(e, goalState)):
			return 1

	return 0

# Replace a node have higher evaluation and same state with other node in frontier
def replaceNodeWithHigherEvaluation(search, node, goalState, frontier):
	for i in range (len(frontier)):
		if node.state == frontier[i].state and (search == 'UCS' and node.pathCost < frontier[i].pathCost or search == 'ASS' and EvaluationFunction(node, goalState) < EvaluationFunction(frontier[i], goalState)):
			frontier[i] = node
			break

# Algorithm for BFS
def BFS(problem, mode):
	node = Node(problem.sourceState, 0, '', 0)
	if problem.goalState == node.state:
		print('===== COST = ' + str(childNode.pathCost) + ' =====')
		return 1

	frontier = []
	frontier.append(node)
	explored = []
	
	while 1:
		if len(frontier) == 0:
			return 0
			
		node = popMinEvaluation('BFS', problem.goalState, frontier)
		explored.append(node.state)
		if mode == 1:
			fill_block(node.state, GREEN)
		
		for action in problem.actions(node.state):
			childNode = child_node(problem, node, action)

			if childNode.state not in explored and not nodeHaveInFrontier(childNode, frontier):
				if problem.goalState == childNode.state:
					print('===== COST = ' + str(childNode.pathCost) + ' =====')

					while childNode.parent != 0:
						childNode = childNode.parent
						if childNode.state != problem.sourceState:
							mark_block(childNode.state, '+', BLACK)

					if mode == 1:
						drawFillColorSourceGoal(problem.sourceState, SOURCE_LABEL, problem.goalState, GOAL_LABEL, BLUE, WHITE)
					
					return 1
					
				frontier.append(childNode)
				if mode == 1:
					fill_block(childNode.state, PURPLE)

# Algorithm for UCS
def UCS(problem, mode):
	node = Node(problem.sourceState, 0, '', 0)
	frontier = []
	frontier.append(node)
	explored = []

	while 1:
		if len(frontier) == 0:
			return 0
			
		node = popMinEvaluation('UCS', problem.goalState, frontier)
		if problem.goalState == node.state:
			print('===== COST = ' + str(node.pathCost) + ' =====')

			while node.parent != 0:
				node = node.parent
				if node.state != problem.sourceState:
					mark_block(node.state, '+', BLACK)

			if mode == 1:
				drawFillColorSourceGoal(problem.sourceState, SOURCE_LABEL, problem.goalState, GOAL_LABEL, BLUE, WHITE)

			return 1
			
		explored.append(node.state)
		if mode == 1:
			fill_block(node.state, GREEN)
		
		for action in problem.actions(node.state):
			childNode = child_node(problem, node, action)

			if childNode.state not in explored and not nodeHaveInFrontier(childNode, frontier):
				frontier.append(childNode)
				if mode == 1:
					fill_block(childNode.state, PURPLE)

			if nodeHaveInFrontierWithHigherEvaluation('UCS', childNode, problem.goalState, frontier):
				replaceNodeWithHigherEvaluation('UCS', childNode, problem.goalState, frontier)

# Algorithm for Greedy best first search
def IDS(problem, mode):
	input()

# Algorithm for Greedy best first search
def GBFS(problem, mode):
	node = Node(problem.sourceState, 0, '', 0)
	frontier = []
	frontier.append(node)
	explored = []

	while 1:
		if len(frontier) == 0:
			return 0
			
		node = popMinEvaluation('GBFS', problem.goalState, frontier)
		if problem.goalState == node.state:
			print('===== COST = ' + str(node.pathCost) + ' =====')

			while node.parent != 0:
				node = node.parent
				if node.state != problem.sourceState:
					mark_block(node.state, '+', BLACK)

			if mode == 1:
				drawFillColorSourceGoal(problem.sourceState, SOURCE_LABEL, problem.goalState, GOAL_LABEL, BLUE, WHITE)

			return 1
			
		explored.append(node.state)
		if mode == 1:
			fill_block(node.state, GREEN)
		
		for action in problem.actions(node.state):
			childNode = child_node(problem, node, action)

			if childNode.state not in explored and not nodeHaveInFrontier(childNode, frontier):
				frontier.append(childNode)
				if mode == 1:
					fill_block(childNode.state, PURPLE)

# Algorithm for A* search
def ASS(problem, mode):
	node = Node(problem.sourceState, 0, '', 0)
	frontier = []
	frontier.append(node)
	explored = []

	while 1:
		if len(frontier) == 0:
			return 0
			
		node = popMinEvaluation('ASS', problem.goalState, frontier)
		if problem.goalState == node.state:
			print('===== COST = ' + str(node.pathCost) + ' =====')

			while node.parent != 0:
				node = node.parent
				if node.state != problem.sourceState:
					mark_block(node.state, '+', BLACK)

			if mode == 1:
				drawFillColorSourceGoal(problem.sourceState, SOURCE_LABEL, problem.goalState, GOAL_LABEL, BLUE, WHITE)

			return 1
			
		explored.append(node.state)
		if mode == 1:
			fill_block(node.state, GREEN)
		
		for action in problem.actions(node.state):
			childNode = child_node(problem, node, action)

			if childNode.state not in explored and not nodeHaveInFrontier(childNode, frontier):
				frontier.append(childNode)
				if mode == 1:
					fill_block(childNode.state, PURPLE)

			if nodeHaveInFrontierWithHigherEvaluation('ASS', childNode, problem.goalState, frontier):
				replaceNodeWithHigherEvaluation('ASS', childNode, problem.goalState, frontier)


# ============================== MAIN::CHOICE ALGORITHM AND MODE ==============================
# Choice algorithm
print('Algorithms:')
print(' - [1] Breadth-first search')
print(' - [2] Uniform-cost search')
print(' - [3] Iterative deepening searh')
print(' - [4] Greedy best-first search')
print(' - [5] A* search')

algorithm = int(input('Choice your algorithm: '))
while algorithm < 1 or algorithm > 5:
	algorithm = int(input('Your choice is invalid, please choose again: '))

# Choice mode
print('\nModes:')
print(' - [0] Find path')
print(' - [1] Step by step')

mode = int(input('Choice your mode: '))
while mode != 0 and mode != 1:
	mode = int(input('Your choice is invalid, please choose again: '))


# ============================== MAIN::CREAT MAZE ==============================
read_input_file(INPUT_FILE_NAME)

# Setup Screen & Pencil
screen = Screen()
screen.title(TITLE)
pen = Turtle()
pen.speed('fastest')

# Draw & Fill Color for Frame
# Rectangle 1
pen.up()
pen.goto(0, LENGTH_UNIT)

pen.fillcolor(GRAY)
pen.begin_fill()
rectangle((WIDTH + 1) * LENGTH_UNIT, LENGTH_UNIT)
pen.end_fill()

# Rectangle 2
pen.up()
pen.goto(WIDTH * LENGTH_UNIT, (HEIGHT + 1) * LENGTH_UNIT)

pen.fillcolor(GRAY)
pen.begin_fill()
rectangle(LENGTH_UNIT, (HEIGHT + 1) * LENGTH_UNIT)
pen.end_fill()

# Rectangle 3, 4
pen.up()
pen.goto(0, (HEIGHT + 1) * LENGTH_UNIT)

pen.fillcolor(GRAY)
pen.begin_fill()
rectangle((WIDTH + 1) * LENGTH_UNIT, LENGTH_UNIT)
rectangle(LENGTH_UNIT, (HEIGHT + 1) * LENGTH_UNIT)
pen.end_fill()

# Draw Chessboard
for i in range (HEIGHT + 2):
	pen.up()
	pen.goto(0, (HEIGHT + 1) * LENGTH_UNIT - i * LENGTH_UNIT)
	pen.down()
	pen.forward((WIDTH + 1) * LENGTH_UNIT)

pen.setheading(270)
for i in range (WIDTH + 2):
	pen.up()
	pen.goto(0 + i * LENGTH_UNIT, (HEIGHT + 1) * LENGTH_UNIT)
	pen.down()
	pen.forward((HEIGHT + 1) * LENGTH_UNIT)
pen.setheading(0)

# Draw & Fill Color Source/Goal
drawFillColorSourceGoal(SOURCE_COORDINATE, SOURCE_LABEL, GOAL_COORDINATE, GOAL_LABEL, BLUE, WHITE)

# Fill Color Obstacles
for i in range (len(POLYGONS)):
	for j in range (len(POLYGONS[i])):
		fill_block(POLYGONS[i][j], POLYGONS_COLOR_1[i % (len((POLYGONS_COLOR_1)))])

# Draw Polygons
temp = POLYGONS.copy()
POLYGONS.clear()

for i in range (len(temp)):
	for j in range (len(temp[i]) - 1):
		POLYGONS.append(temp[i][j])
		add_obstacles(temp[i][j], temp[i][j + 1], POLYGONS, POLYGONS_COLOR_2[i])

	POLYGONS.append(temp[i][len(temp[i]) - 1])
	add_obstacles(temp[i][len(temp[i]) - 1], temp[i][0], POLYGONS, POLYGONS_COLOR_2[i])


# ============================== MAIN::START SEARCH ==============================
problem = Problem(WIDTH, HEIGHT, SOURCE_COORDINATE, POLYGONS, GOAL_COORDINATE, PATH_COST)
print()

if algorithm == 1:
	BFS(problem, mode)
elif algorithm == 2:
	UCS(problem, mode)
elif algorithm == 3:
	IDS(problem, mode)
elif algorithm == 4:
	GBFS(problem, mode)
else:
	ASS(problem, mode)

print('\'press Enter to end\'')
input()