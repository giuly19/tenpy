"""test of :class:`tenpy.models.XXZChain`.

.. todo ::
    more tests...
"""

from __future__ import division

import numpy as np
import numpy.testing as npt
import pprint

import tenpy.linalg.np_conserved as npc
from tenpy.models.xxz_chain import XXZChain


def test_XXZChain():
    pars = dict(L=4, Jxx=1., Jz=1., hz=0.0, bc_MPS='finite')
    chain = XXZChain(pars)
    chain.test_sanity()
    for Hb in chain.H_bond[1:]:   # check bond eigenvalues
        Hb2 = Hb.combine_legs([['pL', 'pR'], ['pL*', 'pR*']], qconj=[+1, -1])
        print Hb2.to_ndarray()
        W = npc.eigvalsh(Hb2)
        # TODO check eigenvalues for nozero hz, ...?
        npt.assert_array_almost_equal_nulp(np.sort(W),
                                           np.sort([-0.75, 0.25, 0.25, 0.25]),
                                           16**3)
    pars['hz'] = 0.2
    print "hz =", pars['hz']
    chain = XXZChain(pars)
    chain.test_sanity()
    Hb = chain.H_bond[2]  # the only central bonds: boundaries have different hz
    Hb2 = Hb.combine_legs([['pL', 'pR'], ['pL*', 'pR*']], qconj=[+1, -1])
    print Hb2.to_ndarray()
    W = npc.eigvalsh(Hb2)
    print W
    npt.assert_array_almost_equal_nulp(np.sort(W),
                                       np.sort([-0.75,
                                                0.25 - 2*0.5*0.5*pars['hz'],
                                                0.25,
                                                0.25 + 2.*0.5*0.5*pars['hz']]),
                                       16**3)
    pars['bc_MPS'] = 'infinite'

    for L in [2, 3, 4, 5, 6]:
        print "L =", L
        pars['L'] = L
        chain = XXZChain(pars)
        pprint.pprint(chain.coupling_terms)
        assert len(chain.H_bond) == L
        Hb0 = chain.H_bond[0]
        for Hb in chain.H_bond[1:]:
            assert(npc.norm(Hb - Hb0, np.inf) == 0.)  # exactly equal
