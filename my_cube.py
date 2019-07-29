import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.geometry import colorcube

window = app.Window(width=512, height=512, color=(1, 1, 1, 1))

# Vertex shader

vertex = """
uniform mat4   model;  
uniform mat4   view;        
uniform mat4   projection;
uniform vec4   u_color;         // Global color
attribute vec4 a_color;         // Vertex color
attribute vec3 a_position;      // Vertex position
varying vec4   v_color;         // Interpolated fragment color (out)
varying vec2   v_texcoord;      // Interpolated fragment texture coordinates (out)

void main()
{
    v_color = u_color * a_color;
    gl_Position = projection * view * model * vec4(a_position,1.0);
}
"""

fragment = """
varying vec4 v_color;         // Interpolated fragment color (in)
void main()
{
    gl_FragColor = v_color;
}
"""

# Created a buffer for the vertices

@window.event
def on_draw(dt):

    window.clear()

    # Outlined cube
    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable(gl.GL_BLEND)
    gl.glDepthMask(gl.GL_FALSE)
    cube['u_color'] = 0, 0, 0, 1
    cube.draw(gl.GL_LINES, outline)
    gl.glDepthMask(gl.GL_TRUE)

@window.event
def on_resize(width, height):
    cube['projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glPolygonOffset(1, 1)
    gl.glEnable(gl.GL_LINE_SMOOTH)

vertices = np.zeros(8, dtype = [('a_position', np.float32, 3), ('a_color', np.float32, 4)])

vertices['a_position'] = [[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1],
                   [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]
vertices['a_color']    = [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 0, 1],
                   [1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1]]

vertices = vertices.view(gloo.VertexBuffer)

outline = np.array([0,1, 1,2, 2,3, 3,0, 4,7, 7,6,
              6,5, 5,4, 0,5, 1,6, 2,7, 3,4], dtype=np.uint32)
outline = outline.view(gloo.IndexBuffer)

cube = gloo.Program(vertex, fragment)
cube.bind(vertices)

cube['model'] = np.eye(4, dtype=np.float32)
cube['view'] = glm.translation(0, 0, -5)

app.run()