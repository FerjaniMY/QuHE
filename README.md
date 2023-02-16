### QuHE: Open source library for quantum homomorphic encryption
- ![image](./img/QuHE.png)


### Quantum homomorphic encryption:

- ![image](./img/QFHE.png)


### Project Description: 

Quantum computers will tackle problems in different fields such as medical research and finance, where the protection of sensitive data is a must. But quantum computers on the cloud can be threaten for security, particulary when delegating a potential data to such computers. Clients, with limited computational ability, will want to use the services offered by quantum computation and communication protocols, in a way that their privacy is guaranteed.

In traditional (quantum/classical) cryptography, the server needs to decrypt the data before doing any further computation. This can cause a problem if the client's data is sensitive and the quantum computer is not trusted. This problem can be solved using homomorphic encryption which enables arbitrary computation on encrypted data without decryption.  Similarly to classical HE, quantum homomorphic encryption (QHE) allows clients with limited computational ability to delegated computations to untrusted quantum servers securely.

In this project, we developed QuHE, a library for quantum homomorphic enryption using Qiskit in which we implement some quantum homomorphic encryption protocols that enables quantum computers to compute on encrypted data. 



### Examples
This is an example of Grover's search on encrypted data using our library: https://github.com/FerjaniMY/QuHE/blob/master/tests/grover.ipynb

