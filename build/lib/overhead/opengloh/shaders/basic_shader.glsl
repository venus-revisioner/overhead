#version 410

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

uniform sampler2D u_texture;
in vec2 v_texcoord;
out vec4 FragColor;

void main()
{
    vec4 tex = texture2D(u_texture, v_texcoord);
    FragColor = tex;
}