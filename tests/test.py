#from Context import *
import QuHE as qhe
import unittest
from qiskit import *
from math import pi

#from Evaluation import *


class ContextTestCase(unittest.TestCase):

    


    def test_qotp(self):

 
 
        keys=[[1,0,1],[1,1,0]]
        qc=QuantumCircuit(3,3)
        ctx=qhe.Context(qc,keys,method='qotp',scheme='Liang')

        ctx.encrypt()

        ctx.add_T(0)
        ctx.update_T(0)


        ctx.add_T(1)
        ctx.update_T(1)

        ctx.add_X(1)# no key update is required with the X-gate

        ctx.add_T(1)
        ctx.update_T(1)

        ctx.add_X(2)




        x=ctx.decrypt()
        print(x)
        ctx.visualize()


if __name__ == '__main__':
    unittest.main()
    