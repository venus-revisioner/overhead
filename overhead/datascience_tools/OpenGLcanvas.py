import threading
import time

import numpy as np
from vispy import app
from vispy import gloo
from vispy.util.transforms import ortho

VERT_SHADER = """
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;

attribute vec2 a_position;
attribute vec2 a_texcoord;

varying vec2 v_texcoord;

// Main
void main (void)
{
	v_texcoord = a_texcoord;
	gl_Position = u_projection * u_view * u_model * vec4(a_position,0.0,1.0);
}
"""

FRAG_SHADER = """
uniform sampler2D u_texture;
varying vec2 v_texcoord;
void main()
{
	gl_FragColor = texture2D(u_texture, v_texcoord);
	gl_FragColor.a = 1.0;
}
"""


class OpenGLcanvas(app.Canvas):
	"""
	Usage:
		# Create a canvas
		opengl_display = Canvas(canvas_size=(1024, 1024), tex_size=(1024, 1024), position=(2500, 10))

		# Update the texture and process events, this will update the canvas immediately
		opengl_display.update_texture(your_texture_as_np_array, immediate=True)

		The texture is updated in the main thread, so it is safe to use this function in a separate thread.
	"""
	
	def __init__(self, keys='interactive', canvas_size=(320, 200), tex_size=(32, 40), position=(1600, 1),
				 decorate=False):
		self.decorate = decorate
		app.Canvas(decorate=self.decorate)
		super().__init__(keys=keys, size=canvas_size, position=position, decorate=self.decorate)
		self.shaders = {"vert": VERT_SHADER, "frag": FRAG_SHADER}
		self.canvas_size = canvas_size
		self.tex_size = tex_size
		self.stop_flag = 0
		self.img_array = np.random.uniform(0, 1, (*self.tex_size, 3)).astype(np.float32)
		
		# A simple texture quad
		self.data = np.zeros(4, dtype=[('a_position', np.float32, 2), ('a_texcoord', np.float32, 2)])
		self.data['a_position'] = np.array(
				[[0, 0], [self.tex_size[0], 0], [0, self.tex_size[1]], [self.tex_size[0], self.tex_size[1]]])
		self.data['a_texcoord'] = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
		
		self.program = gloo.Program(self.shaders['vert'], self.shaders['frag'])
		self.texture = gloo.Texture2D(self.img_array, interpolation='nearest')
		
		self.program['u_texture'] = self.texture
		self.program.bind(gloo.VertexBuffer(self.data))
		
		self.view = np.eye(4, dtype=np.float32)
		self.model = np.eye(4, dtype=np.float32)
		self.projection = np.eye(4, dtype=np.float32)
		
		self.program['u_model'] = self.model
		self.program['u_view'] = self.view
		self.projection = ortho(0, self.tex_size[0], 0, self.tex_size[1], -1, 1)
		self.program['u_projection'] = self.projection
		
		gloo.set_clear_color('black')
		
		self.resize_screen = 0
		self.true_canvas_size = self.canvas_size
		
		self.zoom_amt = 1.0
		self.key_name = ""
		self.delta = 1.0
		
		self.mouse_press = 0
		self.mouse_pos, self.mouse_pos_init = (0, 0), (0, 0)
		self.mouse_pos_mem = self.mouse_pos_init
		
		self.show()
		# self.app.is_interactive = True
		self._timer = app.Timer('auto', connect=self.update, start=True)
		self.timer = 0
		self.timer_toggle = 0
	
	# super.__call__(app.run())
	# self._timer.stop()
	
	def on_timer(self, event):
		# self.timer += 1.
		self.timer = self._timer.iter_count
	
	def on_resize(self, event):
		width, height = event.physical_size
		gloo.set_viewport(0, 0, width, height)
		self.projection = ortho(0, width, 0, height, -100, 100)
		self.program['u_projection'] = self.projection
		
		# Compute thje new size of the quad
		r = width / float(height)
		R = self.tex_size[0] / float(self.tex_size[1])
		if r < R:
			w, h = width, width / R
			x, y = 0, int((height - h) / 2)
		else:
			w, h = height * R, height
			x, y = int((width - w) / 2), 0
		self.data['a_position'] = np.array([[x, y], [x + w, y], [x, y + h], [x + w, y + h]])
		self.program.bind(gloo.VertexBuffer(self.data))
	
	def on_key_press(self, event):
		print(event.key.name)
		self.key_name = event.key.name
		# self.program['show_components'] = event.key.name
		if event.key.name == "z":
			self.program['u_zoom'] = self.zoom_amt
			self.mouse_pos = self.mouse_pos_init
			self.program['u_mouse_pos'] = self.mouse_pos
			self.program['show_components'] = event.key.name
		
		if event.key.name in "+, -":
			scalar = 1.125 if event.key.name == "+" else 0.875
			temp = int(self.canvas_size[0])
			temp *= scalar
			canvas.size = (temp, temp)
			print("#" + "-" * 32)
			print("New canvas size:", self.canvas_size)
			print("#" + "-" * 32)
		
		if event.key.name in "Space":
			if self._timer.running:
				self.timer_toggle = 0
				self._timer.stop()
				print("*** Rendering pause ***")
			else:
				self._timer.start()
				self.timer_toggle = 1
		
		if event.key.name in ('Escape', 'q', 'Q'):
			self.stop_flag = 1
			self.close()
			print("*** Rendering stopped ***")
			self.app.quit()
	
	def on_mouse_press(self, event):
		if event:
			self.mouse_press = 1
			print("mouse press:", self.mouse_press)
	
	def on_mouse_release(self, event):
		if event:
			self.mouse_press = 0
			print("mouse press:", self.mouse_press)
	
	def on_mouse_wheel(self, event):
		self.delta = sum(event.delta)
		print("delta:", self.delta)
		# if event.delta[1] > 0:
		# 	value += event.delta[1]
		# if event.delta[0] < 0:
		# 	value += event.delta[0]
		# self.translate -= event.delta[1]
		# self.zoom_amt -= event.delta[1] * 0.05
		# print(self.zoom_amt)
		# self.program['u_zoom'] = self.zoom_amt
		# self.program['u_view'] = self.view
		self.update()
	
	# self.delta = 1.0
	# return event.delta
	
	def on_draw(self, event):
		gloo.clear(color=True, depth=True)
		self.texture.set_data(self.img_array)
		self.program.draw('triangle_strip')
	
	def update_texture(self, tex=None, immediate=False):
		if isinstance(tex, np.ndarray):
			self.img_array = tex.astype(np.float32)
		elif tex == 'sin':
			tex = np.sin(np.linspace(0, 2 * np.pi, self.tex_size[0])).astype(np.float32)
			tex = np.tile(tex, (self.tex_size[1], 1)).T
			self.img_array = np.dstack((tex, tex, tex))
		elif tex is None:
			self.img_array = np.random.uniform(0, 1, (*self.tex_size, 3)).astype(np.float32)
		
		if immediate:
			self.img_array = tex
			self.app.process_events()
			self.update()


