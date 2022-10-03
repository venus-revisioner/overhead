import time
import numpy as np

from PIL import Image
from screeninfo import get_monitors

from vispy import app
from vispy import gloo
from vispy.util.transforms import ortho

from overhead.opengloh import slice_glsl
from overhead.toolboxoh import FileManager, ImageProcess, ColorizeText
from overhead.toolboxoh import print_boxed


def maximize_canvas(res, native):
    res = np.array(res[:2])
    native = np.array(native)
    return res * (1 / np.max(res / native))


class ShowImage:
    def __init__(self, img_path=None, folder=None, sideways=1, upside_down=1, instant=0, ext_filter='.jpg',
                 file_manager: FileManager = None):
        self.image_out_np = None
        self.image_out_shape = None
        self.sideways = sideways
        self.upside_down = upside_down

        self.folder = folder
        self.ext_filter = ext_filter
        self.file = None
        self.file_path = None

        self.canvas = Canvas(canvas_size=(512, 512), tex_size=(512, 512), canvas_sca=1.)
        self.canvas.show(False)
        self.color = ColorizeText()
        self.file_manager = FileManager(folder=folder)
        self.file_manager.get_folder_files(folder, ext_filter)
        self.img_process = ImageProcess()

        self.img_path = img_path
        if img_path:
            self.load_image()
            if instant:
                self.show()

    def slideshow(self, idx=0, poll_rate=0, automate=0):
        self.canvas.show(True)

        if automate:
            poll_rate = 2

        if poll_rate:
            while True:
                self.canvas.key_name = None

                if automate == 1:
                    self.update_file_manager(index=idx)

                self.canvas.app.process_events()
                time.sleep(poll_rate)

                if self.canvas.key_name is not None and automate == 0:
                    self.update_file_manager()  # left or right arrow to browse the image dict
                    print("Key:", self.canvas.key_name)

                # if self.canvas.key_name == "Up":
                #     self.file_manager.move_file(self.file_path, 'BEST')
                #     self.file_manager.get_files()
                #     print(len(self.file_manager.file_dict))
                if self.canvas._closed:
                    print("EXIT")
                    break

                idx += 1
        else:
            self.canvas.app.run()

    def next_slide(self, idx):
        self.canvas.show(True)
        self.canvas._timer.start()
        self.update_file_manager(index=idx)

    # self.canvas.app.process_events()
    # self.canvas._timer.stop()

    def show(self):
        self.canvas.show(True)
        canvas = Canvas(canvas_size=self.img_np_shape, tex_size=self.img_np_shape, canvas_sca=1.)
        canvas.rgb_inject = self.image_out_np
        canvas.app.run()

    def show_image(self, img_path):
        self.canvas.show(True)
        self.canvas._timer.start()
        tex = self.img_process.load_image_to_array(img_path, normalize=1, rotate=-1)
        self.canvas.tex_size = tex.shape
        # self.canvas.size = maximize_canvas(tex.shape, (1600,1600))
        self.canvas.maximize_canvas(self.canvas.tex_size)
        self.canvas.rgb_inject = tex
        self.canvas.app.process_events()
        # time.sleep(5)
        self.canvas._timer.stop()

    def update_file_manager(self, index=None):
        if self.canvas.key_name == 'Left':
            self.file = self.file_manager.previous_file
        elif self.canvas.key_name == 'Right':
            self.file = self.file_manager.next_file
        if index is not None:
            self.file_manager.idx = index
            self.file = self.file_manager.get_file(self.file_manager.idx)
        self.file_path = self.file_manager.folder + self.file
        file_str = self.color.colorize(self.file, fore='light blue')
        tex = self.img_process.load_image_to_array(self.file_path, normalize=1, rotate=-1)

        print(f'- {self.file_manager.idx}: {tex.shape[:2]}\n{self.file_manager.folder + file_str}')

        print("-" * 65)
        self.canvas.rgb_inject = tex

    def load_image(self, img_path=None, upside_down=None):
        if not img_path:
            img_path = self.img_path
        if not upside_down:
            upside_down = self.upside_down
        img = Image.open(img_path)
        img_np = np.array(img, dtype=np.float32)
        img_np /= 255.0
        if img_np.shape[2] > 3:
            img_np = img_np[:, :, 0:3]
        if img_np.shape[1] >= img_np.shape[0]:
            img_np = np.swapaxes(img_np, 1, 0)
        if upside_down:
            img_np = np.fliplr(img_np)
        self.image_out_np = img_np
        self.img_np_shape = img_np.shape[:2]
        print("Original shape:", img_np.shape)


