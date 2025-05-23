from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import re
from sklearn.linear_model import LogisticRegression
import pickle

app = Flask(__name__)


df = pd.read_csv("email.csv")

df = df.drop(columns=['Email No.'])
X = df.drop(columns=['Prediction'])
y = df['Prediction']

model = LogisticRegression(max_iter=1000)
model.fit(X, y)


with open('models/logreg_model.pkl', 'wb') as f:
    pickle.dump(model, f)


vocabulary = X.columns.tolist()
with open('models/vocabulary.pkl', 'wb') as f:
    pickle.dump(vocabulary, f)



with open('models/logreg_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/vocabulary.pkl', 'rb') as f:
    vocabulary = pickle.load(f)


def preprocess_input(text):
   
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()

    features = np.zeros(len(vocabulary), dtype=int)
    word_index = {word: i for i, word in enumerate(vocabulary)}

    for w in words:
        if w in word_index:
            features[word_index[w]] += 1
    return features.reshape(1, -1)


@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = ''
    if request.method == 'POST':
        email_text = request.form['emailtext']
        features = preprocess_input(email_text)
        pred = model.predict(features)[0]
        prediction = 'Spam' if pred == 1 else 'Not Spam'

    return render_template('index.html', prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)
