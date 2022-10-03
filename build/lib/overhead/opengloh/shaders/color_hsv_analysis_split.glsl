#version 120

#if COMPILING_VS

// Uniforms
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_antialias;

// Attributes
attribute vec2 a_position;
attribute vec2 a_texcoord;

// Varyings
varying vec2 v_texcoord;

// Main
void main (void)
{
    v_texcoord = a_texcoord;
    gl_Position = u_projection * u_view * u_model * vec4(a_position,0.0,1.0);
}

#else if COMPILING_FS

uniform sampler2D u_texture;
uniform sampler2D u_texture2;
uniform sampler2D u_texture3;
uniform sampler2D u_texture4;

uniform float neighbourhood;
uniform int show_components;
uniform vec2 u_tex_size;
uniform vec2 u_mouse_pos;
uniform float u_zoom;

varying vec2 v_texcoord;

float hue2rgb(float p, float q, float t) {
    if (t < 0.0) t += 1.0;
    if (t > 1.0) t -= 1.0;
    if (t < 1.0 / 6.0) return p + (q - p) * 6.0 * t;
    if (t < 1.0 / 2.0) return q;
    if (t < 2.0 / 3.0) return p + (q - p) * (2.0 / 3.0 - t) * 6.0;
    return p;
}

vec4 rgb2hsl(vec4 tex) {
    float r = tex.r;
    float g = tex.g;
    float b = tex.b;
    float max = max(r, max(g, b));
    float min = min(r, min(g, b));
    float h, s, l = (max + min) / 2.0;

    if (max == min) {
        h = 0.0;
        s = 0.0;
    } else {
        float d = max - min;
        s = l > 0.5 ? d / (2.0 - max - min) : d / (max + min);
        if (max == r) {
            h = (g - b) / d + (g < b ? 6.0 : 0.0);
        } else if (max == g) {
            h = (b - r) / d + 2.0;
        } else {
            h = (r - g) / d + 4.0;
        }
        h /= 6.0;
    }
    return vec4(h, s, l, tex.a);
}

vec4 hsl2rgb(vec4 tex) {
    float h = tex.x;
    float s = tex.y;
    float l = tex.z;
    float r, g, b;

    if (s == 0.0) {
        r = l;
        g = l;
        b = l;
    } else {
        float q = l < 0.5 ? l * (1.0 + s) : l + s - l * s;
        float p = 2.0 * l - q;
        r = hue2rgb(p, q, h + 1.0 / 3.0);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1.0 / 3.0);
    }
    return vec4(r, g, b, tex.w);
}

//void main(void) {
//   vec4 tex = texture2D(u_texture, v_texcoord);
//    vec4 hsl = rgb2hsl(tex);
//    hsl.x = mod(hsl.x + u_hue, 1.0);
//    tex = hsl2rgb(hsl);
//    gl_FragColor = tex;
//}

float grid(vec2 texcoord, float grid_amt, vec2 tex_size) {
    vec2 grid = vec2(0.);
    vec2 width = (1./tex_size) * grid_amt + (1./(tex_size));

    if (mod(texcoord.x * grid_amt - width.x/2., 1.) > (1. - width.x))
    grid.x = 1.;
    if (mod(texcoord.y * grid_amt - width.y/2., 1.) > (1. - width.y))
    grid.y = 1.;

    return (grid.x + grid.y) * 0.5;
}


float view_1d(sampler2D tex, vec2 coord, float cut_point, vec2 scale, float width) {
    vec2 coord_s = coord * 2. - 1.;

    // cut point is the place, where the side-view is sampled and created
    float h = texture2D(tex, vec2(cut_point, coord.y)).r;
    float plot_y_sca = scale.y;
    float plot_x_sca = scale.x;
    float plot_width = width;

    // make sure plot remains inside canvas y-axis
    h *= (1.-plot_width);
    h += (plot_width / 2.);
    // dim_sca plot x-axis for convenience
    coord_s.x *= plot_x_sca;
    coord_s.x += ((1.-plot_x_sca) / 2.);
    // dim_sca plot y-axis for convenience
    h *= plot_y_sca;
    h += ((1.-plot_y_sca) / 2.);
    float plot = abs(1. - smoothstep(0., plot_width, abs(h - (coord.x))));
    return plot;
}

vec4 corner_crop(sampler2D tex, vec2 coord, vec2 corner, vec2 mouse) {

    vec2 m = vec2(mouse.y, 1.-mouse.x);

    m = min(vec2(1.), m);
    m = max(vec2(0.), m);

    coord *= ((m+0.5) + (coord*(0.5-m)));

    coord = min(vec2(1.),coord);
    coord = max(vec2(0.),coord);

    vec2 tc = vec2(coord.x * 2. - corner.x, coord.y * 2. - corner.y);
    if (tc.x >= 0. && tc.y >= 0. && tc.x <= 1. && tc.y <= 1.) {
        return texture2D(tex, tc);
    } else {
        return vec4(0.,0.,0.,1.);
    }
}

