#!/usr/bin/env python
# coding: utf-8

import itertools

import numpy as np
import pandas as pd
import plotly
import scipy.spatial
from plotly import express as px
from plotly import graph_objs as go
from umap import UMAP

from . import relations as rel


def flatten(iterable):
    return itertools.chain.from_iterable(iterable)


def feature_matrix(ces, relations):
    """Return a matrix representing each cause and effect in the CES.

    .. note::
        Assumes that causes and effects have been separated.
    """
    N = len(ces)
    M = len(relations)
    # Create a mapping from causes and effects to indices in the feature matrix
    index_map = {purview: i for i, purview in enumerate(ces)}
    # Initialize the feature vector
    features = np.zeros([N, M])
    # Assign features
    for j, relation in enumerate(relations):
        indices = [index_map[relatum] for relatum in relation.relata]
        # Create the column corresponding to the relation
        relation_features = np.zeros(N)
        # Assign 1s where the cause/effect purview is involved in the relation
        relation_features[indices] = 1
        # Assign the feature column to the feature matrix
        features[:, j] = relation_features
    return features


def get_coords(data, y=None, **params):
    umap = UMAP(
        n_components=3, metric="euclidean", n_neighbors=30, min_dist=0.5, **params,
    )
    return umap.fit_transform(data, y=y)


def relation_vertex_indices(features, j):
    """Return the indices of the vertices for relation ``j``."""
    return features[:, j].nonzero()[0]


def all_triangles(vertices):
    """Return all triangles within a set of vertices."""
    return itertools.combinations(vertices, 3)


def all_edges(vertices):
    """Return all edges within a set of vertices."""
    return itertools.combinations(vertices, 2)


def make_label(nodes, node_labels=None):
    if node_labels is not None:
        nodes = node_labels.indices2labels(nodes)
    return "".join(nodes)


def label_mechanism(mice):
    return make_label(mice.mechanism, node_labels=mice.node_labels)


def label_purview(mice):
    return make_label(mice.purview, node_labels=mice.node_labels)


def vertex_sizes(min_size, max_size, ces):
    phis = np.array(
        [(distinction.cause.phi, distinction.effect.phi) for distinction in ces]
    )
    min_phi = phis.min()
    max_phi = phis.max()
    return min_size + (((phis - min_phi) * (max_size - min_size)) / (max_phi - min_phi))


def plot_relations(
    ces,
    relations,
    max_order=3,
    cause_effect_offset=(0.5, 0, 0),
    vertex_size_range=(10, 30),
):
    # Select only relations <= max_order
    relations = list(filter(lambda r: len(r.relata) <= max_order, relations))
    # Separate CES into causes and effects
    separated_ces = rel.separate_ces(ces)

    # Initialize figure data
    figure_data = []

    # Dimensionality reduction
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Create the features for each cause/effect based on their relations
    features = feature_matrix(separated_ces, relations)

    # Now we get one set of coordinates for the CES; these will then be offset to
    # get coordinates for causes and effects separately, so that causes/effects
    # are always near each other in the embedding.

    # Collapse rows of cause/effect belonging to the same distinction
    # NOTE: This depends on the implementation of `separate_ces`; causes and
    #       effects are assumed to be adjacent in the returned list
    umap_features = features[0::2] + features[1::2]
    distinction_coords = get_coords(umap_features)
    # Duplicate causes and effects so they can be plotted separately
    coords = np.empty(
        (distinction_coords.shape[0] * 2, distinction_coords.shape[1]),
        dtype=distinction_coords.dtype,
    )
    coords[0::2] = distinction_coords
    coords[1::2] = distinction_coords
    # Add a small offset to effects to separate them from causes
    coords[1::2] += cause_effect_offset

    # Purviews
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Extract vertex indices for plotly
    x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
    # Get mechanism and purview labels
    mechanism_labels = list(map(label_mechanism, separated_ces))
    purview_labels = list(map(label_purview, separated_ces))
    # Make the labels
    labels = go.Scatter3d(
        x=x, y=y, z=z, mode="text", text=purview_labels, name="Labels", showlegend=True,
    )
    figure_data.append(labels)
    # Compute size and color
    size = vertex_sizes(vertex_size_range[0], vertex_size_range[1], ces)
    color = list(flatten([("red", "green")] * len(ces)))
    vertices = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        name="Purviews",
        showlegend=True,
        marker=dict(size=size, color=color),
    )
    figure_data.append(vertices)

    # 2-relations
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Get edges from all relations
    edges = list(
        flatten(
            relation_vertex_indices(features, j)
            for j in range(features.shape[1])
            if features[:, j].sum() == 2
        )
    )
    if edges:
        # Convert to DataFrame
        edges = pd.DataFrame(
            dict(
                x=x[edges],
                y=y[edges],
                z=z[edges],
                line_group=flatten(zip(range(len(edges) // 2), range(len(edges) // 2))),
            )
        )
        # Plot edges
        edge_figure = px.line_3d(edges, x="x", y="y", z="z", line_group="line_group")
        figure_data.extend(edge_figure.data)

    # 3-relations
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Get triangles from all relations
    triangles = [
        relation_vertex_indices(features, j)
        for j in range(features.shape[1])
        if features[:, j].sum() == 3
    ]
    if triangles:
        # Extract triangle indices
        i, j, k = zip(*triangles)
        mesh = go.Mesh3d(
            # x, y, and z are the coordinates of vertices
            x=x,
            y=y,
            z=z,
            # i, j, and k are the vertices of triangles
            i=i,
            j=j,
            k=k,
            # Intensity of each vertex, which will be interpolated and color-coded
            intensity=np.linspace(0, 1, len(x), endpoint=True),
            opacity=0.2,
            colorscale="viridis",
            showscale=False,
            name="3-Relations",
            showlegend=True,
        )
        figure_data.append(mesh)

    # Create figure
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    axis = dict(
        showbackground=True,
        showline=True,
        zeroline=True,
        showgrid=True,
        gridcolor="lightgray",
        showticklabels=False,
        title="",
        showspikes=True,
        autorange=True,
        backgroundcolor="white",
    )
    layout = go.Layout(
        showlegend=True,
        scene=dict(xaxis=dict(axis), yaxis=dict(axis), zaxis=dict(axis)),
        hovermode="closest",
        title="",
        autosize=True,
    )
    # Merge figures
    return go.Figure(data=figure_data, layout=layout)