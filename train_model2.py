# coding= utf-8
from dataSet2 import DataSet
import math
import numpy
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
import numpy as np
from keras.callbacks import TensorBoard
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.utils import plot_model


# 建立一个基于CNN的识别模型
class Model(object):
    FILE_PATH = "/home/hq/桌面/cat_dog/Keras_CNN_image_classification-master/model2.h5"  # 模型进行存储和读取的地方

    def __init__(self):
        self.model = None

    # 读取实例化后的DataSet类作为进行训练的数据源
    def read_trainData(self, dataset):
        self.dataset = dataset

    # 建立一个CNN模型，一层卷积、一层池化、一层卷积、一层池化、抹平之后进行全链接、最后进行分类      其中flatten是将多维输入一维化的函数 dense是全连接层
    def build_model(self):
        self.model = Sequential()
        self.model.add(
            Conv2D(

                filters=32,
                kernel_size=(3, 3),
                padding='same',
                dim_ordering='tf',
                input_shape=self.dataset.X_train.shape[1:],  # 输入三维

            )
        )
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(
            MaxPooling2D(
                pool_size=(2, 2),
                strides=(2, 2),
                padding='same'
            )
        )

        self.model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='same'))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
        self.model.add(Dropout(0.15))

        self.model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='same'))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
        self.model.add(Dropout(0.15))

        self.model.add(Flatten())
        self.model.add(Dense(512))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Dense(128))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Dense(self.dataset.num_classes))
        self.model.add(BatchNormalization())
        self.model.add(Activation('softmax'))
        self.model.summary()



    # 进行模型训练的函数，具体的optimizer、loss可以进行不同选择


    def train_model(self):
        self.model.compile(
            optimizer='adadelta',  # 有很多可选的optimizer，例如RMSprop,Adagrad，你也可以试试哪个好，我个人感觉差异不大   adadelta
            loss='squared_hinge',  # 你可以选用 categorical_crossentropy  squared_hinge作为loss看看哪个好
            metrics=['accuracy'])

        self.model.fit(self.dataset.X_train, self.dataset.Y_train, epochs=10, batch_size=32)

    def evaluate_model(self):
        print('\nTesting---------------')
        loss, accuracy = self.model.evaluate(self.dataset.X_test, self.dataset.Y_test)

        print('test loss;', loss)
        print('test accuracy:', accuracy)

    def save(self, file_path=FILE_PATH):
        print('Model Saved.')
        self.model.save(file_path)

    def load(self, file_path=FILE_PATH):
        print('Model Loaded.')
        self.model = load_model(file_path)

    def predict(self, img):
        ##img = img.astype('float32')
        img = img / 255.0
        result = self.model.predict_proba(img)  # 测算一下该img属于某个label的概率
        max_index = np.argmax(result)  # 找出概率最高的

        return max_index, result[0][max_index]  # 第一个参数为概率最高的label的index,第二个参数为对应概率


if __name__ == '__main__':
    datast = DataSet('/home/hq/desktop/cat_dog/c-d-data/train')
    model = Model()
    model.read_trainData(datast)
    model.build_model()
    model.train_model()
    model.evaluate_model()
    model.save()
    # score=model.evaluate()
























