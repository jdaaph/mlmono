import tensorflow as tf

from ml.base import trainer_utils
from ml.base.base_utils import find_subclass_by_name


class MLTrainer(object):
    def __init__(self, trainer_config):
        self.trainer_config = trainer_config
        self.train_hooks = []
        self.train_ops = []

        self.loss = None
        self.optimizer = None

    @classmethod
    def from_config(cls, trainer_config):
        subcls = find_subclass_by_name(cls, trainer_config.trainer_name)
        return subcls.from_config(trainer_config)

    def register_to_graph(self, graph):
        raise NotImplementedError


class DefaultTrainer(MLTrainer):
    @classmethod
    def from_config(cls, trainer_config):
        self = cls(trainer_config)

        # Optimizer.
        lr = trainer_config.learning_rate
        if (trainer_config.optimizer).lower() == 'adam':
            self.optimizer = tf.train.AdamOptimizer(
                learning_rate=lr)
        elif (trainer_config.optimizer).lower() == 'sgd':
            self.optimizer = tf.train.AdamOptimizer(
                learning_rate=lr)

        # Train_Hooks.
        examples_sec_hook = trainer_utils.ExamplesPerSecondHook(
            params.train_batch_size, every_n_steps=10)
        self.train_hooks += [examples_sec_hook]
        return self

    def register_to_graph(self, graph):
        # Register loss in this method as it requries to connect to graph.
        self.loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(
            logits=logits_train, labels=tf.cast(labels, dtype=tf.int32)))

    def register_op_and_hook(self):
        pass
