# -*- coding: utf-8 -*-
"""
@author: Trajan
"""
import numpy as np
import sys

from classbuild import Contract
from classbuild import Dynamics
from classbuild import Tree

class Vanilla_Contract(Contract):
    def __init__(self, Strick = 95, Time = 0.25, interval = 0.02):
        self.K = Strick
        self.T = Time
        self.observationinterval = interval

class Tree_Dynamics(Dynamics):
    def __init__(self, S0 = 100, sigma = 0.4, r = 0):
        self.S0 = S0
        self.sigma = sigma
        self.r = r

def put_option_pricer(dynamics, contract, tree):
    
    S0, sigma, r = dynamics.S0, dynamics.sigma, dynamics.r
    K, T, interval  = contract.K, contract.T, contract.observationinterval
    N = tree.N

    deltat = T/N 
    deltax = sigma*np.sqrt(3*deltat) 
    
    S=S0*np.exp(np.linspace(N, -N, num=2*N+1, endpoint=True)*deltax)

    if abs(interval/deltat-round(interval/deltat)) > 1e-12:
        sys.exit("This value of N fails to place the observation dates in the tree.")

    nu =  r - sigma*sigma/2
    Pu =  1/2*((sigma*sigma*deltat+nu*nu*deltat*deltat)/(deltax*deltax) + nu*deltat/deltax)    
    Pm =  1 - (sigma*sigma*deltat+nu*nu*deltat*deltat)/(deltax*deltax)      
    Pd =  1/2*((sigma*sigma*deltat+nu*nu*deltat*deltat)/(deltax*deltax) - nu*deltat/deltax)      
        
    optionprice = np.maximum(K-S,0)   
        
    
    for t in np.linspace(N-1, 0, num=N, endpoint=True)*deltat:
        optionprice = np.exp(-r*deltat)*(optionprice[:-2]*Pu+optionprice[1:-1]*Pm+optionprice[2:]*Pd)
        
    return optionprice[0]   

   

if __name__ == '__main__':
    contract = Vanilla_Contract()
    dynamics = Tree_Dynamics()
    tree = Tree()
    P = put_option_pricer(dynamics, contract, tree)
    # C = call_option_pricer(dynamics, contract, tree)
    print(P)