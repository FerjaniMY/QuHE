# Author: Mohamed Yassine Ferjani

from qiskit import *
from math import pi

def xor(a,b):
        return (a+b)%2


class Context:

    def __init__(self,qc,keys,method:str,scheme:str=None):
        """[summary]

        Args:
            qc ([type]): [description]
            keys ([type]): [description]
            method (str): [description]
            scheme (str, optional): [description]. Defaults to None.
        """     


      
        self.qc=qc
        self.method=method
        self.scheme=scheme
        self.keys=keys
        self.verify=True
    
    

    def encrypt(self):
        
        if self.method.upper()=='QOTP':
            """
            keys: QOTP encryption keys
            keys[0]: indicates X gates (ai)
            keys[1]: indicates z gates (bi)
            Example: keys=[[1,0,1,1],[0,0,1,1]] -> X - X X, - - Z Z
            len(keys)=2
            len(keys[0])=nqubits
            """


            for i in range(len(self.keys[0])):
                if self.keys[0][i]==1:
                    self.qc.x(i)
                if self.keys[1][i]==1:
                    self.qc.z(i)
            self.qc.barrier()
    
        
        elif self.method.upper()=='RANDOM_BASIS':
             """
             Ref: ..
             keys[0]={theta0, theta1,...}
             keys[1]={phi0, phi1,....}
             """
             for i in range(len(self.keys[0])):
                 self.qc.u3(self.keys[0][i],self.keys[1][i],pi,i)
             self.qc.barrier()
            

        return self.qc

   
    def execute_circuit(self):
        """
        Execute a quantum circuit using the qasm_simulator from Qiskit

        Returns:
            (list): measurements results
        """        

        for i in range(len(self.keys[0])):
            self.qc.measure(i,i)
        #self.qc.measure(0,0)
        #if self.verify=True and self.scheme.upper()=='LIANG'::
        #    for i in range(self.nb):
        #        if i!=j:
        #            qc.measure(i,i) #measure all qubits except the one that contains T-gates
        
        print(self.qc)
        backend = BasicAer.get_backend('qasm_simulator')
        shots = 1096
        results = execute(self.qc, backend=backend, shots=shots).result()
        answer = results.get_counts()
        
        return list(answer.keys())[0][::-1]
    
    
    def update_T(self,j): # j is the index of the qubit that contains the T-gate
        """Update the keys when evaluating T-gate according to the chosen scheme 

        Args:
            keys ([type]): [description]
            j ([type]): qubit index

        Returns:
            [type]: [description]
        """        
        #self.verify=True

        if self.scheme.upper()=='LIANG':
          #create auxiliary qubits to evaluate T
          qr = QuantumRegister(2,'aux')
          cr=ClassicalRegister(2)
          circ=QuantumCircuit(qr,cr)
          
          circ.reset(qr[0])
          circ.reset(qr[1])
          

    
          #According to the scheme in paper ...
          # Bell State
          circ.h(0)
          circ.cx(0,1)

          new=self.qc+circ
          #print(new)
          
     
          # Correction of the errors introduced by T-gates according to the scheme 
          new.swap(j,qr[0])
          if self.keys[0][j]==1: 
              new.s(qr[0]) #S^a
          new.cx(qr[0],qr[1])
          new.h(qr[0])
          #new.barrier(qr[0],qr[1])
          

          #self.qc.measure(j,j)# j is the index to T gate
          #new.measure(0,0)
          
          # r_a, r_b
          new.measure(qr[0],cr[0]) #r_a
          new.measure(qr[1],cr[1]) #r_b
          
          new.barrier(qr[0],qr[1])

          
          #print(new)

          #circuit execution
          backend = BasicAer.get_backend('qasm_simulator')
          shots = 1000
          results = execute(new, backend=backend, shots=shots).result()
          answer = results.get_counts()
          r=list(answer)[0]#[::-1]#[0:2]
          #plot_histogram(answer)
   
          # Key update ----> (ai, bi) = (ai−1 ⊕ ra, ai−1 ⊕ bi−1 ⊕ rb)
          r_a=int(r[1])
          r_b=int(r[0])
          #t=int(r[0])
          #print('r_a',r_a,'r_b',r_b)
          
          #self.qc=new   this was the main issue
          print("T-gate update circuit:",new)
          
          
          #self.qc.measure(j,j)


          
          self.keys[1][j]=xor(xor(self.keys[0][j], self.keys[1][j]), r_b)#a ⊕ b ⊕ rb
          self.keys[0][j]=xor(self.keys[0][j], r_a)#ai ⊕ ra
          print("T",j,"updated")
        
    def decrypt(self): 
            """
            Decrypt a quantum circuit using the encryption key 

            Args:
                qc (Qiskit.object): quantum circuit
                j (int): index of the qubit
            
            Returns:
                y (str): decrypted result
            
            """            
            
            if self.method.upper()=='RANDOM_BASIS':
                """ theta,phi= keys[0],keys[1] """
              
                # for now phi is fixed to 0  
                for j in range(len(self.keys[0])):
                    self.qc.u(-self.keys[0][j],0,pi,j) #conjugate transpose of K (encryption matrix)
                x=self.execute_circuit()
                #print(self.qc)
                return 'Decrypted result',x

                
            
            elif self.method.upper()=='QOTP':
                #print(qc)
                #if self.verify==True:
                    #x=self.execute_circuit(j)
                #x=self.execute_circuit()# meas results of the updated circuit
                #measurement
                self.qc.barrier()
                for i in range(len(self.keys[0])):
                    self.qc.measure(i,i)
                backend = BasicAer.get_backend('qasm_simulator')
                shots = 1000
                results = execute(self.qc, backend=backend, shots=shots).result()
                answer = results.get_counts()
                x=list(answer.keys())[::-1]#[0][::-1]
                #y=list(answer.keys())[0:2][::-1]
                
                #print(self.qc)
                print("Server output",x[0:len(self.keys[0])]) 
                #print("Server's output",y) 
                
                #Don't forget to implement the case of multiple output 
                
                s=['']*len(x)

                #if self.verify==True:
                #x=x[2:len(self.keys[0])]
                #print('new x',x)
                
                c=len(self.keys[0])
                #print('Xj',x)
                
                for i in range(len(x)):

                  for j in range(len(self.keys[0])): #nbqubits = len(self.keys[0])
                    #self.qc.measure(j) #client side
                    #calculates the results
                    #return (int(x[j+1])+ self.keys[0][j])%2,(int(x[j])+self.keys[0][j+1])%2 # reverse the order of qubits according to quantum information convention
                    # !!! the output result is not reversed like the qiskit outputs.
                    #s+=str((int(x[len(self.keys[0])-j-1])+ self.keys[0][j])%2)
                    #print('test',x[i][j],j)
                     
                     

                    
                    s[i]+=str((int(x[i][len(self.keys[0])-j-1])+ self.keys[0][j])%2)
                    #s[i]+=str((int(x[i][j])+ self.keys[0][j])%2)

                    #s[i]+=str((int(x[i][j])+ self.keys[0][len(self.keys[0])-j-1])%2)
                     
                     
                    
                return "Decrypted result",s
            
            else:
                raise ValueError('Method does not exist')

                
    def update_h(self,j):
        """Update the keys after applying hadamard gate

        Args:
            j (int): qubit index
        """        
    
        x=self.keys[0][j] #keys[0] indicates x gates, keys[0][0]-> X gate on the first qubit
        self.keys[0][j]=self.keys[1][j]
        self.keys[1][j]=x

    def update_cx(self,j):
        """Update the keys after applying CNOT gate

        Args:
            j (int): qubit index
        """        
    
        self.keys[1][j]=(self.keys[1][j]+self.keys[1][j+1])%2
        self.keys[0][j+1]=(self.keys[0][j]+self.keys[0][j+1])%2
    
    
    
    
    

    def update_cz(self,j,m):
        # j: control, m:target 
       
        self.keys[1][j]=self.keys[1][j]* self.keys[0][m]
        self.keys[1][m]=self.keys[1][m]* self.keys[0][j]

        



    
    def make_secret_key(self, **params):
        pass

    

    def visualize(self):
        
        return self.qc.draw(output='mpl')


    
    def update_Tdg(self,j): # j is the index of the qubit that contains the T-gate
        """Update the keys when evaluating Tdg-gate according to the chosen scheme 

        Args:
            keys ([type]): [description]
            j ([type]): qubit index

        Returns:
            [type]: [description]
        """        
        #self.verify=True

        if self.scheme.upper()=='LIANG':
          #create auxiliary qubits to evaluate T
          qr = QuantumRegister(2,'aux')
          cr=ClassicalRegister(2)
          circ=QuantumCircuit(qr,cr)
          
          circ.reset(qr[0])
          circ.reset(qr[1])
          

    
          #According to the scheme in paper ...
          # Bell State
          circ.h(0)
          circ.cx(0,1)

          new=self.qc+circ
          #print(new)
          
     
          # Correction of the errors introduced by T-gates according to the scheme 
          new.swap(j,qr[0])
          if self.keys[0][j]==1: 
              new.s(qr[0]) #S^a
          new.cx(qr[0],qr[1])
          new.h(qr[0])
          #new.barrier(qr[0],qr[1])
          

          #self.qc.measure(j,j)# j is the index to T gate
          #new.measure(0,0)
          
          # r_a, r_b
          new.measure(qr[0],cr[0]) #r_a
          new.measure(qr[1],cr[1]) #r_b
          
          new.barrier(qr[0],qr[1])

          
          #print(new)

          #circuit execution
          backend = BasicAer.get_backend('qasm_simulator')
          shots = 1000
          results = execute(new, backend=backend, shots=shots).result()
          answer = results.get_counts()
          r=list(answer)[0]#[0:2]
          #plot_histogram(answer)
   
          # Key update ----> (ai, bi) = (ai−1 ⊕ ra, ai−1 ⊕ bi−1 ⊕ rb)
          r_a=int(r[1])
          r_b=int(r[0])
          #t=int(r[0])
          #print('r_a',r_a,'r_b',r_b)
          #self.qc=new
          #self.qc.measure(j,j)
          print(new)

          


          
          self.keys[1][j]=xor(self.keys[1][j], r_b)#a ⊕ b ⊕ rb
          self.keys[0][j]=xor(self.keys[0][j], r_a)#ai ⊕ ra
          print("Tdj",j,"updated")

    
    def update_swap(self,i,j):
        """[summary]

        Args:
            i ([type]): qubit index
            j ([type]): qubit index
        """        
        x=self.keys[0][j]
        self.keys[O][i]=x


        self.keys[1][i]=self.keys[1][j]

    # add gates 
    def add_T(self,j):
        self.qc.t(j)
    
    def add_Tdg(self,j):
        self.qc.tdg(j)

    def add_X(self,j):
        self.qc.x(j)

    def add_Z(self,j):
        self.qc.z(j)
    
    def add_H(self,i):
        self.qc.h(i)

    def add_CX(self,i,j):
        self.qc.cx(i,j)
    
    def add_CZ(self,i,j):
        self.qc.cz(i,j)
     
    def measure(self,i):
        self.qc.measure(i,i)
    
    def qc(self):
        return self.qc 
