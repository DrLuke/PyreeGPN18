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

mat2 rot2(float a) {
	return mat2(cos(a), -sin(a), sin(a), cos(a));
}


void main()
{
    vec2 uv = uvIn * vec2(3. * round(rand1*4 + 1), 1 * round(rand1*4 + 1));
    #define MODVAL 0.2
    //uv.y = mod(uv.y-0.5 + MODVAL/2, MODVAL)+0.5-MODVAL/2;
    vec4 samp = texture(tex1, rot2(rand1 * 0. * 3.1415 * 2. + beat * 0.0 * (round(rand1*2 - 1)))*(uv - vec2(0, 0.5)));
    float mask = clamp(samp.r + samp.g + samp.b, 0., 1.);

    //colorOut = vec4(vec3(199./255., 11./255. + uv.y, 13./255.)*0.8, mask);
    colorOut.rgba = texture(tex1, uv).rgba;
    //colorOut.a = 1;

    colorOut.rgb = rot3(vec3(1,1,1), time * 0.1 + round(beat)) * colorOut.rgb * 0.4;

    //colorOut = texture(tex1, vec2(uv.x, 1.-uv.y)).rgbr;
    //colorOut.a = 1.;
}