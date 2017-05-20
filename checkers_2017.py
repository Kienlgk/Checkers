from copy import deepcopy
from time import time

# Constants
MaxUtility = float('inf')
MaxAllowedTimeInSeconds = 2.9
MaxDepth = 100

# ======================== Class CheckersState =======================================
class CheckersState:
	def __init__(self, grid, blackToMove, moves):
		self.grid = grid
		self.blackToMove = blackToMove
		self.moves = moves
		self.str = 'b' if blackToMove else 'r'

# ======================== Class Player =======================================
class Player:
	def __init__(self, str_name):
		self.str = str_name
		self.blackToMove = True if self.str == 'b' else False
		# self.isKingJump = False

	def __str__(self):
		return self.str

	def nextMove(self, state):
		def isTerminalState(state):
			blackSeen, redSeen = False, False
			for row in state.grid:
				for cell in row:
					if cell == 'b' or cell == 'B': blackSeen = True
					elif cell == 'r' or cell == 'R': redSeen = True
					if blackSeen and redSeen: return False
			state.loser = 'r' if blackSeen else 'b'
			return True

		def getTerminalUtility(state):
			return MaxUtility if state.loser != self.str else -MaxUtility

		def evaluationFunc(state):
			black, red = 0, 0
			for row in state.grid:
				for cell in row:
					if cell == 'b': black += 10
					elif cell == 'B': black += 15
					elif cell == 'r': red += 10
					elif cell == 'R': red += 15
			if self.str == 'r': return red - black
			return black - red

		def getSuccessors(state):
			def getSteps(cell):
				rSteps = [(-1, -1), (-1, 1)]
				bSteps = [(1, -1), (1, 1)]
				steps = []
				if cell != 'b': steps.extend(rSteps)
				if cell != 'r': steps.extend(bSteps)
				return steps
			def getJumpSteps():
				Steps = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
				return Steps
			def generateMoves(board, i, j, states):
				t = 0
				# print("init:==========================")
				for step in getSteps(board[i][j]):
					# t = t +1
					# print(t)
					z = 0
					x, y = i, j
					# print(x)
					if board[i][j] == 'R' or board[i][j] == 'B':
						# print("isKing ", board[i][j])
						while 0 <= x and x <= 7 and 0 <= y and y <= 7:
							# z += 1
							x, y = x + step[0], y + step[1]
							# print(z,"/",x,",",y)
							if x >= 0 and x <= 7 and y >= 0 and y <= 7 and board[x][y] == '.':
								boardCopy = deepcopy(board)
								# update board
								boardCopy[x][y], boardCopy[i][j] = boardCopy[i][j], '.'
								# turning to a King
								if (x == 7 and state.str == 'b') or (x == 0 and state.str == 'r'):
									boardCopy[x][y] = boardCopy[x][y].upper()
								# update new state
								states.append(CheckersState(boardCopy, not state.blackToMove, [(i, j), (x, y)]))
					else:
						x, y = x + step[0], y + step[1]
						if x >= 0 and x <= 7 and y >= 0 and y <= 7 and board[x][y] == '.':
							boardCopy = deepcopy(board)
							# update board
							boardCopy[x][y], boardCopy[i][j] = boardCopy[i][j], '.'
							# turning to a King
							if (x == 7 and state.str == 'b') or (x == 0 and state.str == 'r'):
								boardCopy[x][y] = boardCopy[x][y].upper()
							# update new state
							states.append(CheckersState(boardCopy, not state.blackToMove, [(i, j), (x, y)]))

			def generateJumps(board, i, j, moves, states):
				jumpEnd = True
				# if not self.isKingJump:
				if board[i][j] == 'R'or board[i][j] == 'B':
					for step in getJumpSteps():
						x, y = i, j
						while 0 <= x + step[0] and x + step[0] <= 7 and 0 <= y + step[1] and y + step[1] <= 7:
							# prevChar = board[x][y]
							# x, y = x + step[0], y + step[1]
							# if (prevChar != '.' and (x - step[0]) != i and (y - step[1]) != j):
							# 	break
							x, y = x + step[0], y + step[1]
							xNext, yNext = x + step[0], y + step[1]
							if (0 <= xNext and xNext <= 7 and 0 <= yNext and yNext <= 7):
								nextChar = board[xNext][yNext]
								if x >= 0 and x <= 7 and y >= 0 and y <= 7 and board[x][y] != '.' and nextChar != '.':
									break
							# check place end
							if x >= 0 and x <= 7 and y >= 0 and y <= 7 and board[x][y] != '.' and board[i][j].lower() != board[x][y].lower():
								xp, yp = x, y
								while 0 <= xp + step[0] and xp + step[0] <= 7 and 0 <= yp + step[1] and yp <= 7 + step[1]:
									xp, yp = xp + step[0], yp + step[1]
									if xp >= 0 and xp <= 7 and yp >= 0 and yp <= 7 and board[xp][yp] == '.':
										board[xp][yp], save = board[i][j], board[x][y]
										board[i][j] = board[x][y] = '.'
										previous = board[xp][yp]
										# promoted
										if (xp == 7 and state.str == 'b') or (xp == 0 and state.str == 'r'):
											board[xp][yp] = board[xp][yp].upper()
											# self.isKingJump = True

										moves.append((xp, yp))
										if i == 7 and j == 0:
											print("x,y: ",x, ", ", y)
											print("i,j: ",i, ", ", j)
										# print("moves: ----------")
										# for move in moves:
										# 	print(move)
										# print("end moves -------")
										generateJumps(board, xp, yp, moves, states)
										moves.pop()
										board[i][j], board[x][y], board[xp][yp] = previous, save, '.'
										jumpEnd = False
										# self.isKingJump = False
							# end check place end
					if jumpEnd and len(moves) > 1:
						states.append(CheckersState(deepcopy(board), not state.blackToMove, deepcopy(moves)))
				else:
					for step in getJumpSteps():
						x, y = i + step[0], j + step[1]
						if x >= 0 and x <= 7 and y >= 0 and y <= 7 and board[x][y] != '.' and board[i][j].lower() != board[x][y].lower():
							xp, yp = x + step[0], y + step[1]
							if xp >= 0 and xp <= 7 and yp >= 0 and yp <= 7 and board[xp][yp] == '.':
								board[xp][yp], save = board[i][j], board[x][y]
								board[i][j] = board[x][y] = '.'
								previous = board[xp][yp]
								# promoted
								if (xp == 7 and state.str == 'b') or (xp == 0 and state.str == 'r'):
									board[xp][yp] = board[xp][yp].upper()
									# self.isKingJump = True

								moves.append((xp, yp))
								generateJumps(board, xp, yp, moves, states)
								moves.pop()
								board[i][j], board[x][y], board[xp][yp] = previous, save, '.'
								jumpEnd = False
								# self.isKingJump = False
					if jumpEnd and len(moves) > 1:
						states.append(CheckersState(deepcopy(board), not state.blackToMove, deepcopy(moves)))

			states = []

			# generate jumps
			for i in range(8):
				for j in range(8):
					if state.grid[i][j].lower() == state.str:
						# self.isKingJump = False
						generateJumps(state.grid, i, j, [(i, j)], states)
			longestMove = 0
			longestStates = None
			for state in states:
				if len(state.moves) > longestMove:
					longestMove = len(state.moves)
					longestStates = state
			if len(states) > 0:
				return [longestStates]

			# generate moves
			for i in range(8):
				for j in range(8):
					if state.grid[i][j].lower() == state.str:
						generateMoves(state.grid, i, j, states)
			return states

		def iterativeDeepeningAlphaBeta(state):
			startTime = time()

			def alphaBetaSearch(state, alpha, beta, depth):
				def maxValue(state, alpha, beta, depth):
					val = -MaxUtility
					for successor in getSuccessors(state):
						val = max(val, alphaBetaSearch(successor, alpha, beta, depth))
						if val >= beta: return val
						alpha = max(alpha, val)
					return val

				def minValue(state, alpha, beta, depth):
					val = MaxUtility
					for successor in getSuccessors(state):
						val = min(val, alphaBetaSearch(successor, alpha, beta, depth - 1))
						if val <= alpha: return val
						beta = min(beta, val)
					return val

				if isTerminalState(state): return getTerminalUtility(state)
				if depth <= 0 or time() - startTime > MaxAllowedTimeInSeconds: return evaluationFunc(state)
				return maxValue(state, alpha, beta, depth) if state.str == self.str else minValue(state, alpha, beta, depth)

			bestMove = None
			for depth in range(1, MaxDepth):
				if time() - startTime > MaxAllowedTimeInSeconds: break
				val = -MaxUtility
				for successor in getSuccessors(state):
					score = alphaBetaSearch(successor, -MaxUtility, MaxUtility, depth)
					if score > val or score == -MaxUtility:
						val, bestMove = score, successor.moves
			return bestMove


		result = iterativeDeepeningAlphaBeta(CheckersState(state, self.blackToMove, []))
		return result
