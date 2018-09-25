# -*- coding: utf-8 -*-
"""
@author: Trajan
"""

# One of parameters high and low must be None and the other one must be a number.
import numpy as np

from classbuild import Contract
from vanilla import Tree_Dynamics
from classbuild import MC

class Lookback_Contract(Contract):
    def __init__(self, Strick = 1.1, Time = 10, high = None, low = 0.9):
        self.K = Strick
        self.T = Time
        self.high = high
        self.low = low
        
        
def lookback_put_pricer(contract,dynamics,MC):

    np.random.seed(MC.seed)  
    
    r=dynamics.r
    sigma=dynamics.sigma
    S0=dynamics.S0

    K=contract.K
    T=contract.T
    H=contract.high
    L=contract.low

    t=MC.T
    N=MC.N
    dt=T/t

    Z = np.random.randn(N, t)
    
    paths = S0*np.exp((r-sigma**2/2)*dt*np.tile(np.arange(1,t+1),(N,1))+sigma*np.sqrt(dt)*np.cumsum(Z,axis=1))   
    payoffDiscounted = np.maximum(0,K-paths[:,-1])

    if H:
        high = paths.max(1)<H
        payoffDiscounted = payoffDiscounted*high
    if L:
        low = paths.min(1)>L
        payoffDiscounted = payoffDiscounted*low


    allpathvalue = np.exp(-t*r*dt)*payoffDiscounted
    putprice = np.mean(allpathvalue)
        
    return(putprice)


if __name__ == '__main__':
    contract = Lookback_Contract()
    dynamics = Tree_Dynamics(S0=1)
    mc = MC()
    P = lookback_put_pricer(contract, dynamics, mc)
    # C = lookback_call_pricer(contract, dynamics, mc)
    print(P) 
