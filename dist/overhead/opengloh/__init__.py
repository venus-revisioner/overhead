

def cut(in_string, start, end):
	start = str (start)
	end = str (end)
	strip = ""
	for line in in_string.splitlines ():
		if start:
			m = line.find (start)
			if m >= 0:
				strip = in_string.split (start)[1]
			if end:
				m = strip.find (end)
				if m >= 0:
					strip = strip.split (end)[0]
		else:
			m = line.find (end)
			if m >= 0:
				strip = in_string.split (end)[0]
	return strip.strip ()



def file_to_string(filename, verbose=0):
	file_data = ""
	with open(filename, buffering=0) as f1:
		for line in lines:
			lines = f1.readlines()
		# for line in f1.split():
			a = line.strip()
			# if a != "" and a.startswith(("//", "\n")) is False:
			file_data += a + "\n"

	# if verbose: print(file_data)
	return file_data


def slice_glsl(in_file=None, start="#if COMPILING_VS", end="#else if COMPILING_FS"):
	"""Outputs tuple: VERTEX and FRAGMENT shader code"""
	version = ""
	# version = "#version 120"
	# version = "#version 410"
	# vert_source = version + "\n" + cut(SOURCE, start, end)
	vert_source = version + "\n" + cut(SOURCE, start, end)
	frag_source = cut(SOURCE, end, "")
	return vert_source, frag_source


SOURCE = """


#version 120

#if COMPILING_VS


attribute vec2 a_position;
attribute vec2 a_texcoord;
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_size;
varying vec2 v_texcoord;

void main (void)
{
    v_texcoord = a_texcoord;
    gl_Position = u_projection * u_view * u_model * vec4(a_position,0.0,1.0);
}

    #else if COMPILING_FS

uniform sampler2D u_texture;
varying vec2 v_texcoord;
uniform vec2 u_tex_size;
uniform vec2 u_mouse_pos;
uniform float u_zoom;

vec2 zoom_wheel(vec2 coord, vec2 mouse_pos, float zoom) {
    return (((coord*2.-1.)*(zoom))+vec2(mouse_pos.y,1-mouse_pos.x)) * 2.;
}

void main() {
    vec2 mouse = u_mouse_pos / u_tex_size;
    vec2 zoom_coord = zoom_wheel(v_texcoord, mouse, u_zoom);
    zoom_coord *= 0.25;
    zoom_coord += 0.25;

//    vec4 out_image = texture2D(u_texture, v_texcoord);
    vec4 out_image = texture2D(u_texture, zoom_coord);
    gl_FragColor = vec4(out_image.rgb, 1.0);
}


"""