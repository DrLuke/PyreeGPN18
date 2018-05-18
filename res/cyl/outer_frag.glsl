#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout(binding=0) uniform sampler2D tex1;
layout(binding=1) uniform sampler2D tex2;

layout (location = 0) out vec4 colorOut;

uniform float time;
uniform float beat;
uniform float jerk;
uniform float snare;

uniform float rand1;
uniform float rand2;

mat3 rot3(vec3 axis, float angle)
{
    axis = normalize(axis);
    float s = sin(angle);
    float c = cos(angle);
    float oc = 1.0 - c;

    return mat3(oc * axis.x * axis.x + c,           oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,
                oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,
                oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c          );
}


void main()
{
    vec2 uv = uvIn * vec2(3, 1);
    vec4 samp = texture(tex1, uv);
    float mask = clamp(samp.r + samp.g + samp.b, 0., 1.);
    //colorOut = vec4(199./255., 11./255., 13./255., 1.);
    //colorOut -= vec4(texture(tex1, uv).rgb, 0.)*1.;
    colorOut = vec4(vec3(199./255. - (0.7-uv.y)*0.3, 11./255. + (1.-uv.y)*0.1, 13./255.)*0.4, mask);

    colorOut.rgb = rot3(vec3(1,1,1), time * 0.11 + round(beat)*0.1 + rand1 * 10 + rand2 * 10) * colorOut.rgb;

    //colorOut.rgb = normalize(colorOut.rgb);
}