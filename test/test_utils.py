#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import numpy as np

from cyphi import utils, constants
from cyphi.network import Network


def test_phi_eq():
    phi = 0.5
    close_enough = phi - constants.EPSILON/2
    not_quite = phi - constants.EPSILON*2
    assert utils.phi_eq(phi, close_enough)
    assert not utils.phi_eq(phi, not_quite)
    assert not utils.phi_eq(phi, (phi - phi))


def test_marginalize_out(standard):
    marginalized_distribution = utils.marginalize_out(standard.nodes[0],
                                                      standard.tpm)
    assert np.array_equal(marginalized_distribution,
                            np.array([[[[0.,  0.,  0.5],
                                        [1.,  1.,  0.5]],
                                       [[1.,  0.,  0.5],
                                        [1.,  1.,  0.5]]]]))


def test_purview_max_entropy_distribution():
    # Individual setUp
    size = 3
    state = (0, 1, 0)
    past_state = (1, 1, 0)
    tpm = np.ones([2] * size + [size]).astype(float) / 2
    network = Network(tpm, state, past_state)

    max_ent = utils.max_entropy_distribution(network.nodes[0:2], network)
    assert max_ent.shape == (2, 2, 1)
    assert np.array_equal(max_ent,
                          (np.ones(4) / 4).reshape((2, 2, 1)))
    assert max_ent[0][1][0] == 0.25


def test_combs_for_1D_input():
    n, k = 3, 2
    data = np.arange(n)
    assert np.array_equal(utils.combs(data, k),
                          np.asarray([[0, 1],
                                      [0, 2],
                                      [1, 2]]))


def test_combs_r_is_0():
    n, k = 3, 0
    data = np.arange(n)
    assert np.array_equal(utils.combs(data, k), np.asarray([]))


def test_comb_indices():
    n, k = 3, 2
    data = np.arange(6).reshape(2, 3)
    assert np.array_equal(data[:, utils.comb_indices(n, k)],
                          np.asarray([[[0, 1],
                                       [0, 2],
                                       [1, 2]],
                                      [[3, 4],
                                       [3, 5],
                                       [4, 5]]]))


def test_powerset():
    a = np.arange(2)
    assert list(utils.powerset(a)) == [(), (0,), (1,), (0, 1)]


def test_hamming_matrix():
    H = utils._hamming_matrix(3)
    answer = np.array([[0.,  1.,  1.,  2.,  1.,  2.,  2.,  3.],
                       [1.,  0.,  2.,  1.,  2.,  1.,  3.,  2.],
                       [1.,  2.,  0.,  1.,  2.,  3.,  1.,  2.],
                       [2.,  1.,  1.,  0.,  3.,  2.,  2.,  1.],
                       [1.,  2.,  2.,  3.,  0.,  1.,  1.,  2.],
                       [2.,  1.,  3.,  2.,  1.,  0.,  2.,  1.],
                       [2.,  3.,  1.,  2.,  1.,  2.,  0.,  1.],
                       [3.,  2.,  2.,  1.,  2.,  1.,  1.,  0.]])
    assert (H == answer).all()


def test_bipartition():
    answer = [((), (0, 1, 2)), ((0,), (1, 2)), ((1,), (0, 2)), ((0, 1), (2,))]
    assert answer == utils.bipartition(tuple(range(3)))
    # Test with empty input
    assert [] == utils.bipartition(())


def test_emd_same_distributions():
    a = np.ones((2, 2, 2)) / 8
    b = np.ones((2, 2, 2)) / 8
    assert utils.hamming_emd(a, b) == 0.0


def test_emd_different_shapes():
    a = np.ones((2, 1, 2)) / 4
    b = np.ones((2, 2, 2)) / 8
    with pytest.raises(ValueError):
        assert utils.hamming_emd(a, b)


def test_emd_mismatched_size():
    a = np.ones((2, 2, 2, 2)) / 16
    b = np.ones((2, 2, 2)) / 8
    with pytest.raises(ValueError):
        assert utils.hamming_emd(a, b)
