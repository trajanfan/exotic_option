# -*- coding: utf-8 -*-
"""
@author: Trajan
"""

class Contract:
    pass

class Dynamics:
    pass

class Tree:
    def __init__(self, N=100):
        self.N = N

class TD:
    pass

class MC:
    def __init__(self, N=10000, T=10, seed=0):
        self.N = N
        self.T = T
        self.seed = seed