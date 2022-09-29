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
