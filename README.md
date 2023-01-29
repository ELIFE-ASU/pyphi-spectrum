## PyPhi-Spectrum
PyPhi-Spectrum is a wrapper for [PyPhi](https://doi.org/10.1371/journal.pcbi.1006343) that can be used to calculate all possible Phi values for a given system. Its core functionality is based on elementary function calls to PyPhi, with the main difference from PyPhi being that whenever there is a minimization or maximization procedure, it looks for all minimizers or maximizers, forks the state of the computation accordingly, and carries on computations according to the mathematical definition for all forks.

### Usage

For each cut of a given subsystem, a spectrum of Phi values results as a consequence of an inability to resolve degenerate core causes/effects. These spectra can be calculated for all cuts via the function call `get_phi_spectrum` which takes a given subsystem as input and returns the cuts and their corresponding Phi values as output. However, only Phi values between the min and max value of the MIP (cut with the lowest overall Phi value) satisfy the definition of Phi_MIP. The valid $\Phi^{MIP}$ values are computed via the function call `get_Phi_MIP`, which takes the spectrum of Phi values previously calculated and keeps only those between the min and max Phi value of the MIP.

#### Sample Usage

```python
import pyphi
import numpy as np
from pyphi import phi_spectrum

# Transition probability matrix. Saying where each state goes (little-end notation)
tpm = np.array([
    [0.,0.,0.],
    [0.,0.,0.],
    [1.,0.,0.],
    [1.,0.,1.],
    [0.,1.,0.],
    [0.,1.,0.],
    [1.,1.,0.],
    [1.,1.,1.]
])

# Set up network object
network = pyphi.Network(tpm, node_labels=['A','B','C'])
print("Network = ",network.node_labels)

# Put the system into a given state
state = (0,0,0)
nodes = ['A','B','C']

## Get the requisite Subsystem
subsystem = pyphi.Subsystem(network, state, nodes)

## Calculate all Phi values
display_CES = False  # if True, output will display all constellations
solution = None # how to handle degenerate purview elements (None,'Smallest','Largest', or 'Moon')
Phi_Spectrum = phi_spectrum.get_phi_spectrum(subsystem,display_CES,solution)

## Print the spectrum of Phi values for each cut
print("\nCuts = ",Phi_Spectrum[0])
print("\nPhi Spectrum = ",Phi_Spectrum[1])

## Print all valid Phi_MIP values
Phi_MIP = phi_spectrum.get_Phi_MIP(Phi_Spectrum)
print("Phi MIP = ",Phi_MIP)
```



#### Implementing Alternate Solutions

The problem of degenerate core causes has several unofficial solutions, which can be implemented using the `solution` keyword passed to the `get_phi_spectrum` function. Keyword values include "Moon", "Smallest", "Largest", and `None`. The "Moon" solution throws away degenerate core causes/effects if multiple cause/effect repertoires have the same phi value (https://doi.org/10.3390/e21040405), the "Smallest" solution is to keep the smallest of the degenerate core cause/effect repertoires, and the "Largest" solution is to keep the largest of the degenerate core cause/effect repertoires. Since the smallest and largest repertoires are not guaranteed to be unique, these solutions retain all possible degenerate core causes/effects of a given size (i.e. biggest or smallest). Using keyword argument `None` keeps all degenerate core causes/effects regardless of their size.

An additional solution is suggested by Krohn and Ostwald, 2017 (https://doi.org/10.1093/nc/nix017). Here, the authors propose a new definition of Phi ("big Phi") based on the sum of phi values ("little phi") rather than a distance between constellations. This solution can be implemented via the `USE_SMALL_PHI_DIFFERENCE_FOR_CES_DISTANCE` keyword in the standard PyPhi configuration file (`pyphi_config.yml`). This solution can be used in combination with any of the previous solutions since it implements a completely different definition of Phi.

## References

### More information about core PyPhi can be found at:

- [Documentation for the latest stable
  release](http://pyphi.readthedocs.io/en/stable/)
- [Documentation for the latest (potentially unstable) development
  version](http://pyphi.readthedocs.io/en/latest/).
- Documentation is also available within the Python interpreter with the `help`
  function.

### Please cite these papers if you use this code:

Mayner WGP, Marshall W, Albantakis L, Findlay G, Marchman R, Tononi G. (2018)
[PyPhi: A toolbox for integrated information
theory](https://doi.org/10.1371/journal.pcbi.1006343). PLOS Computational
Biology 14(7): e1006343. <https://doi.org/10.1371/journal.pcbi.1006343>

```
@article{mayner2018pyphi,
  title={PyPhi: A toolbox for integrated information theory},
  author={Mayner, William GP and Marshall, William and Albantakis, Larissa and Findlay, Graham and Marchman, Robert and Tononi, Giulio},
  journal={PLoS Computational Biology},
  volume={14},
  number={7},
  pages={e1006343},
  year={2018},
  publisher={Public Library of Science},
  doi={10.1371/journal.pcbi.1006343},
  url={https://doi.org/10.1371/journal.pcbi.1006343}
}
```

Albantakis L, Oizumi M, Tononi G (2014). [From the Phenomenology to the
Mechanisms of Consciousness: Integrated Information Theory
3.0](http://www.ploscompbiol.org/article/info%3Adoi%2F10.1371%2Fjournal.pcbi.1003588).
PLoS Comput Biol 10(5): e1003588. doi: 10.1371/journal.pcbi.1003588.

```
@article{iit3,
    title={From the Phenomenology to the Mechanisms of Consciousness:
    author={Albantakis, Larissa AND Oizumi, Masafumi AND Tononi, Giulio},
    Integrated Information Theory 3.0},
    journal={PLoS Comput Biol},
    publisher={Public Library of Science},
    year={2014},
    month={05},
    volume={10},
    pages={e1003588},
    number={5},
    doi={10.1371/journal.pcbi.1003588},
    url={http://dx.doi.org/10.1371%2Fjournal.pcbi.1003588}
}
```

## Correspondence
Correspondence regarding the modified PyPhi code (PyPhi-Spectrum) should be directed to Jake Hanson, at [<jake.hanson@asu.edu>](mailto:jake.hanson@asu.edu). Correspondence regarding core PyPhi functionality should be directed to the original authors.
