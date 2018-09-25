# -*- coding: utf-8 -*-
"""
@author: Trajan
"""

# reference:https://canvas.uchicago.edu/courses/14057/files/1305305?module_item_id=581775
import numpy as np

from classbuild import Contract
from vanilla import Tree_Dynamics
from classbuild import MC

class American_Contract(Contract):
    def __init__(self, K = 1, T = 4):
        self.T = T
        self.K = K

def american_put_pricer(contract,dynamics,MC):

    np.random.seed(MC.seed)  
    
    r=dynamics.r
    sigma=dynamics.sigma
    S0=dynamics.S0

    K=contract.K
    T=contract.T

    t=MC.T
    N=MC.N
    dt=T/t

    Z = np.random.randn(N, t)
    
    paths = S0*np.exp((r-sigma**2/2)*dt*np.tile(np.arange(1,t+1),(N,1))+sigma*np.sqrt(dt)*np.cumsum(Z,axis=1))   
    
    payoffDiscounted = np.maximum(0,K-paths[:,-1])

    for n in np.arange(t-1,0,-1):
        continuationPayoffDiscounted = np.exp(-r*dt)*payoffDiscounted

        X=paths[:,n-1]               
        basisfunctions = np.stack((np.ones((N)), X, X**2), axis=1)
            
        coefficients = np.linalg.lstsq(basisfunctions,continuationPayoffDiscounted)[0]
    
        estimatedContinuationValue = np.dot(basisfunctions,coefficients)
        exerciseValue = K-X
        whichPathsToExercise = (exerciseValue >= np.maximum(estimatedContinuationValue,0))
    
        payoffDiscounted[whichPathsToExercise] = exerciseValue[whichPathsToExercise]
        payoffDiscounted[np.logical_not(whichPathsToExercise)] = continuationPayoffDiscounted[np.logical_not(whichPathsToExercise)]


    continuationPayoffDiscounted = np.exp(-r*dt)*payoffDiscounted;
    estimatedContinuationValue = np.mean(continuationPayoffDiscounted);
    putprice = max(K-S0,estimatedContinuationValue);
        
    return(putprice)


if __name__ == '__main__':
    contract = American_Contract()
    dynamics = Tree_Dynamics(S0=1)
    mc = MC()
    P = american_put_pricer(contract, dynamics, mc)
    # C = american_call_pricer(contract, dynamics, mc)
    print(P)