#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111

class BaseAlgorithm:
	"""Super class of all algorithms"""
	def __init__(self, snake):
		self._snake = snake
		self._map = snake.map

	@property
	def map(self):
		return self._map
	
	@property
	def snake(self):
		return self._snake
	
	@snake.setter
	def snake(self, val):
		self._snake = val
		self._map = val.map

	def nextDirec(self):
		"""Generate the next direction of the snake."""
		return NotImplemented

	def close(self):
		"""Release resources"""
		return NotImplemented