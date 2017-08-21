# -*- coding: utf-8 -*-
# !/usr/bin/env python

import numpy as np
import sklearn.preprocessing as prep
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# Xavier 就是让权重满足0均值，同时方差为 2/(Nin+Nout)
# 分布可以用均匀分布或者高斯分布
def xavier_init(fan_in, fan_out, constant=1):
	low = -constant * np.sqrt(6.0 / (fan_in+fan_out))
	high =  constant * np.sqrt(6.0 / (fan_in+fan_out))
	return tf.random_uniform((fan_in, fan_out),
		minval = low, maxval = high,
		dtype = tf.float32)

# 构建函数：n_input(输入变量数)
# n_hidden(隐含节点数)
# transfer_function(隐含层激活函数，默认为softplus)
# optimizer(优化器，默认为Adam)
# scale(高斯噪声系数，默认为0.1)。
class AdditiveGaussianNoiseAutoencoder(object):
	def __init__(self, n_input, n_hidden, transfer_function=tf.nn.softplus,
		optimizer=tf.train.AdamOptimizer(), scale=0.1):
		self.n_input = n_input
		self.n_hidden = n_hidden
		self.transfer = transfer_function
		self.scale = tf.placeholder(tf.float32)
		self.training_scale = scale
		network_weights = self._initialize_weights()
		self.weights = network_weights

		# 1. 建立一个能提取特征的隐含层，先将输入 x 加上噪声
		# 2. 使用 transfer 对 (wx+b) 进行激活函数处理。
		# 3. 经过隐含层后，在输出层进行数据复原、重建操作（即建立 reconstruction层）
		# 4. 注意：输出层没有使用激活函数
		self.x = tf.placeholder(tf.float32, [None, self.n_input])
		self.hidden = self.transfer(tf.add(tf.matmul(
						self.x + scale * tf.random_normal((n_input,)),
						self.weights['w1']), self.weights['b1']))
		self.reconstruction = tf.add(tf.matmul(self.hidden,
								self.weights['w2']), self.weights['b2'])

		# 定义损失函数和优化器
		# 这里使用 平方误差(Squared Error) 作为 cost
		self.cost = 0.5 * tf.reduce_sum(tf.pow(tf.subtract(self.reconstruction, self.x), 2.0))
		self.optimizer = optimizer.minimize(self.cost)

		# TensorFlow 的全局参数优化器 tf.global_variables_initializer
		init = tf.global_variables_initializer()
		self.sess = tf.Session()
		self.sess.run(init)

	# 返回一个适合激活函数的权重初始分布
	def _initialize_weights(self):
		all_weights = dict()
		all_weights['w1'] = tf.Variable(xavier_init(self.n_input,
								self.n_hidden))
		all_weights['b1'] = tf.Variable(tf.zeros([self.n_hidden],
								dtype = tf.float32))
		all_weights['w2'] = tf.Variable(tf.zeros([self.n_hidden,
								self.n_input], dtype = tf.float32))
		all_weights['b2'] = tf.Variable(tf.zeros([self.n_input],
								dtype = tf.float32))
		return all_weights

	# 用一个 batch 数据进行训练并返回当前的损失 cost
	def partial_fit(self, X):
		cost, opt = self.sess.run((self.cost, self.optimizer),
						feed_dict = {self.x: X, self.scale: self.training_scale})
		return cost

	# 不训练，只求 cost，在测试集上对模型性能进行评测。		
	def calc_total_cost(self, X):
		return self.sess.run(self.cost, feed_dict = {self.x: X, 
			self.scale: self.training_scale})

	# 提供一个接口来获取抽象后的特征
	def transform(self, X):
		return self.sess.run(self.hidden, feed_dict = {self.x: X, 
			self.scale: self.training_scale})

	# 将隐含层的输出结果作为输入
	# 通过之后的重建层将提取到的高阶特征复原为原始数据
	def generate(self, hidden = None):
		if hidden is None:
			hidden = np.random_normal(size = self.weights['b1'])
		return self.sess.run(self.reconstruction,
				 feed_dict = {self.hidden: hidden})

	# 输入是 原数据， 输出是 复员后的数据。
	def reconstruct(self, X):
		return self.sess.run(self.reconstruction,feed_dict = {self.x: X, 
			self.scale: self.training_scale})

	def getWeights(self):
		return self.sess.run(self.weights['w1'])

	def getBiases(self):
		return self.sess.run(self.weights['b1'])

def getDataSet():
	return input_data.read_data_sets('MNIST_data', one_hot=True)

# 标准化处理：让数据变成0均值且标准差为1的分布
def standard_scale(X_train, X_test):
	preprocessor = prep.StandardScaler().fit(X_train)
	X_train = preprocessor.transform(X_train)
	X_test = preprocessor.transform(X_test)
	return X_train, X_test

# 不放回抽样，获取随机block函数
def get_random_block_from_data(data, batch_size):
	start_index = np.random.randint(0, len(data)-batch_size)
	return data[start_index:(start_index + batch_size)]	

def main():
	mnist = getDataSet()
	X_train, X_test = standard_scale(mnist.train.images, mnist.test.images)
	n_samples = int(mnist.train.num_examples)
	training_epochs = 10
	batch_size = 128
	display_step = 1

	autoencoder = AdditiveGaussianNoiseAutoencoder(n_input = 784,
					n_hidden = 200,
					transfer_function = tf.nn.softplus,
					optimizer = tf.train.AdamOptimizer(learning_rate = 0.001),
					scale = 0.01)

	# 1. 随机抽取一个 block 的数据
	# 2. 计算当前 cost
	# 3. 求出 avg_cost
	# 4. 显示当前的迭代数和每一轮的 avg_cost
	for epoch in range(training_epochs):
		avg_cost = 0
		total_batch = int(n_samples / batch_size)
		for i in range(total_batch):
			batch_xs = get_random_block_from_data(X_train, batch_size)
			cost = autoencoder.partial_fit(batch_xs)
			avg_cost += cost / n_samples * batch_size

		if epoch % display_step == 0:
			print("Epoch:", '%04d' % (epoch+1), "cost=:", "{:.9f}".format(avg_cost))	

	# 对训练完的模型进行性能测试
	print('Total cost: ' + str(autoencoder.calc_total_cost(X_test)))

if __name__ == '__main__':
	main()














