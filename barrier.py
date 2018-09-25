# -*- coding: utf-8 -*-
"""
@author: Trajan
"""

import numpy as np
import vanilla

from vanilla import Vanilla_Contract
from vanilla import Tree_Dynamics
from classbuild import Tree

class Barrier_Contract(Vanilla_Contract):
    def __init__(self, Strick = 95, Time = 0.25, Barrier = 74, interval = 0.02):
        self.K = Strick
        self.T = Time
        self.H = Barrier
        self.observationinterval = interval
    

def upout_barrier_pricer(dynamics, contract, tree, callorput = 'Call'):
    
    S0, sigma, r = dynamics.S0, dynamics.sigma, dynamics.r
    K, T, H, interval  = contract.K, contract.T, contract.H, contract.observationinterval
    N = tree.N

    deltat = T/N 
    deltax = sigma*np.sqrt(3*deltat) 
    
    S=S0*np.exp(np.linspace(N, -N, num=2*N+1, endpoint=True)*deltax)

    nu =  r - sigma*sigma/2       
    Pu =  1/2*((sigma*sigma*deltat+nu*nu*deltat*deltat)/(deltax*deltax) + nu*deltat/deltax)   
    Pm =  1 - (sigma*sigma*deltat+nu*nu*deltat*deltat)/(deltax*deltax)      
    Pd =  1/2*((sigma*sigma*deltat+nu*nu*deltat*deltat)/(deltax*deltax) - nu*deltat/deltax)     
        
    if callorput == "Call":
        optionprice = np.maximum(S-K,0)
    else:
        optionprice = np.maximum(K-S,0)  
        
    
    for t in np.linspace(N-1, 0, num=N, endpoint=True)*deltat:
        optionprice = np.exp(-r*deltat)*(optionprice[:-2]*Pu+optionprice[1:-1]*Pm+optionprice[2:]*Pd)
        S = S[1:-1]
        idx = S>H
        optionprice[idx] = 0

    return optionprice[0]

def downout_barrier_pricer(dynamics, contract, tree, callorput = 'Call'):
    
    S0, sigma, r = dynamics.S0, dynamics.sigma, dynamics.r
    K, T, H, interval  = contract.K, contract.T, contract.H, contract.observationinterval
    N = tree.N

    deltat = T/N 
    deltax = sigma*np.sqrt(3*deltat) 
    
    S=S0*np.exp(np.linspace(N, -N, num=2*N+1, endpoint=True)*deltax)

    nu =  r - sigma*sigma/2       
    Pu =  1/2*((sigma*sigma*deltat+nu*nu*deltat*deltat)/(deltax*deltax) + nu*deltat/deltax)   
    Pm =  1 - (sigma*sigma*deltat+nu*nu*deltat*deltat)/(deltax*deltax)      
    Pd =  1/2*((sigma*sigma*deltat+nu*nu*deltat*deltat)/(deltax*deltax) - nu*deltat/deltax)     
        
    if callorput == "Call":
        optionprice = np.maximum(S-K,0)
    else:
        optionprice = np.maximum(K-S,0)
        
    
    for t in np.linspace(N-1, 0, num=N, endpoint=True)*deltat:
        optionprice = np.exp(-r*deltat)*(optionprice[:-2]*Pu+optionprice[1:-1]*Pm+optionprice[2:]*Pd)
        S = S[1:-1]
        idx = S<H
        optionprice[idx] = 0

    return optionprice[0]

def upin_barrier_pricer(dynamics, contract, tree, callorput = 'Call'):
    UO = upout_barrier_pricer(dynamics, contract, tree, callorput = callorput)
    if callorput == 'Call':
        VO = vanilla.call_option_pricer(dynamics, contract, tree)
    else:
        VO = vanilla.put_option_pricer(dynamics, contract, tree)
    return VO-UO
    
def downin_barrier_pricer(dynamics, contract, tree, callorput = 'Call'):
    DO = downout_barrier_pricer(dynamics, contract, tree, callorput = callorput)
    if callorput == 'Call':
        VO = vanilla.call_option_pricer(dynamics, contract, tree)
    else:
        VO = vanilla.put_option_pricer(dynamics, contract, tree)
    return VO-DO

if __name__ == '__main__':
    
    contract = Barrier_Contract()
    dynamics = Tree_Dynamics()
    tree = Tree()
    UO = upout_barrier_pricer(dynamics, contract, tree)
    DO = downout_barrier_pricer(dynamics, contract, tree)
    UI = upin_barrier_pricer(dynamics, contract, tree)
    DI = downin_barrier_pricer(dynamics, contract, tree)
    print(UO, DO, UI, DI)
