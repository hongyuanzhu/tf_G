import warnings

import tensorflow as tf
import numpy as np

from src.pagerank.pagerank import PageRank
from src.utils.utils import Utils


class NumericPageRank(PageRank):
    def __init__(self, sess, name, graph, beta, T):
        PageRank.__init__(self, sess, name)
        self.G = graph

        self.beta = beta
        self.T = T
        self.T.attach(self)
        self.v = tf.Variable(tf.fill([1, self.G.n], tf.pow(self.G.n_tf, -1)),
                             name=self.G.name + "_" + self.name + "_Vi")
        self.run(tf.variables_initializer([self.v]))

    def ranks(self, convergence=1.0, steps=0, personalized=None):
        self.pagerank_vector_tf(convergence, steps, personalized)
        ranks = tf.map_fn(
            lambda x: [x, tf.gather(tf.reshape(self.v, [self.G.n]), x)],
            tf.transpose(
                tf.py_func(Utils.ranked,
                           [tf.scalar_mul(-1, self.v)], tf.int64)),
            dtype=[tf.int64, tf.float32])
        return np.concatenate(self.run(ranks), axis=1)

    def update(self, edge, change):
        warnings.warn('PageRank auto-update not implemented yet!')
