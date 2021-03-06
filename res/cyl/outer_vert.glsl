#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout (location = 0) out vec3 posOut;
layout (location = 1) out vec2 uvOut;
layout (location = 2) out vec3 normOut;

uniform mat4 MVP;

layout(binding=1) uniform sampler2D tex2;

uniform float time;
uniform float beat;
uniform float jerk;


uniform float rand2;
uniform float rand3;

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


void main()
{
    vec3 pos = posIn;


    vec2 uv = uvIn;
    pos.xy *= rot2(uv.y*10*rand2);
    pos.xy = cpow(pos.xy, 2)*0.2;
    vec3 norm = normalize( transpose(inverse(mat3(MVP))) * normIn );
    //pos.z += ((texture(tex2, uvIn).rgb - vec3(0.5)) * 6.5 * jerk * jerk * jerk * jerk).z;

    pos.xy -= (norm * (sin(uv.y) + sin(uv.y) * 0.1)).xy;


    float fac = sin(uv.y * 10 + time * 10) * 1;
    fac *= fac;

    pos.xy += ((texture(tex2, uvIn - vec2(rand3)).rgb - vec3(0.5)) * 6.5 * jerk * jerk).xy * 0.08 * fac;

    //pos -= norm / abs(tan((uv.x * uv.y)*3.1415*2. + time));

    gl_Position = MVP * vec4(pos, 1);
    posOut = (MVP * vec4(pos, 1)).xyz;
    uvOut = uvIn;
    normOut = normIn;
}