vec2 corner_crop_vec2(vec4 tex, vec2 coord, vec2 corner, vec2 mouse) {

    vec2 m = vec2(mouse.y, 1.-mouse.x);

    m = min(vec2(1.), m);
    m = max(vec2(0.), m);

    coord *= ((m+0.5) + (coord*(0.5-m)));

    coord = min(vec2(1.),coord);
    coord = max(vec2(0.),coord);

    vec2 tc = vec2(coord.x * 2. - corner.x, coord.y * 2. - corner.y);
    if (tc.x >= 0. && tc.y >= 0. && tc.x <= 1. && tc.y <= 1.) {
        return tc;
    } else {
        return vec2(0., 0.);
    }
}

vec4 corner_crop_vec4(vec4 tex, vec2 coord, vec2 corner, vec2 mouse) {

    vec2 m = vec2(mouse.y, 1.-mouse.x);

    m = min(vec2(1.), m);
    m = max(vec2(0.), m);

    coord *= ((m+0.5) + (coord*(0.5-m)));

    coord = min(vec2(1.),coord);
    coord = max(vec2(0.),coord);

    vec2 tc = vec2(coord.x * 2. - corner.x, coord.y * 2. - corner.y);
    if (tc.x >= 0. && tc.y >= 0. && tc.x <= 1. && tc.y <= 1.) {
        return tex;
    } else {
        return vec4(0.,0.,0.,1.);
    }
}

vec2 zoom_wheel(vec2 coord, vec2 mouse_pos, float zoom) {
    return (((coord*2.-1.)*(zoom))+vec2(mouse_pos.y,1-mouse_pos.x)) * 2.;
}

void main()
{

    vec2 mouse = u_mouse_pos / u_tex_size;

    vec2 zoom_coord = zoom_wheel(v_texcoord, mouse, u_zoom);
    zoom_coord *= 0.25;
    zoom_coord += 0.25;

    vec4 som_zoom = texture2D(u_texture, zoom_coord);
    vec4 som_full_orig = texture2D(u_texture, v_texcoord);

    if (show_components == 1) {
        gl_FragColor = som_full_orig;

    } else if (show_components == 2) {

        vec2 crop_coord = v_texcoord * 2. - 1.;

        vec4 som = texture2D(u_texture, crop_coord);
        vec4 mex_hat = texture2D(u_texture2, crop_coord);
        vec4 dist = texture2D(u_texture3, crop_coord);
        vec4 influence = texture2D(u_texture4, crop_coord);

        // down left
        vec4 dl = vec4(1.);
        dl *= corner_crop_vec4(mex_hat, v_texcoord, vec2(0.,0.), mouse);

        // up left
        vec4 ul = vec4(1.);
        ul *= corner_crop_vec4(som, v_texcoord, vec2(1.,0.), mouse);

        // down right
        vec4 dr = vec4(1.);
        dr *= corner_crop_vec4(influence, v_texcoord, vec2(0.,1.), mouse);
        dr *= corner_crop_vec4(dist, v_texcoord, vec2(0.,1.), mouse);

        // up right
        vec4 ur = vec4(1.);
        ur *= corner_crop_vec4(influence, v_texcoord, vec2(1.,1.), mouse);
        ur *= corner_crop_vec4(mex_hat, v_texcoord, vec2(1.,1.), mouse);
        ur *= corner_crop_vec4(som, v_texcoord, vec2(1.,1.), mouse);

        gl_FragColor = ul + dl + dr + ur;

    } else if (show_components == 0) {
        gl_FragColor = som_zoom;

    } else if (show_components == 3) {
        gl_FragColor = rgb2hsl(som_zoom);

    } else if (show_components == 4) {
        gl_FragColor = vec4(vec3(som_zoom.r), 1.);

    } else if (show_components == 5) {
        gl_FragColor = vec4(vec3(som_zoom.g), 1.);

    } else if (show_components == 6) {
        gl_FragColor = vec4(vec3(som_zoom.b), 1.);

    } else if (show_components == 7) {
        gl_FragColor = vec4(rgb2hsl(som_zoom).rrr, 1.);

    } else if (show_components == 8) {
        gl_FragColor = vec4(rgb2hsl(som_zoom).ggg, 1.);

    } else if (show_components == 9) {
        gl_FragColor = vec4(rgb2hsl(som_zoom).bbb, 1.);
    }
}
