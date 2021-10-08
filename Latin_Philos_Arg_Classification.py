import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import string
from string import punctuation
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
import tensorflow as tf

text_raw= pd.read_excel('text_raw.xlsx')     
fig, ax = plt.subplots(figsize=(16,4))
sns.countplot(x='topic',ax=ax,data=text_raw)
train_raw = text_raw[text_raw.topic != 'aeternitas mundi']
test_set = text_raw[text_raw.topic == 'aeternitas mundi']

"""
latin stopwords = ab, ac, ad, adhic, aliqui, aliquis, an, ante, apud, at, atque, aut, autem, cum, cur, de, deinde, dum, ego, enim, ergo, es, est, et, etiam, etsi, ex, fio, haud, hic, iam, idem, igitur, ille, in, infra, inter, interim, ipse, is, ita, magis, modo, mox, nam, ne, nec, necque, neque, nisi, non, nos, o, ob, per, possum, post, pro, quae, quam, quare, qui, quia, quicumque, quidem, quilibet, quis, quisnam, quisquam, quisque, quisquis, quo, quoniam, sed, si, sic, sive, sub, sui, sum, super, suus, tam, tamen, trans, tu, tum, ubi, vel, uel, uero
package punkt = divide text into sentences
"""
def remove_stopwords(text):
    stpword = stopwords.words('latin')
    no_punctuation = [char for char in text if char not in  
      string.punctuation]
    no_punctuation = ''.join(no_punctuation)
    return ' '.join([word for word in no_punctuation.split() if 
      word.lower() not in stpword])train_raw['data'] = train_raw['sentence'].apply(remove_stopwords)
test_set['data'] = test_set['sentence'].apply(remove_stopwords)

"""
Train data
get_dummies = convert data into 1/0 binaries
"""
train_one_hot = pd.get_dummies(train_df['annotation'])
train_df = pd.concat([train_df['data'],train_one_hot],axis=1)
y_train = train_df.drop('data',axis=1).value

#Test data
test_one_hot = pd.get_dummies(test_df['annotation'])
test_df = pd.concat([test_df['data'],test_one_hot],axis=1)

from sklearn.feature_extraction.text import CountVectorizer
#Define input
sentences_train = train_df['data'].values
sentences_test = test_df['sentence'].value
#Transform sentences into vectors
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(sentences_train)
X_test = vect.transform(sentences_test)

#Display occurrences of words
from yellowbrick.text import FreqDistVisualizer
features   = vectorizer.get_feature_names()
visualizer = FreqDistVisualizer(features=features, size=(800, 1000))
visualizer.fit(X_train)
visualizer.finalize()

# compute weight for each word
tfidf = TfidfTransformer()
X_train = tfidf.fit_transform(X_train)
X_train = X_train.toarray()

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.regularizers import l2def create_deep_model(factor, rate):
    model = Sequential()      
    model.add(Dense(units=4096,kernel_regularizer=l2(factor), 
      activation='relu')), Dropout(rate),
    model.add(Dense(units=512,kernel_regularizer=l2(factor),
      activation='relu')), Dropout(rate),
    model.add(Dense(units=512,kernel_regularizer=l2(factor),
      activation='relu')), Dropout(rate),
    #Output layer
    model.add(Dense(units=3, activation='softmax'))
    return model

# example = model with factor 0.0001
model= create_deep_model(factor=0.0001, rate=0.2)
model.summary()

# avoid overfitting
early_stop = EarlyStopping(monitor='val_loss', mode='min',   
  verbose=1, patience=5)
opt=tf.keras.optimizers.Adam(learning_rate=learningrate)
model.compile(loss='categorical_crossentropy', optimizer=opt,   
  metrics=['accuracy']) 

# split data into training and validation
X_train_enc, X_val, y_train_enc, y_val = train_test_split(X_train, y_train, test_size=0.1, shuffle= False)

# fit the model
history=model.fit(x=X_train_enc, y=y_train_enc, batch_size=batchsize, epochs=epochs, validation_data=(X_val, y_val), verbose=1, callbacks=early_stop)

y_train= np.argmax(y_train, axis=1)
y_test= np.argmax(y_test, axis=1)

y_test=y_val
y_test=np.argmax(y_test, axis=1)
y_pred = np.argmax(model.predict(X_val), axis=-1)from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred, target_names=['No Argument', 'Argument For', 'Argument Against']))

y_test = test_df.drop('data',axis=1).values
y_test=np.argmax(y_test, axis=1)
y_pred = np.argmax(model.predict(X_test), axis=-1)