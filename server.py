from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from depth import createDepthMap
from stlMaker import createMesh
import numpy as np
import io
import random
from PIL import Image
app = Flask(__name__)
CORS(app)
def img_decode(buffer):

    img = Image.open(io.BytesIO(buffer))
    img_array = np.array(img)
    # img.show()
    return img_array

def img_encode(np_img):
    img = Image.fromarray(np_img)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()

def mesh_encode(faces, vertices):
    buffer = io.BytesIO()
    np.savez_compressed(buffer, faces=faces, vertices=vertices)
    # np_mesh.save(bytes_io, mode=mesh.Mode.Binary)
    print(f'Mesh is {buffer.getbuffer().nbytes} bytes')
    return buffer.getvalue()

@app.route('/')
def home():
    return "Flask Test"

@app.route('/image2depth', methods=['POST'])
def i2d():
    if 'image' not in request.fil7es:
        return jsonify({"error": "No image provided"}), 400
    img_buffer = request.files['image'].read()
    decoded_img = img_decode(img_buffer)
    depth_map = createDepthMap(decoded_img)
    response = make_response(mesh_encode(depth_map))
    response.headers.set('Content-Type', 'image/jpeg')

    return response

@app.route('/depth2mesh', methods=['POST'])
def d2m():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    img_buffer = request.files['image'].read()
    decoded_img = img_decode(img_buffer)
    print(decoded_img.shape)
    # depth_map = np.dot(decoded_img[...,:3], [0.2989, 0.5870, 0.1140])
    # print(depth_map.shape)
    faces, vertices = createMesh(decoded_img)
    mesh_buffer = mesh_encode(faces, vertices)
    response = make_response(mesh_buffer)
    response.headers.set('Content-Type', 'application/octect-stream')

    return response

@app.route('/image2mesh', methods=['POST'])
def i2m():
    print(request.headers)
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    img_buffer = request.files['image'].read()
    decoded_img = img_decode(img_buffer)
    depth_map = createDepthMap(decoded_img)
    faces, vertices = createMesh(depth_map)
    
    return jsonify({"faces": faces.tolist(), "vertices": vertices.tolist()})
    # mesh_buffer = mesh_encode(faces, vertices)
    # response = make_response(mesh_buffer)
    # response.headers.set('Content-Type', 'application/octect-stream')

    return response

@app.route('/meshtest', methods=['POST'])
def meshTest():
    depth_map = np.array([
        [random.randint(1,254),random.randint(1,254),random.randint(1,254)],
        [random.randint(1,254),random.randint(1,254),random.randint(1,254)],
        [random.randint(1,254),random.randint(1,254),random.randint(1,254)]])
    faces, vertices = createMesh(depth_map)
    return jsonify({"faces": faces.tolist(), "vertices": vertices.tolist()})
    
if __name__ == '__main__':
    app.run()