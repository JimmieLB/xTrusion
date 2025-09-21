from flask import Flask, render_template, request, make_response, jsonify
from depth import createDepthMap
from stlMaker import createMesh
import numpy as np
from stl import mesh
import io
from PIL import Image
app = Flask(__name__)

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

def mesh_encode(np_mesh):
    bytes_io = io.BytesIO()
    np_mesh.save(bytes_io, mode=mesh.Mode.Binary)
    bytes_io.seek(0)
    return bytes_io.getvalue()

@app.route('/')
def home():
    return "Flask Test"

@app.route('/img2depth', methods=['POST'])
def i2d():
    if 'image' not in request.files:
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
    mesh_bytes_io = createMesh(decoded_img)
    response = make_response(mesh_bytes_io)
    response.headers.set('Content-Type', 'application/octect-stream')

    return response


if __name__ == '__main__':
    app.run()