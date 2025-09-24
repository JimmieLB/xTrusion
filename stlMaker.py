import numpy as np
import matplotlib.pyplot as plt
# from skimage import measure
# import cv2
from stl import mesh 
from PIL import Image


def in_range(index, list):
  return index >= 0 and index < len(list)

def createMesh(raw_data, name="cube", shrink=True, save=False, z_max=20, xy_max=200):
  verts = []
  indexes = []
  i = 0
  xy_scale = 1
  z_scale = 1
  if shrink:
    xy_data_max = max([len(raw_data), len(raw_data[0])])
    xy_scale = xy_max / xy_data_max
    xy_scale = round(xy_scale,5)
    z_data_max = np.max(raw_data)
    z_scale = z_max / z_data_max
    z_scale = round(z_scale,5)
    print("Z scale:", z_scale)

  print(raw_data.shape,  xy_scale, z_scale)
  print("Creating Vertices...")
  for y in range(len(raw_data)):
    indexes.append([])
    for x in range(len(raw_data[y])):
      verts.append([round(x * xy_scale,3 ), round(y * xy_scale,3), 0])
      verts.append([round(x * xy_scale,3 ), round(y * xy_scale,3), round(raw_data[y][x] * z_scale,3)])
      indexes[y].append(i)
      i += 2

  vertices = np.array(verts)

  # Define the triangles composing the cube

  faces = []

  print("Creating Faces...")
  for y in range(len(indexes)):
    for x in range(len(indexes[y])):
      x = len(indexes[y]) - x - 1
      y = len(indexes) - y - 1
      x_up = in_range(x + 1, indexes[y])
      y_up = in_range(y + 1, indexes)
      x_down = in_range(x - 1, indexes[y])
      y_down = in_range(y - 1, indexes)

      x_max = len(indexes[y]) - 1
      y_max = len(indexes) - 1

      #Top & Bottom
      if(x_up and y_up):
        faces.append([indexes[y][x], indexes[y+1][x], indexes[y][x+1]])
        faces.append([indexes[y][x]+1, indexes[y][x+1]+1, indexes[y+1][x]+1])
      if(x_down and y_down):
        faces.append([indexes[y][x], indexes[y-1][x], indexes[y][x-1]])
        faces.append([indexes[y][x]+1, indexes[y][x-1]+1, indexes[y-1][x]+1])

      #Front & Back
      if(x == 0 and y_up):
        faces.append([indexes[y][x], indexes[y][x]+1, indexes[y+1][x]])
        faces.append([indexes[y][x]+1, indexes[y+1][x]+1, indexes[y+1][x]])

        faces.append([indexes[y][x_max], indexes[y+1][x_max], indexes[y][x_max]+1])
        faces.append([indexes[y][x_max]+1, indexes[y+1][x_max], indexes[y+1][x_max]+1])

      #Side Faces
      if(y == 0 and x_up):
        faces.append([indexes[y][x], indexes[y][x+1], indexes[y][x]+1])
        faces.append([indexes[y][x]+1, indexes[y][x+1], indexes[y][x+1]+1])

        faces.append([indexes[y_max][x], indexes[y_max][x]+1, indexes[y_max][x+1]])
        faces.append([indexes[y_max][x]+1, indexes[y_max][x+1]+1, indexes[y_max][x+1]])



  # Create the mesh
  
  faces = np.array(faces)
  if save:
    print("Creating Mesh...")
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]

    print("Mesh Created")
    # Write the mesh to file "cube.stl"
    print("Saving Mesh...")
    cube.save(f'./output/{name}.stl')
    print("Mesh Saved")

  # return cube
  return (faces, vertices)

# if __name__ == "__main__":
#     depth = cv2.imread("./exampleout.jpg",cv2.IMREAD_GRAYSCALE)
#     createMesh(depth)