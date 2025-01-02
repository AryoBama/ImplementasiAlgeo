import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def create_cube(center, size):
    """Membuat vertices dan edges untuk kubus"""

    x, y, z = center
    vertices = np.array([
        [x-size/2, y-size/2, z-size/2], 
        [x+size/2, y-size/2, z-size/2], 
        [x+size/2, y+size/2, z-size/2], 
        [x-size/2, y+size/2, z-size/2], 
        [x-size/2, y-size/2, z+size/2], 
        [x+size/2, y-size/2, z+size/2], 
        [x+size/2, y+size/2, z+size/2], 
        [x-size/2, y+size/2, z+size/2]  
    ])
    
   
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]], 
        [vertices[4], vertices[5], vertices[6], vertices[7]], 
        [vertices[0], vertices[1], vertices[5], vertices[4]], 
        [vertices[2], vertices[3], vertices[7], vertices[6]], 
        [vertices[1], vertices[2], vertices[6], vertices[5]], 
        [vertices[0], vertices[3], vertices[7], vertices[4]]  
    ]
    
    return vertices, faces

def calculate_shadow_point(light_source, point, floor_height=0):

    direction = point - light_source
    
    t = (floor_height - light_source[2]) / direction[2]
    
    shadow_point = light_source + t * direction
    shadow_point[2] = floor_height  
    
    return shadow_point

def plot_cube_and_shadow(cube_center=[0, 0, 2], cube_size=2, light_source=[4, 4, 6]):

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Buat kubus
    vertices, faces = create_cube(cube_center, cube_size)
    
    cube = Poly3DCollection(faces, alpha=0.25)
    cube.set_facecolor('blue')
    ax.add_collection3d(cube)
    
    shadow_vertices = []
    light_source = np.array(light_source)
    
    print("\nPosisi vertex kubus dan bayangannya:")
    print("=====================================")
    vertex_names = ['Depan-Kiri-Bawah', 'Depan-Kanan-Bawah', 'Belakang-Kanan-Bawah', 
                   'Belakang-Kiri-Bawah', 'Depan-Kiri-Atas', 'Depan-Kanan-Atas',
                   'Belakang-Kanan-Atas', 'Belakang-Kiri-Atas']
    
    for i, vertex in enumerate(vertices):
        shadow_point = calculate_shadow_point(light_source, vertex)
        shadow_vertices.append(shadow_point)
        
        # Print koordinat
        print(f"\nVertex {vertex_names[i]}:")
        print(f"  Posisi asli  : ({vertex[0]:.2f}, {vertex[1]:.2f}, {vertex[2]:.2f})")
        print(f"  Posisi bayang: ({shadow_point[0]:.2f}, {shadow_point[1]:.2f}, {shadow_point[2]:.2f})")
        
        ax.plot([light_source[0], vertex[0]], 
                [light_source[1], vertex[1]], 
                [light_source[2], vertex[2]], 
                'r--', alpha=0.3)
    
    shadow_vertices = np.array(shadow_vertices)
    
    print(f"\nPosisi sumber cahaya: ({light_source[0]:.2f}, {light_source[1]:.2f}, {light_source[2]:.2f})")
    
    shadow_faces = [[shadow_vertices[0], shadow_vertices[1], 
                    shadow_vertices[2], shadow_vertices[3]]]
    
    shadow = Poly3DCollection(shadow_faces, alpha=0.3)
    shadow.set_facecolor('gray')
    ax.add_collection3d(shadow)
    
    ax.scatter(*light_source, color='yellow', s=100, label='Light Source')
    
    # Set batas plot
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    

    ax.view_init(elev=20, azim=45)
    
    # Set batas axis
    ax.set_xlim([-3, 6])
    ax.set_ylim([-3, 6])
    ax.set_zlim([0, 8])
    
    plt.title('Cube Shadow Projection')
    plt.legend()
    plt.show()

plot_cube_and_shadow([1.5, 0, 1.5], 1, [4,-1,6])

