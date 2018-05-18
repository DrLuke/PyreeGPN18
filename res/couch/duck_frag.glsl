#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout(binding=0) uniform sampler2D tex1;
layout(binding=1) uniform sampler2D tex2;

layout (location = 0) out vec4 colorOut;


void main()
{
    vec3 lightdir = vec3(0., 1., -0.4);
    float diff = max(dot(normIn, lightdir), 0.0);
    float amb = 0.2;
    float light = amb + diff;

    vec2 uv = uvIn * vec2(1., 1);
    vec4 samp = texture(tex1, uv);
    float mask = clamp(samp.r + samp.g + samp.b, 0., 1.);

    //colorOut = vec4(vec3(199./255., 11./255. + uv.y, 13./255.)*0.8, mask);
    colorOut.rgb = normIn;
    colorOut = texture(tex1, vec2(uv.x, 1.-uv.y)).rgbr * light;
    colorOut.a = 1.;
    //colorOut.rgb = vec3(uv, 0.);
}