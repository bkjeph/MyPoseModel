from flask import Flask, request, jsonify
import numpy as np
import math
np.warnings.filterwarnings('ignore')

app = Flask(__name__)
global model_features

# root
@app.route("/")
def index():
    """
    this is a root dir of my server
    :return: str
    """
    return "This is root!!!!"


# GET
@app.route('/users/<user>')
def hello_user(user):
    """
    this serves as a demo purpose
    :param user:
    :return: str
    """
    return "Hello %s!" % user


# POST
@app.route('/api/post_comparing_mat', methods=['POST'])
def set_comparing_mat():
    """
    predicts requested text whether it is ham or spam
    :return: json
    """
    json = request.get_json()
    model_x_array = np.fromstring(json['model_x_array'], dtype=float, sep=' ')
    model_y_array = np.fromstring(json['model_y_array'], dtype=float, sep=' ')
    global model_features
    model_features = np.vstack((model_x_array, model_y_array)).T
    print("base x array = " + " ".join(map(str,model_features[:,0])))
    print("base y array = " + " ".join(map(str,model_features[:,1])))
    return jsonify({'msg': 'SUCCESS'})

# POST
@app.route('/api/post_some_data', methods=['POST'])
def get_text_prediction():
    """
    predicts requested text whether it is ham or spam
    :return: json
    """
    json = request.get_json()
    print(json)
    input_x_array = np.fromstring(json['input_x_array'], dtype=float, sep=' ')
    input_y_array = np.fromstring(json['input_y_array'], dtype=float, sep=' ')
    input_features = np.vstack((input_x_array, input_y_array)).T
    pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
    unpad = lambda x: x[:, :-1]
    Y = pad(model_features)
    X = pad(input_features)
    A, res, rank, s = np.linalg.lstsq(X, Y)
    A[np.abs(A) < 1e-10] = 0  # set really small values to zero
    transform = lambda x: unpad(np.dot(pad(x), A))

    #Image of input pose onto model pose
    input_transform = transform(input_features)
    output_x_array = " ".join(map(str,input_transform[:,0]))
    output_y_array = " ".join(map(str,input_transform[:,1]))
    print("input_x_array = "+ json['input_x_array'])
    print("input_x_array = "+ json['input_y_array'])
    print("output_x_array = " + output_x_array)
    print("output_y_array = " + output_y_array)
    return jsonify({'output_x_array': output_x_array, 'output_y_array':output_y_array})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)