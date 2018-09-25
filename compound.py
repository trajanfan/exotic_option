# -*- coding: utf-8 -*-
"""
@author: Trajan
"""

import numpy as np

from classbuild import Contract
from classbuild import Dynamics
from classbuild import Tree

class Local_Dynamics(Dynamics):
    def __init__(self, S0=100, q=0.06, r=0.01, maxvol=0.6, localvol=lambda S,t: np.minimum(0.2+5*np.log(S/100)**2+0.1*np.exp(-t), 0.6)):
        self.S0 = S0
        self.maxvol = maxvol
        self.r = r
        self.q = q
        self.localvol = localvol
        
class Compound_Contract(Contract):
    def __init__(self, putexpiry=0.75, putstrike=95, callexpiry=0.25, callstrike=10):
        self.putexpiry = putexpiry
        self.putstrike = putstrike
        self.callexpiry = callexpiry
        self.callstrike = callstrike
        
def pricer_call_on_put_compound(contract,dynamics,tree):
    
    S0, maxvol, r, q, localvol = dynamics.S0, dynamics.maxvol, dynamics.r, dynamics.q, dynamics.localvol
    putT, putK, callT, callK = contract.putexpiry, contract.putstrike, contract.callexpiry, contract.callstrike
    N = tree.N
    
    deltat = putT/N
    deltax = np.maximum(localvol(100,0)*np.sqrt(3*deltat),maxvol*np.sqrt(deltat))
    
    S = S0*np.exp(np.linspace(N, -N, num=2*N+1, endpoint=True)*deltax)
    optionprice = np.maximum(putK-S,0)
    
    for t in np.linspace(N-1, 0, num=N, endpoint=True)*deltat:
        S = S[1:-1]
        nu =  r - q - localvol(S,t)*localvol(S,t)/2
        Pu =  1/2*((localvol(S,t)*localvol(S,t)*deltat+nu*nu*deltat*deltat)/(deltax*deltax) + nu*deltat/deltax)
        Pm =  1 - (localvol(S,t)*localvol(S,t)*deltat+nu*nu*deltat*deltat)/(deltax*deltax)
        Pd =  1/2*((localvol(S,t)*localvol(S,t)*deltat+nu*nu*deltat*deltat)/(deltax*deltax) - nu*deltat/deltax)
        
        if t-callT>-deltat and t<callT:
            compound_optionprice = np.maximum(optionprice-callK,0)
        
        optionprice = np.maximum(np.maximum(putK-S,0),np.exp(-r*deltat)*(optionprice[:-2]*Pu+optionprice[1:-1]*Pm+optionprice[2:]*Pd))
        
        if t<callT:
            compound_optionprice = np.exp(-r*deltat)*(compound_optionprice[2:]*Pu+compound_optionprice[1:-1]*Pm+compound_optionprice[:-2]*Pd)
    
    price_of_call_on_put = compound_optionprice[0]
    
    return price_of_call_on_put



if __name__ == '__main__':
    contract = Compound_Contract()
    dynamics = Local_Dynamics()
    tree = Tree(1000)
    CoP = pricer_call_on_put_compound(contract,dynamics,tree)
    # contract = Compound_Contract(putexpiry=0.25, putstrike=95, callexpiry=0.75, callstrike=10)
    # PoC = pricer_put_on_call_compound(contract,dynamics,tree)
    print(CoP)