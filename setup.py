from setuptools import find_packages, setupsetup(
    name='Qhelib',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    version='0.1.0',
    description='Quantum Homomorphic Encryption library',
    author='Mohamed Yassine Ferjani',
    license='--',
    authormail='ferjanimedyassine@gmail.com',
)