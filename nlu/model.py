
import yaml
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical  #tranformar as labels em índices


data = yaml.safe_load(open('nlu/train.yml', 'r', encoding='utf-8').read())

inputs, outputs = [], []

for command in data['commands']:
    inputs.append(command['input'].lower())
    outputs.append(f'{command["entity"]}\\{command["action"]}')

#processar texto: palavras , caracteres, bytes, sub-palavras
chars = set()

for input in inputs + outputs:
    for ch in input:
        if ch not in chars:
            chars.add(ch)

chr2idx = {}
idx2chr = {}

for i , ch in enumerate(chars):
    idx2chr[i] = ch
    chr2idx[ch] = i


max_seq = max([len(x) for x in inputs ])

print(f'Número de chars: {len(chars)}')
print(f'Maior sequência: {max_seq}')


#dataset one-hot (número de exmplos, tamanho da seq, num caracteres)
#criar dataset disperso (número de exemplos, tamanho da seq)

#input one-hot enconding
input_data = np.zeros((len(inputs), max_seq, len(chars)), dtype= 'int32')
for i, input in enumerate(inputs):
    for k, ch in enumerate(input):
        input_data[i,k, chr2idx[ch]] = 1.0

# entrada de dados / input data sparse
input_data = np.zeros((len(inputs), max_seq), dtype= 'int32')

for i, input in enumerate(inputs):
    for k, ch in enumerate(input):
        input_data[i,k] =  chr2idx[ch]

# Saída / Output
labels = set(outputs)

label2idx = {}
idx2label = {}
for k , label in enumerate(labels):
    label2idx[label] = k
    idx2label[k] = label

output_data = []

for output in outputs:
    output_data.append(label2idx[output])


output_data = to_categorical(output_data ,len(output_data))

print(output_data[0])

model = Sequential()
model.add(Embedding(len(chars), 64))
model.add(LSTM(128, return_sequences=True))
model.add(Dense(len(output_data), activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])


#trinando o modelo
model.fit(input_data, output_data, epochs=16)


# print(inputs)
# print(outputs)




