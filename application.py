from flask import Flask, jsonify, request
import traceback
from azhu_email_classifier import AzhuEmailClassifier

app = Flask("app")
instance = AzhuEmailClassifier()


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    try:
        json = request.get_json()
        print("-- will predict, incoming json: '" + str(json) + "'")
        # temp=list(["0",json["content"]])
        temp=json["content"]
        print("-- will predict, original input: '" + str(temp) + "'")
        prediction = instance.predict(temp)
        print("-- prediction result is: '" + prediction + "'")
        return jsonify({'prediction': str(prediction[0])})
    except:
        print("-- ERROR occurred")
        return jsonify({'trace': traceback.format_exc()})


if __name__ == '__main__':
    app.run(debug=True)