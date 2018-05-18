#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout (location = 0) out vec3 posOut;
layout (location = 1) out vec2 uvOut;
layout (location = 2) out vec3 normOut;

uniform mat4 MVP;

layout(binding=0) uniform sampler2D tex1;

uniform float time;
uniform vec2 indx;

uniform float beat;
uniform float jerk;

uniform float snare;


vec2 cexp(vec2 z)
{
    return exp(z.x) * vec2(cos(z.y), sin(z.y));
}

vec2 clog(vec2 z)
{
    return vec2(log(length(z)), atan(z.y, z.x));
}

vec2 cpow(vec2 z, float p)
{
    return cexp(clog(z) * p);
}

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
    vec3 wPos = posIn;

    wPos.y += sin(time*10 + length(indx))*5;

    //wPos.xz *= rot2(wPos.y * jerk);

    wPos.y += cos(length(indx)*1. - time - beat * 3.1415 * 2.)*2. + 0.5;
    wPos.y += tan(time*1 + length(indx) * 3.);

    wPos.y += smoothstep(15., 18., wPos.y) * wPos.y * wPos.y;

    //wPos.xyz *= rot3(vec3(0, 1, 0), beat);

    vec4 pos = MVP * vec4(wPos, 1);
    vec3 norm = normalize( transpose(inverse(mat3(MVP))) * normIn );

    vec3 samp = texture(tex1, vec2(uvIn.x, 1-uvIn.y)).rgb;
    //pos.xyz += norm*clamp(sin(snare * 3.14159), 0., 1.)*0.2;




    gl_Position = pos;

    posOut = pos.xyz;
    uvOut = uvIn;
    normOut = norm;
}