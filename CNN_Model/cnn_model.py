import tensorflow as tf
import os
from tqdm import tqdm

from CNN_Model.utils.mnist_op_dataset import DataSetGenerator


class Model(object):
    def __init__(self, batch_size=100, hidden_size=1024, n_output=16):
        self.sess = tf.compat.v1.Session()
        self.HIDDEN_SIZE = hidden_size
        self.BATCH_SIZE = batch_size
        self.N_OUTPUT = n_output
        self.N_BATCH = 0

    @staticmethod
    def weight_variable(shape):
        initial = tf.random.truncated_normal(shape, stddev=0.10)
        return tf.Variable(initial, name="w")

    @staticmethod
    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial, name="b")

    @staticmethod
    def conv2d(x, w):
        return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='SAME')

    @staticmethod
    def max_pool_2x2(x):
        return tf.nn.max_pool2d(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    def train_model(self, epoch=21, learning_rate=1e-4, regular_coef=5e-4, model_dir='./model/', model_name='model'):
        mnist_operator = DataSetGenerator()
        mnist_operator.load_dataset(save_dir='./utils/')
        self.N_BATCH = mnist_operator.train.images.shape[0] // self.BATCH_SIZE
        x = tf.compat.v1.placeholder(tf.float32, [None, 784], name='image_input')
        y = tf.compat.v1.placeholder(tf.float32, [None, self.N_OUTPUT])
        rate = tf.compat.v1.placeholder(tf.float32, name="rate")

        x_image = tf.reshape(x, [-1, 28, 28, 1])
        with tf.compat.v1.variable_scope("conv1"):
            w_conv1 = self.weight_variable([5, 5, 1, 32])
            b_conv1 = self.bias_variable([32])
            h_conv1 = tf.nn.relu(self.conv2d(x_image, w_conv1) + b_conv1)
            h_pool1 = self.max_pool_2x2(h_conv1)

        with tf.compat.v1.variable_scope("conv2"):
            w_conv2 = self.weight_variable([5, 5, 32, 64])
            b_conv2 = self.bias_variable([64])
            h_conv2 = tf.nn.relu(self.conv2d(h_pool1, w_conv2) + b_conv2)
            h_pool2 = self.max_pool_2x2(h_conv2)

        with tf.compat.v1.variable_scope("fc1"):
            w_fc1 = self.weight_variable([7 * 7 * 64, self.HIDDEN_SIZE])
            b_fc1 = self.bias_variable([self.HIDDEN_SIZE])
            h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
            h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)
            h_fc1_drop = tf.nn.dropout(h_fc1, rate=rate)

        with tf.compat.v1.variable_scope("fc2"):
            w_fc2 = self.weight_variable([self.HIDDEN_SIZE, self.N_OUTPUT])
            b_fc2 = self.bias_variable([self.N_OUTPUT])
            h_fc2 = tf.matmul(h_fc1_drop, w_fc2) + b_fc2

        regularization = (tf.nn.l2_loss(w_fc1) + tf.nn.l2_loss(b_fc1) + tf.nn.l2_loss(w_fc2) + tf.nn.l2_loss(b_fc1))
        prediction = tf.nn.softmax(h_fc2, name="prediction")
        predict_op = tf.argmax(prediction, 1, name="predict_op")

        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=prediction))
        loss_re = loss + regular_coef * regularization

        train_step = tf.compat.v1.train.AdamOptimizer(learning_rate).minimize(loss_re)

        correct_prediction = tf.equal(predict_op, tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        saver = tf.compat.v1.train.Saver()
        tf.compat.v1.add_to_collection("predict_op", predict_op)

        print("Start training....")
        with tf.compat.v1.Session() as sess:
            sess.run(tf.compat.v1.global_variables_initializer())
            for i in tqdm(range(epoch * self.N_BATCH)):
                epoch = i // self.N_BATCH
                batch_xs, batch_ys = mnist_operator.train.next_batch(self.BATCH_SIZE)
                sess.run(train_step, feed_dict={x: batch_xs, y: batch_ys, rate: 0.3})
                if epoch % 10 == 0 and (i + 1) % self.N_BATCH == 0:
                    acc = []
                    for j in range(mnist_operator.test.labels.shape[0] // self.BATCH_SIZE):
                        batch_xs_test, batch_ys_test = mnist_operator.test.next_batch(self.BATCH_SIZE)
                        test_acc = sess.run(accuracy, feed_dict={x: batch_xs_test, y: batch_ys_test, rate: 0.0})
                        acc.append(test_acc)
                    print()
                    print("Iter" + str(epoch) + ",Testing Accuracy = " + str(sum(acc) / len(acc)))
                    if not os.path.exists(model_dir):
                        os.mkdir(model_dir)
                    saver.save(sess, model_dir + '/' + model_name, global_step=epoch)

    def load_model(self, meta, path):
        saver = tf.compat.v1.train.import_meta_graph(meta)
        saver.restore(self.sess, tf.train.latest_checkpoint(path))

    def predict(self, x):
        predict = tf.compat.v1.get_collection('predict_op')[0]
        graph = tf.compat.v1.get_default_graph()
        input_x = graph.get_operation_by_name("image_input").outputs[0]
        rate = graph.get_operation_by_name("rate").outputs[0]
        return self.sess.run(predict, feed_dict={input_x: x, rate: 0.0})[0:]
