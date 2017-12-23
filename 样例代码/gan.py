import sys
import numpy as np
import tensorflow as tf
import skimage.io
from tensorflow.examples.tutorials.mnist import input_data

def weight_variable(shape):
    """
    生成weight variable
    """
    init = tf.truncated_normal(shape, mean=0.0, stddev=1.0)
    return tf.Variable(init)

def bias_variable(shape):
    init = tf.constant(1.0, shape=shape)
    return tf.Variable(init)

def conv2d_transpose(value, filters, stride=1):
    ishape = tf.shape(value)
    batch_size = ishape[0]
    ih = ishape[1]
    iw = ishape[2]
    fshape = tf.shape(filters)
    fh = fshape[0]
    fw =fshape[1]
    oc = fshape[2]
    ow = (iw-1)*stride+fw
    oh = (ih-1)*stride+fh
    output_shape = tf.stack([batch_size, oh, ow, oc])
    return tf.nn.conv2d_transpose(value, filters, output_shape, 
                                  strides=(1, stride, stride, 1),
                                    padding='VALID')

def conv2d(features, filters, stride=1, padding='VALID'):
    if padding == 'SAME':#tf的padding same并不是输入输出一致的意思
        ishape = tf.shape(features)
        h = ishape[1]
        w = ishape[2]
        fshape = tf.shape(filters)
        fh = fshape[0]
        fw = fshape[1]
        pw = fw+(w-1)*stride - w
        ph = fh+(h-1)*stride - h
        pad = ((0,0), (pw//2, pw-pw//2), (ph//2, ph-ph//2), (0,0))
        features = tf.pad(features, pad)
    return tf.nn.conv2d(features, filters, strides=(1,stride,stride,1), 
                        padding='VALID')

def batch_normalization(features, offset, scale):
    mean, var = tf.nn.moments(features, axes=[0])
    return tf.nn.batch_normalization(features, mean, var, offset, scale, 1e-6)

def get_block_variable(shape):
    w = weight_variable(shape)
    b = bias_variable((shape[-1],))
    #o = tf.Variable(tf.constant(0.0, shape=(shape[-1],)))
    #s = tf.Variable(tf.constant(1.0, shape=(shape[-1],)))
    return w, b#, o, s

class Generator(object):
    
    def __init__(self, channels):
        self.channels = channels
        self.convt_1 = [weight_variable((3,3,8,channels)), bias_variable((8,))]
        self.convt_2 = [weight_variable((3,3,16,8)), bias_variable((16,))]
        self.convt_3 = [weight_variable((8,8,1,16)), bias_variable((1,))]
        self.var_list = self.convt_1+self.convt_2+self.convt_3

    def __call__(self, rand_num):
        _, c = rand_num.get_shape().as_list()
        assert c == self.channels
        x = tf.reshape(rand_num, (-1,1,1,c))
        # batchx3x3x8
        with tf.name_scope('generative'):
            with tf.name_scope('convt_1'):
                x = conv2d_transpose(x, self.convt_1[0], stride=2)
                x += self.convt_1[1]
                x = tf.nn.relu(x)
            # batchx11x11x16
            with tf.name_scope('convt_2'):
                x = conv2d_transpose(x, self.convt_2[0], stride=4)
                x += self.convt_2[1]
                x = tf.nn.relu(x)
            # batchx28x28x1
            with tf.name_scope('convt_3'):
                x = conv2d_transpose(x, self.convt_3[0], stride=2)
                x += self.convt_3[1]
                x = tf.nn.relu(x)
        x = tf.nn.sigmoid(x)
        return x

class Discriminator(object):
    
    def __init__(self):
        self.conv1 = get_block_variable((7,7,1,32))
        self.res_conv1 = get_block_variable((1,1,32,64))
        self.res_conv2 = get_block_variable((3,3,64,128))
        self.res_conv3 = get_block_variable((1,1,128,32))
        self.conv2 = get_block_variable((3,3,32,64))
        self.conv3 = get_block_variable((3,3,64,64))
        self.conv4 = get_block_variable((2,2,64,1))
        self.var_list = (self.conv1 + self.conv2 + self.conv3 + self.conv4 +
                    self.res_conv1 + self.res_conv2 + self.res_conv3)

    def __call__(self, img, name):
        x = img
        with tf.name_scope(name):
            # batchx22x22x16
            with tf.name_scope('conv_1'):
                x = conv2d(x, self.conv1[0], stride=1) + self.conv1[1]
                #x = batch_normalization(x, self.conv1[2], self.conv1[3])
                x = tf.nn.tanh(x)
        
            # batchx11x11x16
            with tf.name_scope('max_pool'):
                x = tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                                strides=[1, 2, 2, 1], padding='VALID')
            # batchx11x11x16
            with tf.name_scope('resnet_1'):
                shortcut = x
                x = conv2d(x, self.res_conv1[0], stride=1) + self.res_conv1[1]
                #x = batch_normalization(x, self.res_conv1[2], self.res_conv1[3])
                x = tf.nn.tanh(x)
                # batchx11x11x8
        
                x = conv2d(x, self.res_conv2[0], stride=2, padding='SAME') + self.res_conv2[1]
                #x = batch_normalization(x, self.res_conv2[2], self.res_conv2[3])
                x = tf.nn.tanh(x)
                # batchx11x11x16
                
                x = conv2d(x, self.res_conv3[0], stride=1) + self.res_conv3[1]
                #x = batch_normalization(x, self.res_conv3[2], self.res_conv3[3])
                x = tf.add(x, shortcut)
                x = tf.nn.tanh(x)
                
            # batchx5x5x32
            with tf.name_scope('conv_2'):
                x = conv2d(x, self.conv2[0], stride=2) + self.conv2[1]
                #x = batch_normalization(x, self.conv2[2], self.conv2[3])
                x = tf.nn.tanh(x)
                
            # batchx2x2x64
            with tf.name_scope('conv_3'):
                x = conv2d(x, self.conv3[0], stride=2) + self.conv3[1]
                #x = batch_normalization(x, self.conv3[2], self.conv3[3])
                x = tf.nn.tanh(x)
        
            # batchx1x1x1
            with tf.name_scope('conv_4'):
                x = conv2d(x, self.conv4[0], stride=2) + self.conv4[1]
                #x = batch_normalization(x, self.conv4[2], self.conv4[3])
                x = tf.nn.tanh(x)
                x = tf.nn.sigmoid(x)
        x = tf.reshape(x, (-1, 1))
        return x

def save_mnist_img(img, name):
    assert np.prod(img.shape) == 28*28*100
    img = np.reshape(img, (100, 28, 28))
    tmp = np.zeros((280, 280), np.float32)
    for k in range(10):
        for t in range(10):
            tmp[k*28:(k+1)*28, t*28:(t+1)*28] = img[k*t, ...]
    skimage.io.imsave(name, tmp)

def main():
    # batch_xs, batch_ys = mnist.train.next_batch(100)
    # mnist.test.images
    # tf.reshape(x, [-1, 28, 28, 1])，mnist图片拉成行向量了，需要reshape。
    
    mnist = input_data.read_data_sets('mnist', one_hot=False)
    batch_size = 512
    epoch = 100
    disc_step = 1
    iter_num = mnist.train.num_examples // batch_size

    save_mnist_img(mnist.test.images[:100], 'test.jpg')
    
    rand_chan = 64
    rand_num = tf.placeholder(tf.float32, shape=(None, rand_chan))
    img = tf.placeholder(tf.float32, shape=(None, 28, 28, 1))

    generator = Generator(rand_chan)
    G = generator(rand_num)
    
    discriminator = Discriminator()
    true_D = discriminator(img, 'true')
    fake_D = discriminator(G, 'fake')
    
    d_loss = -tf.reduce_mean(tf.log(true_D) + tf.log(1-fake_D))#趋向于0
    g_loss = -tf.reduce_mean(tf.log(fake_D)) #g_loss趋向于0
    d_opt = tf.train.MomentumOptimizer(1e-4, 0.9)
    g_opt = tf.train.MomentumOptimizer(1e-2, 0.9)
    d_update = d_opt.minimize(d_loss, var_list=discriminator.var_list)
    g_update = g_opt.minimize(g_loss, var_list=generator.var_list)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for e in range(epoch):
            for i in range(iter_num):
                for k in range(disc_step):
                    rands = np.random.standard_normal((batch_size,rand_chan))
                    true_img, _ = mnist.train.next_batch(batch_size)
                    true_img = np.reshape(true_img, (-1,28,28,1))
                    sess.run(d_update, feed_dict={img:true_img, rand_num:rands})
                    sys.stdout.write('epcho(%d/%d), step(%d/%d), d loss: %f'%(e, epoch,
                          i, iter_num, d_loss.eval({img:true_img, rand_num:rands})))
                rands = np.random.standard_normal((batch_size,rand_chan))
                sess.run(g_update, feed_dict={ rand_num:rands})
                sys.stdout.write(', g loss: %f.\n'%(g_loss.eval(feed_dict={
                    rand_num:rands})))
            fake_img = G.eval(feed_dict={
                            rand_num:np.random.standard_normal((10*10,rand_chan))})
            save_mnist_img(fake_img, 'epoch-%d.jpg'%e)

if __name__ == '__main__':
    main()
