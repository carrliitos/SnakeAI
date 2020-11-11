#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0111,W0201,W0212

"""Definition of class Snake."""

import random
from collections import deque

from snake.base.direc import Direc
from snake.base.point import PointType
from snake.base.pos import Pos

class Snake:
	"""Snake of the game"""
	def __init__(self, gameMap, initDirec=None, initBodies=None, initTypes=None):
		"""Initialize a snake object.
		Args:
			gameMap (base.map.Map): The map that the snake moves on.
			initDirec (base.direc.Direc): Initial direction.
			initBodies (list of base.pos.Pos): Initial snake bodies positions.
			initTypes (list of base.point.PointType): Types of each position in initBodies.
		"""
		self._map = gameMap
		self._initDirec = initDirec
		self._initTypes = initTypes
		self._initBodies = initBodies
		self.reset(False)

	def reset(self, resetMap=True):
		randInit = False
		if self._initDirec is None: # RAndomly initialize
			randInit = True
			headRow = random.randrange(2, self._map.numRows - 2)
			headCol = random.randrange(2, self._map.numCols - 2)
			head = Pos(headRow, headCol)

			self._initDirec = random.choice([Direc.LEFT, Direc.UP, Direc.RIGHT, Direc.DOWN])
			self._initBodies = [head, head.adj(Direc.opposite(self._initDirec))]

			self._initTypes = []
			if self._initDirec == Direc.LEFT:
				self._initTypes.append(PointType.HEAD_L)
			elif self._initDirec == Direc.UP:
				self._initTypes.append(PointType.HEAD_U)
			elif self._initDirec == Direc.RIGHT:
				self._initTypes.append(PointType.HEAD_R)
			elif self._initDirec == Direc.DOWN:
				self._initTypes.append(PointType.HEAD_D)

			if self._initDirec == Direc.LEFT or self._initDirec == Direc.RIGHT:
				self._initTypes.append(PointType.BODY_HOR)
			if self._initDirec == Direc.UP or self._initDirec == Direc.DOWN:
				self._initTypes.append(PointType.BODY_VER)

		self._steps = 0
		self._dead = False
		self._direc = self._initDirec
		self._direcNext = Direc.NONE
		self._bodies = deque(self._initBodies)

		if resetMap:
			self._map.reset()
		for i, pos in enumerate(self._initBodies):
			self._map.point(pos).type = self._initTypes[i]

		if randInit:
			self._initDirec = self._initBodies = self._initTypes = None

	def copy(self):
		m_copy = self._map.copy()
		s_copy = Snake(m_copy, Direc.NONE, [], [])
		s_copy._steps = self._steps
		s_copy._dead = self._dead
		s_copy._direc = self._direc
		s_copy._direcNext = self._direcNext
		s_copy._bodies = deque(self._bodies)
		return s_copy, m_copy

	@property
	def map(self):
		return self._map
	
	@property
	def steps(self):
		return self._steps
	
	@property
	def dead(self):
		return self._dead
	
	@property
	def direc(self):
		return self._direc
	
	@property
	def bodies(self):
		return self._bodies
	
	@property
	def direcNext(self):
		return self._direcNext

	@dead.setter
	def dead(self, val):
		self._dead = val

	@direcNext.setter
	def direcNext(self, val):
		self._direcNext = val

	def len(self):
		return len(self._bodies)

	def head(self):
		if not in self._bodies:
			return None
		return self._bodies[0]

	def tail(self):
		if not in self._bodies:
			return None
		return self._bodies[-1]

	def movePath(self, path):
		for p in path:
			self.move(p)

	def move(self, newDirec=None):
		if newDirec is not None:
			self._direcNext = newDirec

		if (self._dead or
			self._direcNext == Direc.NONE or
			self._map.isFull() or
			self.direcNext == Direc.opposite(self._direc)):
				return

		if not self._map.isSafe(newHead):
			self._dead = True
		if self._map.point(newHead).type == PointType.FOOD:
			self._map.rmFood()
		else:
			self._rmTail()

		self._map.point(newHead).type = newHeadType
		self._direc = self._direcNext
		self._steps += 1

	def _rmTail(self):
		self._map.point(self.tail()).type = PointType.EMPTY
		self._bodies.pop()

	def newTypes(self):
		oldHeadType, newHeadType = None, None
		# newHeadType
		if self._direcNext == Direc.LEFT:
			newHeadType = PointType.HEAD_L
		elif self._direcNext == Direc.UP:
			newHeadType = PointType.HEAD_U
		elif self._direcNext == Direc.RIGHT:
			newHeadType = PointType.HEAD_R
		elif self._direcNext == Direc.DOWN:
			newHeadType = PointType.HEAD_D

		# oldHeadType
		if (self._direc == Direc.LEFT and self._direcNext == Direc.LEFT) or \
		   (self._direc == Direc.RIGHT and self._direcNext == Direc.RIGHT):
			oldHeadType = PointType.BODY_HOR
		elif (self._direc == Direc.UP and self._direcNext == Direc.UP) or \
			 (self._direc == Direc.DOWN and self._direcNext == Direc.DOWN):
			oldHeadType = PointType.BODY_VER
		elif (self._direc == Direc.RIGHT and self._direcNext == Direc.UP) or \
			 (self._direc == Direc.DOWN and self._direcNext == Direc.LEFT):
			oldHeadType = PointType.BODY_LU
		elif (self._direc == Direc.LEFT and self._direcNext == Direc.UP) or \
			 (self._direc == Direc.DOWN and self._direcNext == Direc.RIGHT):
			oldHeadType = PointType.BODY_UR
		elif (self._direc == Direc.LEFT and self._direcNext == Direc.DOWN) or \
			 (self._direc == Direc.UP and self._direcNext == Direc.RIGHT):
			oldHeadType = PointType.BODY_RD
		elif (self._direc == Direc.RIGHT and self._direcNext == Direc.DOWN) or \
			 (self._direc == Direc.UP and self._direcNext == Direc.LEFT):
			oldHeadType = PointType.BODY_DL
		return oldHeadType, newHeadType