import tensorflow as tf
mnist = tf.keras.datasets.mnist

n_nodes = 512
n_classes = 10
batch_size = 100

x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

def neural_network_model(data):
    layer_1 = {'weights':tf.Variable(tf.random_normal([784, n_nodes])),
                      'biases':tf.Variable(tf.random_normal([n_nodes]))}
    output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes, n_classes])),
                    'biases':tf.Variable(tf.random_normal([n_classes])),}
    l1 = tf.add(tf.matmul(data,layer_1['weights']), layer_1['biases'])
    l1 = tf.nn.relu(l1)
    output = tf.matmul(l1,output_layer['weights']) + output_layer['biases']
    return output

def train_neural_network(x):
    prediction = neural_network_model(x)
    cost = tf.reduce_mean( tf.nn.sparse_softmax_cross_entropy_with_logits(logits=prediction,labels=y) )
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    hm_epochs = 5
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        for epoch in range(hm_epochs):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c
            print('Epoch', epoch, 'completed out of',hm_epochs,'loss:',epoch_loss)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:',accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))

train_neural_network(x)