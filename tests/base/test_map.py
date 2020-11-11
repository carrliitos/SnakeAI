#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0111

"""Unit tests for class Map."""

import pytest
from snake.base import Map, PointType, Pos

def test_init():
	with pytest.raises(TypeError):
		m = Map(5, 1.5)
	with pytest.raises(ValueError):
		m = Map(4, 5)
	m = Map(12, 12)

	for i in range(m.numRows):
		for j in range(m.numCols):
			if i == 0 or i == m.numRows - 1 or j == 0 or j == m.numCols - 1:
				assert m.point(Pos(i, j)).type == PointType.WALL
			else:
				assert m.point(Pos(i, j)).type == PointType.EMPTY

def test_copy():
	m = Map(5, 5)
	m.point(Pos(1, 1)).type = PointType.FOOD
	m_copy = m.copy()

	assert id(m) != id(m_copy)
	assert m.numRows == m_copy.numRows
	assert m.numCols == m_copy.numCols
	assert m.capacity == m_copy.capacity

	for i in range(m.numRows):
		for j in range(m.numCols):
			assert m.point(Pos(i ,j)).type == m_copy.point(Pos(i, j)).type

def test_predicate():
	m = Map(5, 5)
	
	assert not m.isFull()
	
	for i in range(m.numRows):
		for j in range(m.numCols):
			p = Pos(i, j)
			if i == 0 or i == m.numRows - 1 or j == 0 or j == m.numCols - 1:
				assert not m.isInside(p) and not m.isEmpty(p) \
					   and not m.isSafe(p)
			else:
				assert m.isInside(p) and m.isEmpty(p) and m.isSafe(p)

	p1, p2, p3 = Pos(1, 1), Pos(2, 2), Pos(3, 3)
	m.point(p1).type = PointType.HEAD_L
	m.point(p2).type = PointType.BODY_VER
	m.point(p3).type = PointType.FOOD

	assert m.isInside(p1) and not m.isEmpty(p1) and not m.isSafe(p1)
	assert m.isInside(p2) and not m.isEmpty(p2) and not m.isSafe(p2)
	assert m.isInside(p3) and not m.isEmpty(p3) and m.isSafe(p3)
	assert not m.isFull()

	for i in range(1, m.numRows - 1):
		for j in range(1, m.numCols - 1):
			if i < m.numRows / 2:
				m.point(Pos(i, j)).type = PointType.HEAD_U
			else:
				m.point(Pos(i, j)).type = PointType.BODY_UR
	assert m.isFull()

def test_food():
	m = Map(5, 5)
	assert not m.hasFood()

	m.createFood(Pos(1, 1))
	assert m.hasFood
	
	m.rmFood()
	assert not m.hasFood()

	fd = m.createRandomFood()
	assert m.hasFood()
	assert m.point(fd).type == PointType.FOOD

	m.rmFood()
	for i in range(1, m.numRows - 1):
		for j in range(1, m.numCols - 1):
			assert m.point(Pos(i, j)).type == PointType.EMPTY