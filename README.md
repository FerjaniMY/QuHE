### QuHE: Open source library for quantum homomorphic encryption
- ![image](./img/QuHE.png)


### Quantum homomorphic encryption:

- ![image](./img/QFHE.png)


### Project Description: 

Quantum computers will tackle problems in different fields such as medical research and finance, where the protection of sensitive data is a must. But quantum computers on the cloud can be threaten for security, particulary when delegating a potential data to such computers. Clients, with limited computational ability, will want to use the services offered by quantum computation and communication protocols, in a way that their privacy is guarantee.

In tradition (quantum/classical) cryptography, the server needs to decrypt the data before doing any further computation. This can cause a problem if the client's data is sensitive and quantum computer is not trusted. This problem can be solve using homomorphic encryption which enables arbitrary computation on encrypted data without decryption.  Similarly to classical HE, quantum homomorphic encryption (QHE) allows clients with limited computational ability to delegated computations to untrusted quantum servers securely.

In this project, we developed QuHE, a library for quantum homomorphic enryption using Qiskit in which we implement some quantum homomorphic encryption protocols to allow the quantum computer to compute on encrypted data. Then, we provide an implementation of Grover's search on encrypted data using our library.


### Future goals and directions of the project:
* Build the first open-source library for quantum homomorphic encryption (QHE). 
* Provide the first qiskit implementation of QHE protocols.
* Make qiskit notebooks that help people to learn about QHE.


### Examples
Check out this example: https://github.com/FerjaniMY/QuHE/blob/master/tests/grover.ipynb


### Hackathon information
* Author: Mohamed Yassine Ferjani
* Contact: ferjanimedyassine@gmail.com
* QHack Team name: Qonlyme
* Challenges: IBM Qiskit Challenge.
