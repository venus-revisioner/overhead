//#version 410


#if COMPILING_VS

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_antialias;
in vec2 a_position;
in vec2 a_texcoord;
out vec2 v_texcoord;

void main (void)
{
    v_texcoord = a_texcoord;
    gl_Position = u_projection * u_view * u_model * vec4(a_position, 0.0, 1.0);
}

    #else if COMPILING_FS

const float pi = 3.1415926538;
uniform sampler2D u_texture;
uniform vec2 u_tex_size;
uniform vec2 u_mouse_pos;
in vec2 v_texcoord;
out vec4 FragColor;


float mexican_hat(float x, float a) {

    float A = 2./(sqrt(3.*a) * pow(pi, 0.25));
    float m = A * (1. - pow(x/a, 2.)) * exp(-0.5 * pow(x/a, 2.));

    return m;
}


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


void main()
{
    vec4 tex = texture2D(u_texture, v_texcoord.yx);
    vec2 tc = v_texcoord;
    vec2 tc_sign = (tc * 2. - 1.);
    vec4 plot_scene = vec4(0., 0., 0., 1.);

    vec2 mouse = u_mouse_pos / u_tex_size;

    // DRAW A CIRCLE
    // float x = v_texcoord.x*2.-1.;
    // float y = v_texcoord.y*2.-1.;
    // float a0 = step(x*x+y*y,1.);
    // plot_scene = vec4(a0,a0,a0,1.);

    // DRAW A SMOOTHED CIRCLE
    //vec2 uv = v_texcoord * 2. - 1.;
    //float d = sqrt(dot(uv, uv));
    //float border_thickness = 0.1;
    //float radius = 0.5;
    //float t = 1. - smoothstep(0., border_thickness, abs(radius-d));
    //plot_scene = vec4(t, t, t, 1.);

    // DRAW A SINE FUNCTION USING TEX COORDS
//    float h = sin(tc.y * 2. * pi) * 0.5 + 0.5;

    // DRAW MEXICAN HAT
//    float hat = mexican_hat(tc_sign.y*32., 4.);
//    tc_sign.x *= 1.;
//    float h = hat;

    // JUST A RANDOM FUNCTION
//    float x = tc.y * u_tex_size.y;
    //float h = 0.4 * (0.4 * log(0.1 * x - 0.1) + 1.);

//    float h = texture2D(u_texture, vec2(0.48, tc.y)).r;
//

//    float plot_y_sca = 0.8;
//    float plot_x_sca = 0.8;
//    float plot_width = 0.02;
//


    // create a reference grid
    float grid_amt = 20.;
    float grid_f = grid(v_texcoord, grid_amt, u_tex_size);
    vec3 col_fill = vec3(1., 0.66, 0.33);

//    plot_y_sca *= (mouse.y);
////    plot_x_sca *= (mouse.x);
//    plot_width *= max(mouse.x, 0.001);

//    // make sure plot remains inside canvas y-axis
//    h *= (1.-plot_width);
//    h += (plot_width / 2.);
//    // dim_sca plot x-axis for convenience
//    tc_sign.x *= plot_x_sca;
//    tc_sign.x += ((1.-plot_x_sca) / 2.);
//    // dim_sca plot y-axis for convenience
//    h *= plot_y_sca;
//    h += ((1.-plot_y_sca) / 2.);

    // check if a point is "in" a shape: 1.0 if true, 0.0 if false
    //float p1 = step(h, v_texcoord.x);
    //float p2 = step(h, v_texcoord.x + plot_width);
    //float p3 = step(p2, p1);

    // same, but much simpler and smoother
//    float plot = abs(1. - smoothstep(0., plot_width, abs(h - (tc.x))));
    // same, but much simpler and smoother
//    float plot = abs(1. - smoothstep(0., plot_width, abs(h - (tc_sign.x))));

    // function version of converting 2d-image to 1d defining a cross section point
    float cut_point = 0.48;
    vec2 edge_pad = vec2(0.8, 0.8);
    float plot_w = 0.02;
    float plot = view_1d(u_texture, v_texcoord, cut_point, edge_pad*mouse, plot_w);

    // draw the plot on top of the blue grid
    plot_scene = vec4(mix(vec3(0., 0., grid_f), col_fill, plot), 1.0);

    FragColor = plot_scene;
}