class RunGL(threading.Thread):
	def __init__(self, glc, img=None):
		self.glc = glc
		self.img = img
		self.key_name = self.glc.key_name
		self.stop_flag = 0
		
		threading.Thread.__init__(self)  # call init of parent class
	
	def update_image(self, img):
		self.img = img  # should this reflect in the run method if called after the thread has started?
		self.glc.update_texture(self.img, immediate=True)
	
	def stop(self):
		self.stop_flag = 1
		self.glc.stop_flag = 1
		self.glc.close()
		self.glc.app.quit()
	
	# self.isAlive = False # this is a hack to stop the thread
	
	def run(self):
		# how to run this without constant polling? can you use yield? without sleep?
		self.key_name = self.glc.key_name
		while True:
			if self.img is not None:
				self.update_image(self.img)
			if self.glc.stop_flag == 1:
				self.stop_flag = 1
				break
			time.sleep(0.1)
		self.stop()


class GLPlotWidget:
	def __init__(self, img=None):
		self.app = app.Application()
		self.glc = GLCanvas(self.app, img=img)
		self.glc.show()
		self.app.process_events()
		self.app.run()
	
	def update_image(self, img):
		self.glc.update_texture(img, immediate=True)
	
	def stop(self):
		self.glc.stop()
		self.glc = None
		self.app.quit()
		self.app = None
	
	def run(self):
		self.app.run()
		self.stop()
	
	def run_threaded(self):
		self.thread = RunGL(self.glc)
		self.thread.start()
		return self.thread
	
	def update_threaded(self, img):
		self.thread.update_image(img)
	
	def stop_threaded(self):
		self.thread.stop()
		self.thread = None