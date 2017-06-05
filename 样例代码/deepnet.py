"""
Kaggle上的Quora question pairs比赛，按照Abhishek Thakur的思路，把整个流程跑通了

讲解的文章https://www.linkedin.com/pulse/duplicate-quora-question-abhishek-thakur。
里面有两个实现，基于传统机器学习模型的实现和基于深度学习的实现，这段脚本是后者。

基本的思路比较简单，不清楚的地方也添加了注释。使用GloVe的词向量库，把每个句子转换成词向量
拼接起来的矩阵，之后就可以搭建神经网络了。自己在Convolution1D、LSTM和DropOut那一块儿还
有些迷糊。
"""
import pandas as pd
import numpy as np
from tqdm import tqdm
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from keras.layers import Merge
from keras.layers import TimeDistributed, Lambda
from keras.layers import Convolution1D, GlobalMaxPooling1D
from keras.callbacks import ModelCheckpoint
from keras import backend as K
from keras.layers.advanced_activations import PReLU
from keras.preprocessing import sequence, text
training = True
training = False
data0 = pd.read_csv('../input/quora_duplicate_questions.tsv', sep='\t')
data = pd.read_csv("../input/test.csv")
if training:
    y = data0.is_duplicate.values

#%% 数据预处理，将文本转换成索引矩阵
#
'''Class for vectorizing texts, or/and turning texts into sequences 
(=list of word indexes, where the word of rank i in the dataset 
(starting at 1) has index i).
'''
tk = text.Tokenizer(num_words=200000)

max_len = 40

#也就是在这些数据上构建单词库
tk.fit_on_texts(list(data.question1.astype('str').values) +
                list(data.question2.astype('str').values) +
                list(data0.question1.astype('str').values) +
                list(data0.question2.astype('str').values))

#将输入的文本转换成单词库中的索引
if training:
    x1 = tk.texts_to_sequences(data0.question1.values)
else:
    x1 = tk.texts_to_sequences(data.question1.values)

'''
将一系列文本索引转换成一个矩阵，每一行是一个样本(也就是一个question)，每个样本最多包含40个单词。
每个question裁剪到了40个单词。这就是输入。
Transform a list of num_samples sequences (lists of scalars) into a 
2D Numpy array of shape (num_samples, num_timesteps). num_timesteps 
is either the maxlen argument if provided, or the length of the longest 
sequence otherwise. Sequences that are shorter than num_timesteps are 
padded with value at the end. 
'''
x1 = sequence.pad_sequences(x1, maxlen=max_len)
if training:
    x2 = tk.texts_to_sequences(data0.question2.values.astype(str))
else:
    x2 = tk.texts_to_sequences(data.question2.values.astype(str))
x2 = sequence.pad_sequences(x2, maxlen=max_len)
#%%
'''
dictionary mapping words (str) to their rank/index (int). 
Only set after fit_on_texts was called
'''
word_index = tk.word_index

'''
Converts a class vector (integers) to binary class matrix.

E.g. for use with categorical_crossentropy.
'''
#ytrain_enc = np_utils.to_categorical(y)

embeddings_index = {}
# 第一行是单词，后面是单词的属性向量。和word2vec类似。每个单词用300维的向量表示。840B tokens
f = open('../input/glove.840B.300d.txt', encoding='utf-8')
for line in tqdm(f):
    values = line.strip().split(r' ')
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

print('Found %s word vectors.' % len(embeddings_index))

#将quora里的单词转换成GloVe矩阵
embedding_matrix = np.zeros((len(word_index) + 1, 300))
for word, i in tqdm(word_index.items()):
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

max_features = 200000
filter_length = 5
nb_filter = 64
pool_length = 4

model = Sequential()
print('Build model...')
#%% 索引矩阵转换成GloVe矩阵，至此每个单词都用一个300维的属性来描述
model1 = Sequential()
#将输入的单词索引转换成GloVe向量，每40个单词(也就是一个问题的单词量)一组，
#输出40x300的矩阵。相当于一个问题的特征。有点像图片了。就是一个转换功能，关键在于weights
#参数，按行处理输入的数据，针对一行中的每一个索引，找到它的描述向量，最后将一行所有元素的描述
#向量拼凑起来，得到一个输出矩阵。注意输出是三维的tensor，第一维相当于样本(question)索引。
#Embedding layer can only be used as the first layer in a model.
#这个转换矩阵估计很占内存
model1.add(Embedding(len(word_index) + 1,
                     300,
                     weights=[embedding_matrix],
                     input_length=40,
                     trainable=False,
                     name='md1'))
print("Embedding ok.")
'''thanks to TimeDistributed wrapper your layer could accept an input with a shape of 
(sequence_len, d1, ..., dn) by applying a layer provided to X[0,:,:,..,:], 
X[1,:,...,:], ..., X[len_of_sequence,:,...,:].'''
#结合embeding的输出，就好理解了。输入的是3维的tensor，但只有后两维是有用的，TimeDistributed
#的作用就是计算只在后两维进行。
# 第一个参数300x300的dense矩阵。
model1.add(TimeDistributed(Dense(300, activation='relu')))

#Wraps arbitrary expression as a Layer object.
#求和时候，每个question就变成了一个300维的向量
model1.add(Lambda(lambda x: K.sum(x, axis=1), output_shape=(300,)))
print("model1 ok.")
model2 = Sequential()
model2.add(Embedding(len(word_index) + 1,
                     300,
                     weights=[embedding_matrix],
                     input_length=40,
                     trainable=False,
                     name='md2'))
