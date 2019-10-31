import os
import keras
from keras import models
from keras import layers 
from keras.models import load_model
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def every_day_im_shuffling(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)

loc = r"C:\Users\Owen Lockwood\Box Sync\Documents\misc\HACKRPI2019\datasets\train"
directory = os.fsencode(loc)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        path = os.path.join(loc, filename)
        count = 0
        num = 0
        with open(path) as f:
            for line in f:
                temp = line.split(',')
                if count == 0 or len(temp[1][12:14]) == 0:
                    count += 1
                    continue                
                if int(temp[1][11:13]) < 17 and int(temp[1][11:13]) > 7:
                    num += 1
        SIZE = num                
        labels = np.zeros(shape=(SIZE, 3))
        data = np.zeros(shape=(SIZE))
        count = 0
        num = 0
        with open(path) as f: 
            for line in f:
                temp = line.split(',')  
                if count == 0 or len(temp[1][12:14]) == 0:
                    count += 1
                    continue
                # 43 = temp
                # 44 = precip
                # 48 = humidity
                if int(temp[1][11:13]) < 17 and int(temp[1][11:13]) > 7:
                    year = int(temp[1][0:4])
                    month = int(temp[1][5:7])
                    day = int(temp[1][8:10])
                    date = 365*(year - 2010) + 30*(month-1) + day
                    data[num] = date
                    if len(temp[43]) == 0:
                        labels[num][0] = 0
                    else: 
                        if len(temp[43]) > 2:
                            tem = temp[43][1:temp[43].find("\"", 1)]                    
                            if tem[len(tem)-1].isalpha():
                                labels[num][0] = float(tem[0:len(tem)-1])
                            else:
                                labels[num][0] = float(tem)
                        elif is_number(temp[43]):
                            labels[num][0] = float(temp[43])
                    if len(temp[44]) == 0 or temp[44].isalpha():
                        labels[num][1] = 0
                    else:
                        if temp[44][0] == "\"":
                            pre = temp[44][1:temp[44].find("\"", 1)]
                            if pre.isalpha():
                                labels[num][1] = 0
                            elif pre[len(pre)-1].isalpha():
                                labels[num][1] = float(pre[0:len(pre)-1])
                            else:
                                labels[num][1] = float(pre)
                        else:
                            if temp[44][len(temp[44]) - 1].isalpha():
                                labels[num][1] = float(temp[44][0:len(temp[44]) - 1])
                            else: 
                                labels[num][1] = float(temp[44])                
                    if len(temp[48]) == 0:
                        labels[num][2] = 0
                    else:
                        if len(temp[48]) > 2:
                            humid = temp[48][1:temp[48].find("\"", 1)]
                            if len(humid) == 0:
                                labels[num][2] = 0
                            else:
                                labels[num][2] = float(humid)
                        elif is_number(temp[48]):
                            labels[num][2] = float(temp[48])
                    count += 1
                    num += 1


        print(num)
        print(labels[0:3])
        print(data[0:3])
        '''
        mean = data.mean(axis=0)
        data -= mean
        std = data.std(axis=0)
        data /= std
        '''
        every_day_im_shuffling(labels, data)
        print(data[0:3])
        partial_train = data[:int(3*SIZE/4)]
        partial_label = labels[:int(3*SIZE/4)]
        val_data = data[int(3*SIZE/4):int(7*SIZE/8)]
        val_label = labels[int(3*SIZE/4):int(7*SIZE/8)]
        test_data = data[int(7*SIZE/8):]
        test_label = labels[int(7*SIZE/8):]
        
        print(len(labels), len(labels[0]))
        model = models.Sequential()
        model.add(layers.Dense(64, activation='relu', input_shape=(1,)))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(3))
        model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
        
        print(data.shape, labels.shape)
        history = model.fit(partial_train, partial_label, epochs=752, batch_size=128, \
                            validation_data=(val_data, val_label), verbose=0)
        mname = str(filename[0:len(filename)-4])
        mname += ".h5"
        model.save(mname)
        results = model.evaluate(test_data, test_label)
        print(results)
        future = model.predict([[3364]])
        print(str(filename))
        print(future)
        history_dict = history.history
        history_dict.keys()
        
        mae = history.history['mean_absolute_error']
        val_mae = history.history['val_mean_absolute_error']
        
        print(val_mae.index(min(val_mae)))
        keras.backend.clear_session()        
