## PyPhi Notes

#### Summary

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

- In line 784 of the PyPhi docs, we have `PICK_SMALLEST_PURVIEW`

> ```
> When computing a |MIC| or |MIE|, it is possible for several MIPs to have
> the same |small_phi| value. If this setting is set to ``True`` the MIP with
> the smallest purview is chosen; otherwise, the one with largest purview is
> chosen.""",
> )
> ```

So you either choose the smallest or largest purview element when calculating the core cause (maximally irreducible cause) or core effect (maximally irreducible effect)