#第二个参数，300x300的dense矩阵
model2.add(TimeDistributed(Dense(300, activation='relu')))
model2.add(Lambda(lambda x: K.sum(x, axis=1), output_shape=(300,)))
print("model2 ok.")
model3 = Sequential()
model3.add(Embedding(len(word_index) + 1,
                     300,
                     weights=[embedding_matrix],
                     input_length=40,
                     trainable=False,
                     name='md3'))
'''This layer creates a convolution kernel that is convolved with the layer 
input over a single spatial (or temporal) dimension to produce a tensor of outputs. '''
#不懂
# 输入40x300的矩阵
# (batch_size, steps, input_dim) -> (batch_size, new_steps, filters)
model3.add(Convolution1D(nb_filter=nb_filter,
                         filter_length=filter_length,
                         border_mode='valid',
                         activation='relu',
                         subsample_length=1))
'''Dropout consists in randomly setting a fraction rate of input units to 0 
at each update during training time, which helps prevent overfitting.'''
model3.add(Dropout(0.2))

model3.add(Convolution1D(nb_filter=nb_filter,
                         filter_length=filter_length,
                         border_mode='valid',
                         activation='relu',
                         subsample_length=1))

model3.add(GlobalMaxPooling1D())
model3.add(Dropout(0.2))

model3.add(Dense(300))
model3.add(Dropout(0.2))
'''Normalize the activations of the previous layer at each batch, 
i.e. applies a transformation that maintains the mean activation 
close to 0 and the activation standard deviation close to 1.'''
#输入任意，输出和输入一致
model3.add(BatchNormalization())
print("model3 ok.")
model4 = Sequential()
model4.add(Embedding(len(word_index) + 1,
                     300,
                     weights=[embedding_matrix],
                     input_length=40,
                     trainable=False,
                     name='md4'))
model4.add(Convolution1D(nb_filter=nb_filter,
                         filter_length=filter_length,
                         border_mode='valid',
                         activation='relu',
                         subsample_length=1))
model4.add(Dropout(0.2))

model4.add(Convolution1D(nb_filter=nb_filter,
                         filter_length=filter_length,
                         border_mode='valid',
                         activation='relu',
                         subsample_length=1))

#(batch_size, steps, features) -> (batch_size, downsampled_steps, features)
model4.add(GlobalMaxPooling1D())
model4.add(Dropout(0.2))

model4.add(Dense(300))
model4.add(Dropout(0.2))
model4.add(BatchNormalization())
print("model4 ok.")
model5 = Sequential()
model5.add(Embedding(len(word_index) + 1, 300, input_length=40, dropout=0.2,name='md5'))
model5.add(LSTM(300, dropout_W=0.2, dropout_U=0.2))
print("model5 ok.")
model6 = Sequential()
model6.add(Embedding(len(word_index) + 1, 300, input_length=40, dropout=0.2,name='md6'))
#输出是300维的数据
model6.add(LSTM(300, dropout_W=0.2, dropout_U=0.2))
print("model6 ok.")
merged_model = Sequential()
'''It takes as input a list of tensors, all of the same shape expect for the 
concatenation axis, and returns a single tensor, the concatenation of all inputs.'''
merged_model.add(Merge([model1, model2, model3, model4, model5, model6], mode='concat'))
print("merge ok.")
merged_model.add(BatchNormalization())

merged_model.add(Dense(300))
merged_model.add(PReLU())
merged_model.add(Dropout(0.2))
merged_model.add(BatchNormalization())

merged_model.add(Dense(300))
merged_model.add(PReLU())
merged_model.add(Dropout(0.2))
merged_model.add(BatchNormalization())

merged_model.add(Dense(300))
merged_model.add(PReLU())
merged_model.add(Dropout(0.2))
merged_model.add(BatchNormalization())

merged_model.add(Dense(300))
merged_model.add(PReLU())
merged_model.add(Dropout(0.2))
merged_model.add(BatchNormalization())

merged_model.add(Dense(300))
merged_model.add(PReLU())
merged_model.add(Dropout(0.2))
merged_model.add(BatchNormalization())

merged_model.add(Dense(1))
merged_model.add(Activation('sigmoid'))
if not training:
    merged_model.load_weights("../temp/weights.02-0.86-0.32-0.81-0.43.hdf5")
    print("weights loaded!")
if training:
    #A metric function is similar to an loss function, except that the results 
    #from evaluating a metric are not used when training the model.
    merged_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Save the model after every epoch.
    checkpoint = ModelCheckpoint("../temp/weights.{epoch:02d}-{acc:.2f}-"
                                "{loss:.2f}-{val_acc:.2f}-{val_loss:.2f}.hdf5",
                                 monitor='val_acc', save_best_only=True, verbose=2)
 
    merged_model.fit([x1, x2, x1, x2, x1, x2], y=y, batch_size=384, nb_epoch=200,
                     verbose=1, validation_split=0.1, shuffle=True, callbacks=[checkpoint])
if not training:
    y = merged_model.predict([x1, x2, x1, x2, x1, x2], batch_size=384)
    result = pd.DataFrame({'test_id':data.test_id, 'is_duplicate':y[:,0]})
    result = result.reindex_axis(["test_id", "is_duplicate"], axis="columns")
    result.to_csv("../temp/result.csv", index=False)