class Canvas(app.Canvas):
    def __init__(self, canvas_size=(512, 512), tex_size=(512, 512), canvas_sca=1.0, canvas_pos=None, glsl='basic_shader_old.glsl'):

        screen_info = get_monitors()[0]
        self.display_max_resolution = screen_info.width, screen_info.height
        canvas_size = maximize_canvas(canvas_size, self.display_max_resolution)
        self.canvas_sca = canvas_sca
        self.canvas_size = int(canvas_size[0] * self.canvas_sca), int(canvas_size[1] * self.canvas_sca)

        self.tex_size = tex_size
        if canvas_pos is not None:
            self.canvas_pos = canvas_pos
            if isinstance(self.canvas_pos[0], float):
                self.canvas_pos = int(self.display_max_resolution[0] * canvas_pos[0]), int(
                    self.display_max_resolution[1] * canvas_pos[1])

        else:
            self.canvas_pos = self.display_max_resolution[0] - self.canvas_size[0] - 1, 1
        self.stop_flag = 0
        
        self._closed = False
        self.glsl = glsl
        
        app.Canvas.__init__(self, keys='interactive', size=self.canvas_size, position=self.canvas_pos, decorate=False)

        self.hw = self.tex_size
        print("Canvas:", self.canvas_size)
        print("Texture:", self.tex_size)
        print()
        self.data = np.zeros(4, dtype=[('a_position', np.float32, 2), ('a_texcoord', np.float32, 2)])

        self.data['a_position'] = np.array([[0, 0], [self.hw[0], 0], [0, self.hw[1]], [self.hw[0], self.hw[1]]])

        self.data['a_texcoord'] = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        self.rgb_array = np.array((self.hw[0], self.hw[1], 3))
        self.rgb_array = np.random.uniform(0, 1, (self.hw[0], self.hw[1], 3)).astype(np.float32)

        self.rgb_inject = np.zeros((self.hw[0], self.hw[1], 3)).astype(np.float32)
        try:
            self.shader_path = self.glsl
            self.VERT_SHADER, self.FRAG_SHADER = slice_glsl(self.shader_path)
            self.program = gloo.Program(self.VERT_SHADER, self.FRAG_SHADER)
        except Exception as e:
            print(e)
        finally:
            # self.shader_path = f"{Path(os.getcwd())}/shaders/opengloh/shaders/basic_shader_old.glsl)"
            self.shader_path = self.glsl
            self.VERT_SHADER, self.FRAG_SHADER = slice_glsl(self.shader_path)
            self.program = gloo.Program(self.VERT_SHADER, self.FRAG_SHADER)
        self.texture = gloo.Texture2D(self.rgb_array, interpolation='linear', wrapping='repeat')

        self.program['u_texture'] = self.texture
        self.program.bind(gloo.VertexBuffer(self.data))
        self.view = np.eye(4, dtype=np.float32)
        self.model = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)
        self.program['u_model'] = self.model
        self.program['u_view'] = self.view
        self.projection = ortho(0, self.hw[0], 0, self.hw[1], -1, 1)
        self.program['u_projection'] = self.projection
        gloo.set_clear_color('white')
        
        self.img_array1 = np.random.uniform(0, 1, (W, H, 3)).astype(np.float32)
        self.img_array2 = np.random.uniform(0, 1, (W, H, 3)).astype(np.float32)
        self.img_array3 = np.random.uniform(0, 1, (W, H, 3)).astype(np.float32)
        self.img_array4 = np.random.uniform(0, 1, (W, H, 3)).astype(np.float32)
        
        self.texture1 = gloo.Texture2D(self.img_array1, interpolation='linear', wrapping='repeat')
        self.program['u_texture1'] = self.texture1
        self.texture2 = gloo.Texture2D(self.img_array2, interpolation='linear', wrapping='repeat')
        self.program['u_texture2'] = self.texture2
        self.texture3 = gloo.Texture2D(self.img_array3, interpolation='linear', wrapping='repeat')
        self.program['u_texture3'] = self.texture3
        self.texture4 = gloo.Texture2D(self.img_array4, interpolation='linear', wrapping='repeat')
        self.program['u_texture4'] = self.texture4
        
        self.theta = 0
        self.phi = 0
        self.mouse_press = 0
        self.true_canvas_size = np.array(self.canvas_size)
        self.resize_screen = 0
        self.mouse_pos_init = np.array([self.tex_size[0] / 2, self.tex_size[1] / 2])
        self.mouse_pos = self.mouse_pos_init
        self.program['u_tex_size'] = self.tex_size
        self.program['u_mouse_pos'] = self.mouse_pos
        self.zoom_amt = 1.0
        self.program['u_zoom'] = self.zoom_amt
        self.key_name = ""
        self.mouse_pos = self.mouse_pos_init
        self.mouse_pos_mem = self.mouse_pos_init
        self.mouse_press = 0
        self.mouse_wheel = 0.0
        self.mouse_wheel_delta = [0, 0.0]
        self.key_name = None
        self.show_fps = 0
        self._timer = app.Timer('auto', connect=self.update, start=True)
        self.timer = 0
        self.timer_toggle = 0
        self.timer_verbose = 0
        self.temp = 0
        self.show()
        self.get_stream_name()

    # ------------------------

    def re_init(self, canvas_size, tex_size):
        self.__init__(canvas_size, tex_size)
        app.Canvas.__init__(self, keys='interactive', size=self.canvas_size, position=self.canvas_pos, decorate=False)

    def maximize_canvas(self, res):
        res = np.array(res[:2])
        native = np.array(self.display_max_resolution)
        max_size = res * (1 / np.max(res / native))
        self.size = max_size
        return max_size

    def injection(self, tex):
        self.rgb_inject = tex
        self.app.process_events()

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)
        self.projection = ortho(0, width, 0, height, -100, 100)
        self.program['u_projection'] = self.projection

        self.position = (self.display_max_resolution[0] - self.size[0] - 2, 1)

        self.hw = self.tex_size
        # Compute the new size of the quad
        r = width / float(height)
        R = self.hw[0] / float(self.hw[1])
        if r < R:
            w, h = width, width / R
            x, y = 0, int((height - h) / 2)
        else:
            w, h = height * R, height
            x, y = int((width - w) / 2), 0
        self.data['a_position'] = np.array(
            [[x, y], [x + w, y], [x, y + h], [x + w, y + h]])
        self.program.bind(gloo.VertexBuffer(self.data))

    def on_timer(self, event):
        # self.timer += 1.
        self.timer = self._timer.iter_count
        if self.timer > 1.:
            self.show()
        # print(self.timer)
        if self.timer_verbose:
            print(self.timer)

    # --- """Keyboard Controls"""
    def on_key_press(self, event):
	
	    print(event.key.name)
	    self.key_name = event.key.name
	    # self.program['show_components'] = event.key.name
	    if event.key.name in "1, 2, 3, 4, 5, 6, 7, 8, 9, 0":
		    self.zoom_amt = 1
		    if event.key.name not in "3, 4, 5, 6, 7, 8, 9, 0":
			    self.program['u_zoom'] = self.zoom_amt
		    self.mouse_pos = self.mouse_pos_init
		    self.program['u_mouse_pos'] = self.mouse_pos
		    self.program['show_components'] = event.key.name

	    if event.key.name == "F":
		    self.show_fps = not self.show_fps
		    self.program['show_fps'] = self.show_fps
		    
	    if event.key.name == "T":
		    self.timer_verbose = not self.timer_verbose
		    self.program['timer_verbose'] = self.timer_verbose
	 
	    if event.key.name == "R":
		    self.re_init(self.canvas_size, self.tex_size)
		    self.program['u_tex_size'] = self.tex_size
		    self.program['u_mouse_pos'] = self.mouse_pos
		    self.program['u_zoom'] = self.zoom_amt
		    self.program['show_components'] = event.key.name
		    self.program['show_fps'] = self.show_fps
		    self.program['timer_verbose'] = self.timer_verbose
		    self.program['u_tex_size'] = self.tex_size
		    self.program['u_mouse_pos'] = self.mouse_pos
		    self.program['u_zoom'] = self.zoom_amt
		    self.program['show_components'] = event.key.name
		    self.program['show_fps'] = self.show_fps
		    self.program['timer_verbose'] = self.timer_verbose

        try:
            self.key_name = event.key.name
            if event.key.name in "+, -":
                scalar = 1.05 if event.key.name == "+" else 1 / 1.05
                self.size = round(self.size[0] * scalar), round(self.size[1] * scalar)
                self.tex_size = round(self.tex_size[0] * scalar), round(self.tex_size[1] * scalar)

                print(f"New canvas size: {self.size}")
                print(f"New texture size: {self.tex_size}")
            if event.key.name in "Space":
                if self._timer.running:
                    self._timer.stop()
                    print_boxed("Rendering pause")
                else:
                    self._timer.start()
        except:
            print("Key error...")

    # -----------------------------

    # --- """Mouse Controls"""
    def on_mouse_move(self, event):
        if self.mouse_press:
            # print(event.pos, "mouse_move")
            # self.mouse_pos = self.mouse_pos * 0.2 + (
            #         np.subtract(((event.pos / self.true_canvas_size) * np.array(self.tex_size)),
            #                     self.mouse_pos_mem) * 0.6)
            self.mouse_pos = (self.mouse_pos / np.array(self.tex_size)) * self.canvas_size
            self.program['u_mouse_pos'] = self.mouse_pos
            # print(self.mouse_pos)
            self.update()
        # self.mouse_pos_mem = ((self.mouse_pos / self.true_canvas_size) * np.array(self.tex_size))
        # print("mem", self.mouse_pos_mem)
        if not self.mouse_press:
            self.mouse_pos_mem = ((self.mouse_pos / self.true_canvas_size) * np.array(self.tex_size))
        # print("mem", self.mouse_pos_mem)

    def on_mouse_press(self, event):
        if event:
            self.mouse_press = 1
            print("mouse press:", self.mouse_press)

    def on_mouse_release(self, event):
        if event:
            self.mouse_press = 0
            print("mouse press:", self.mouse_press)

    def on_mouse_wheel(self, event):
        # self.translate -= event.delta[1]
        self.zoom_amt -= event.delta[1] * 0.05
        print(self.zoom_amt)
        self.program['u_zoom'] = self.zoom_amt
        # self.program['u_view'] = self.view
        self.update()

    # _____________________________

    def on_draw(self, event):
        gloo.clear(color=True, depth=True)

        if self.timer_toggle:
            self.on_timer(event)

        self.update_texture()
	
        self.program.draw('triangle_strip')

        if self.show_fps:
            self.measure_fps(window=2)

        if self.stop_flag:
            self._timer.stop()
            self.app.quit()

    def update_texture(self, tex=None, use_astype=None):
        # if tex is not None:
        #     tex = self.rgb_inject.astype(np.float32)
        # print(type(self.rgb_inject))
        # self.rgb_array[...] = self.rgb_inject.astype(np.float32)
        # self.rgb_array = self.rgb_inject.astype(np.float64)
        
        if self.rgb_inject is not np.ndarray:
        self.rgb_array = self.rgb_inject.astype(np.float32)
			self.texture1.set_data(self.self.rgb_array)
        else:
	        self.rgb_array_inject = self.rgb_inject
	        
	        self.img_array1 = self.rgb_array_inject[0].astype(np.float32)
	        self.texture1.set_data(self.img_array1)

	        self.img_array2 = self.rgb_array_inject[1].astype(np.float32)
            self.texture2.set_data(self.img_array2)

            self.img_array3 = self.rgb_array_inject[2].astype(np.float32)
            self.texture3.set_data(self.img_array3)
			
			self.img_array4 = self.rgb_array_inject[3].astype(np.float32)
    		self.texture4.set_data(self.img_array4)
    

    # if tex is not None:
    #     self.rgb_array = tex
    # else:
    #     self.rgb_array = self.rgb_inject
    # if use_astype:
    #     self.rgb_array = self.rgb_inject.astype(np.float32)

    def get_stream_name(self):
        print_boxed(self.__str__())

    def quit(self):
        self._timer.stop()
        self.app.quit()


