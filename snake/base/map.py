#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0111,W0201,W0212

"""Definition of class Map."""

import random

from snake.base.point import Point, PointType
from snake.base.pos import Pos

class Map:
	"""2D game map."""
	def __init__(self, numRows, numCols):
		"""Initialize map object"""
		if not isinstance(numRows, int) or not isinstance(numCols, int):
			raise TypeError("\'numRows\' and \'numCols\' must be integers")
		if numRows < 5 or numCols < 5:
			raise ValueError("\'numRows\' and \'numCols\' must >= 5")

		self._numRows = numRows
		self._numCols = numCols
		self._capacity = (numRows - 2) * (numCols - 2)
		self._content = [[Point() for _ in range(numCols)] for _ in range(numRows)]
		self.reset()

	def reset(self):
		self._food = None
		for i in range(self._numRows):
			for j in range(self._numCols):
				if i == 0 or i == self._numRows - 1 or \
				   j == 0 or j == self._numCols - 1:
					self._content[i][j].type = PointType.WALL
				else:
					self._content[i][j].type = PointType.EMPTY

	def copy(self):
		m_copy = Map(self._numRows, self._numCols)
		for i in range(self._numRows):
			for j in range(self._numCols):
				m_copy._content[i][j].type = self._content[i][j].type
		return m_copy

	@property
	def numRows(self):
		return self._numRows
	
	@property
	def numCols(self):
		return self._numCols

	@property
	def capacity(self):
		return self._capacity
	
	@property
	def food(self):
		return self._food
	
	@property
	def content(self):
		return self._content
	
	@content.setter
	def content(self, val):
		self._content = val

	def point(self, pos):
		"""Return a point on the map.
		DO NOT directly modify the point type to PointType.FOOD and vice versa.
		Use {add|rm}_food() methods instead.
		Args:
			pos (base.pos.Pos): The position of the point to be fetched
		Returns:
			snake.point.Point: The point at the given position.
		"""
		return self._content[pos.x][pos.y]

	def isInside(self, pos):
		return pos.x > 0 and pos.x < self.numRows - 1 \
				and pos.y > 0 and pos.y < self.numCols - 1

	def isEmpty(self, pos):
		return self.isInside(pos) and self.point(pos).type == PointType.EMPTY

	def isSafe(self, pos):
		return self.isInside(pos) and (self.point(pos).type == PointType.EMPTY or \
										self.point(pos).type == PointType.FOOD)

	def isFull(self):
		"""Check if the map is filled with the snake's body."""
		for i in range(1, self.numRows - 1):
			for j in range(1, self.numCols - 1):
				t = self._content[i][j].type
				if t.value < PointType.HEAD_L.value:
					return False
		return True

	def hasFood(self):
		return self._food is not None

	def rmFood(self):
		if self.hasFood():
			self.point(self._food).type = PointType.EMPTY
			self._food = None

	def createFood(self, pos):
		self.point(pos).type = PointType.FOOD
		self._food = pos
		return self._food

	def createRandomFood(self):
		emptyPos = []
		for i in range(1, self._numRows - 1):
			for j in range(1, self._numCols - 1):
				t = self._content[i][j].type
				if t == PointType.EMPTY:
					emptyPos.append(Pos(i, j))
				elif t == PointType.FOOD:
					return None # Stop if the food exists

		if emptyPos:
			return self.createFood(random.choice(emptyPos))
		else:
			return None