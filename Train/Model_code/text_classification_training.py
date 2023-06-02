import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from gensim.models import Word2Vec
# from using_model import WordEmbedding

# Tải mô hình Word2Vec đã được huấn luyện
word2vec_model = Word2Vec.load('../Model_files/W2V/word_embedding.model')

# Trích xuất từ điển từ vựng và ma trận embedding từ mô hình Word2Vec
word_vectors = word2vec_model.wv
embedding_matrix = word_vectors.vectors

# Tạo mô hình Keras
model = Sequential()
model.add(Embedding(input_dim=embedding_matrix.shape[0], output_dim=embedding_matrix.shape[1], 
                    weights=[embedding_matrix], trainable=False))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))

# Compile và huấn luyện mô hình
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3, batch_size=64)