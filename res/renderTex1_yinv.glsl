#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout(binding=0) uniform sampler2D tex1;

layout (location = 0) out vec4 colorOut;
void main()
{
    vec2 uv = uvIn;

    colorOut = texture(tex1, vec2(uv.x, 1.-uv.y)).rgbr;
    //colorOut = texture(tex1, vec2(uv.x, 1.-uv.y));
    colorOut.a = 1.;
}