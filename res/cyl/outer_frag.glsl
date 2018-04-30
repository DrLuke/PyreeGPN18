#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

uniform sampler2D tex1;

layout (location = 0) out vec4 colorOut;
void main()
{
    vec2 uv = uvIn * vec2(3, 1);
    vec4 samp = texture(tex1, uv);
    float mask = clamp(samp.r + samp.g + samp.b, 0., 1.);
    //colorOut = vec4(199./255., 11./255., 13./255., 1.);
    //colorOut -= vec4(texture(tex1, uv).rgb, 0.)*1.;
    colorOut = vec4(vec3(199./255. - (0.7-uv.y)*0.3, 11./255. + (1.-uv.y)*0.1, 13./255.)*0.4, mask);
}