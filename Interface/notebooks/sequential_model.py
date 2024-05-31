""" This notebook explores sequential model to classify hand gestures"""
import csv
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns
import pickle
import o
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

# COMMAND ----------

RANDOM_SEED = 42
script_directory = o.path.dirname(o.path.abspath(__file__))
data_folder = o.path.join(script_directory, "data_folder")

# COMMAND ----------

lb = []
t_x = [] 
t_y = [] 
for i, df in enumerate(o.listdir(data_folder)):
    with open(o.path.join(data_folder, df), 'rb') as f:
        d = pickle.load(f)
        #train path
        for h in d:
            t_y.append(i)
            t_x.append((h - h[0]).flatten())
        lb.append(df[5:-2])
t_x = np.array(t_x)
self.clf.fit(t_x, t_y)
plt.switch_backend('Agg')

# COMMAND ----------

model_save_path = 'model/sequential.hdf5'
tflite_save_path = 'model/sequential.tflite'

# COMMAND ----------

NUM_CLASSES = 4
X_train, X_test, y_train, y_test = train_test_split(t_x, t_y, train_size=0.75, random_state=RANDOM_SEED)

# COMMAND ----------

model = tf.keras.models.Sequential([
    tf.keras.layers.Input((21 * 2, )),
#     tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(20, activation='relu'),
#     tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

# COMMAND ----------
model.summary()  # tf.keras.utils.plot_model(model, show_shapes=True)
# Model checkpoint callback
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    model_save_path, save_best_only=True, monitor="val_accuracy", verbose=1, save_weights_only=False)
# Callback for early stopping
es_callback = tf.keras.callbacks.EarlyStopping(patience=40, verbose=1)

# COMMAND ----------
lr_reducer = tf.keras.callbacks.ReduceLROnPlateau(
    monitor="val_accuracy",
    factor=0.1,
    patience=20,
    verbose=1)

# COMMAND ----------
# Model compilation
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# COMMAND ----------
model.fit(
    X_train,
    y_train,
    epochs=1000,
    batch_size=256,
    validation_data=(X_test, y_test),
    callbacks=[cp_callback, es_callback, lr_reducer]
)

# COMMAND ----------

def print_confusion_matrix(y_true, y_pred, report=True):
    labels = sorted(list(set(y_true)))
    cmx_data = confusion_matrix(y_true, y_pred, labels=labels)

    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(df_cmx, annot=True, fmt='g' ,square=False)
    ax.set_ylim(len(set(y_true)), 0)
    plt.show()

    if report:
        print('Classification Report')
        print(classification_report(y_test, y_pred))

# COMMAND ----------

Y_pred = model.predict(X_test)
y_pred = np.argmax(Y_pred, axis=1)

print_confusion_matrix(y_test, y_pred)

# Save as a model dedicated to inference
model.save(model_save_path, include_optimizer=False)
# Transform model (quantization)

# COMMAND ----------

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quantized_model = converter.convert()

open(tflite_save_path, 'wb').write(tflite_quantized_model)

interpreter = tf.lite.Interpreter(model_path=tflite_save_path)
interpreter.allocate_tensors()

# Get I / O tensor
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.set_tensor(input_details[0]['index'], np.array([X_test[0]]))

# COMMAND ----------

# Commented out IPython magic to ensure Python compatibility.
# %%time
# # Inference implementation
# interpreter.invoke()
# tflite_results = interpreter.get_tensor(output_details[0]['index'])

print(np.squeeze(tflite_results))
print(np.argmax(np.squeeze(tflite_results)))