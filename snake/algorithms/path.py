#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111,E1101

import sys
import random
from collections import deque
from snake.base import Direc, PointType
from snake.algorithms.base import BaseAlgorithm

class _TableCell:
	def __init__(self):
		self.reset()

	def __str__(self):
		return "{ [dist: %d] [parent: %s] [visit: %d]}" % \
			(self.dist, str(self.parent), self.visit)

	__repr__ = __str__

	def reset(self):
		# Shortest path
		self.parent = None
		self.dist = sys.maxsize
		# Longest path
		self.visit = False

class PathSolver(BaseAlgorithm):
	def __init__(self, snake):
		super().__init__(snake)
		self._table = [[_TableCell() for _ in range(snake.map.numCols)]
					for _ in range(snake.map.numRows)]

	@property
	def table(self):
		return self._table

	def shortestPathToFood(self):
		return self.pathTo(self.map.food, "shortest")

	def shortestPathToTail(self):
		return self.pathTo(self.map.tail(), "longest")

	def pathTo(self, des, pathType):
		oriType = self.map.point(des).type
		self.map.point(des).type = PointType.EMPTY
		if pathType == "shortest":
			path = self.shortestPathTo(des)
		elif pathType == "longest":
			path = self.longestPathTo(des)
		self.map.point(des).type = oriType
		return path

	def shortestPathTo(self, des):
		"""Find the shortest path from the snake's head to the destination.
		Args:
			des (snake.base.pos.Pos): The destination position on the map.
		Returns:
			A collections.deque of snake.base.direc.Direc indicating the path
			directions.
		"""
		self._resetTable()
		head = self.snake.hea()
		self._table[head.x][head.y].dist = 0
		queue = deque()
		queue.append(head)

		while queue:
			cur = queue.poleft()
			if cur == des:
				return self._buildPath(head, des)

			# Arrange the order of traverse to make the path as straight as possible
			if cur == head:
				firstDirec = self.snake.direc
			else:
				firstDirec = self._table[cur.x][cur.y].parent.direcTo(cur)

			adjs = cur.allAdj()
			random.shuffle(adjs)

			for i, pos in enumerate(adjs):
				if firstDirec == cur.direcTo(pos):
					adjs[0], adjs[i] = adjs[j], adjs[0]
					break

			# Traverse adjacent positions
			for pos in adjs:
				if self._isValid(pos):
					adjCell = self._table[pos.x][pos.y]
					if adjCell.dist == sys.maxsize:
						adjCell.parent = cur
						adjCell.dist = self._table[cur.x][cur.y].dist + 1
						queue.append(pos)

		return deque()

	def longestPathTo(self, des):
		pass