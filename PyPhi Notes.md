## PyPhi Notes

I have all concepts. Where do we calculate big phi as a distance between concepts?

I need to use `ces_distance` which means I need to convert my concepts into a cause-effect structure (constellation).

- How do I apply cuts to get a new TPM

#### Summary

I am not going to optimize over subsystems (assume subsystem size is fixed).

I will use the elementary functions of PyPhi to calculate all possible $\Phi$ values. Need to modify the CES so that it includes multiple concepts with the same $\phi$ values.

Most of the functions I will use are in `subsystem.py`. To use them, I need to pass the right arguments, which are often specific class atributes. Therefore, I need to know how to set these attibutes.

#### Get Directions

You find the MIP with a direction specified. How or where do you do this? Well, if you import direction then you have access to the directions:

```python
from pyphi import Direction

direction = Direction.CAUSE
```

#### Get Purviews

Before I can call potential purviews I need to generate mechanisms. Not sure why purviews would require mechanisms but it does. Regardless, I can use the `potential_purviews` method to get the purviews:

```python
potential_purviews(self, direction, mechanism, purviews=False)
```

#### Get Mechanisms

You get the mechanisms from `utils.powerset`. For example:

```python
mechanisms = utils.powerset(subsystem.node_indices, nonempty=True)
```

#### Miscellaneous

- There are different types of cuts: IIT 3.0 and "concept style"
- In line 784 of the PyPhi docs, we have `PICK_SMALLEST_PURVIEW`:

> ```
> When computing a |MIC| or |MIE|, it is possible for several MIPs to have
> the same |small_phi| value. If this setting is set to ``True`` the MIP with
> the smallest purview is chosen; otherwise, the one with largest purview is
> chosen.""",
> )
> ```

Though this functionality does not seem to be implemented in the code; the argument doesn't show up anywhere and if you test it the same purview element always comes back regardless of this value. In the test we ran, it chose the biggest purview element. Farnsworth 2021, it chose [R,C] as the core cause of P, rather than [R] or [C]. 

- The function returns the first max that is encountered, as it makes use of a strictly greater than relation. 

Line 713-715 of PyPhi:

```python
max_mip = max(
  self.find_mip(direction, mechanism, purview) for purview in purviews
)
```



So you either choose the smallest or largest purview element when calculating the core cause (maximally irreducible cause) or core effect (maximally irreducible effect)

#### Thoughts on Moon, 2019

>At the level of an individual mechanism, the integration postulate says that only mechanisms
>that specify integrated information can contribute to consciousness.

The exclusion postulate as applied to a mechanism requires first that only one cause exist [Oizumi, 2014]. The only cause is the maximally irreducible one. For something to exist it must make a difference. If you take away one, it didn't make a difference, if you take away the other, it doesn't make a difference - if you take away both, it makes a difference. There is redundancy.

To exist as a whole it must make a difference as a whole above and beyond the sum of its parts i.e. the same difference cannot be generated under a partition. 

The situation Moon described cannot exist. If AB and CD generate the same cause information about AB, then AB is contrained equally well by either. If you get rid of one, then AB is still constrained by the other; however, the only way getting rid of a purview element does not affect the state of AB is if the purview elements are entirely redundant. What this means is that, from the internal perspective of the system, the information coming from the disparate purview elements is entirely redundant. Logically, this implies that inputs from the two different purview elements are really just a single input, meaning one of the systems can be cut out without affecting the phi value.

Going in the other direction, imagine there are degenerate core effects, meaning a mechanism in a state constrains purview elements (as a whole) with equal magnitude. So A constrains B just as well as it constrains C. In this case, we can imagine B and C are copy c