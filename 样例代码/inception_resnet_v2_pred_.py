"""
读取文件夹里的图片，并用inception_resnet_v2模型识别。

参考：https://github.com/tensorflow/models/blob/master/slim/slim_walkthrough.ipynb
"""
import os
import tensorflow as tf
import numpy as np
from glob import glob
from tensorflow.contrib import slim
from datasets import imagenet
from nets import inception_resnet_v2
from preprocessing import inception_preprocessing

image_size = inception_resnet_v2.inception_resnet_v2.default_image_size

with tf.Graph().as_default():
    
    # 读取图片并预处理
    paths = glob('images/*.jpg')
    image_tensors = []
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        for e in paths:
            with open(e, 'rb') as file:
                content = file.read()
                image = tf.image.decode_jpeg(content, channels=3)
                processed_image = inception_preprocessing.preprocess_image(
                        image, image_size, image_size, is_training=False)
                image_tensors.append(sess.run(processed_image))
    # 将多个图片作为组合成一个tensor作为网络的输入
    processed_images = tf.stack(image_tensors)
    with slim.arg_scope(inception_resnet_v2.inception_resnet_v2_arg_scope()):
        logits, _ = inception_resnet_v2.inception_resnet_v2(processed_images,
                  num_classes=1001, is_training=False)
    probabilities = tf.nn.softmax(logits)
    
    init_fn = slim.assign_from_checkpoint_fn(
        os.path.join('../../', 'inception_resnet_v2_2016_08_30.ckpt'),
        slim.get_model_variables())
    probs = None
    with tf.Session() as sess:
        init_fn(sess) #初始化网络，读取保存的weights
        probs = sess.run(probabilities)
    sorted_index = np.argsort(-probs)
    sorted_index = sorted_index[:, :5] # 取出概率前5的标签
    
    names = imagenet.create_readable_names_for_imagenet_labels()
    for k in range(sorted_index.shape[0]):
        print('*'*10)
        print(paths[k])
        for i in range(5):
            index = sorted_index[k, i]
            print('Probability %0.2f%% => [%s]' % (probs[k, index] * 100, names[index]))