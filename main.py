import trimesh
import numpy as np
import pickle

padding = 1
dx = 0.05


mesh = trimesh.load_mesh('E:/min-tang/unit-test-mesh-vol-particle-sdf-mixedCD-20231110-v0/data/my-bunny.obj')


bbox = mesh.bounding_box.bounds
#获取最小的点 box.min
#print(bbox[0])


if(padding < 1):
    padding = 1

unit = np.array([1.0,1.0,1.0],)

#加padding
min_box =np.array(bbox[0]- padding*dx*unit)
max_box =np.array(bbox[1]+ padding*dx*unit)

sizes =((max_box - min_box)//dx).astype(int)

#print(sizes)

#构造网格,逐点查询距离
sdf_points = []
distances = []
query = trimesh.proximity.ProximityQuery(mesh)

for i in range(sizes[2]):
    for j in range(sizes[1]):
        for k in range(sizes[0]):
            sdf_points=(min_box+dx*np.array([k,j,i])).reshape(1,3)
            distances.append(-query.signed_distance(sdf_points))
    print('当前进度：'+str((i+1)/sizes[2]*100)+'%')       

#保存
with open('E:/min-tang/unit-test-mesh-vol-particle-sdf-mixedCD-20231110-v0/data/bunny.txt', "wb") as sdf_file:
    sdf_file.write((str(sizes[0])+' '+str(sizes[1])+' '+str(sizes[2])+'\n').encode(encoding='utf-8'))
    sdf_file.write((str(min_box[0])+' '+str(min_box[1])+' '+str(min_box[2])+'\n').encode(encoding='utf-8'))
    sdf_file.write((str(dx)+'\n').encode(encoding='utf-8'))
    for i in range(len(distances)):
        sdf_file.write((str(distances[i][0])+'\n').encode(encoding='utf-8'))