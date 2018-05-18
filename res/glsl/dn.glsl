#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout(binding=0) uniform sampler2D tex1;
layout(binding=0) uniform sampler2D tex2;

layout (location = 0) out vec4 colorOut;

uniform float time;

const vec2 iResolution = vec2(1920, 1080);

uniform float beat;
uniform float jerk;
uniform float snare;

uniform float rand1;
uniform float rand2;
uniform float rand3;

 #define MARCHLIMIT 128

vec3 camPos = vec3(0.0, 0.0, -1.0);
vec3 ld = vec3(0.0, 0.0, 1.0);
vec3 up = vec3(0.0, 1.0, 0.0);
vec3 right = vec3(1.0, 0.0, 0.0);
vec3 lightpos = vec3(1.5, 1.5, 1.5);

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

// Smooth HSV to RGB conversion
vec3 hsv2rgb_smooth( in vec3 c )
{
    vec3 rgb = clamp( abs(mod(c.x*6.0+vec3(0.0,4.0,2.0),6.0)-3.0)-1.0, 0.0, 1.0 );

	rgb = rgb*rgb*(3.0-2.0*rgb); // cubic smoothing

	return c.z * mix( vec3(1.0), rgb, c.y);
}


void main()
{
    vec2 uv = uvIn;

    uv.x *= 1920/1080;

    colorOut = texture(tex, vec2(uv.x-0.01, uv.y)).rgbr;

    colorOut.a = 1.;

    colorOut.rgb *= rot3(vec3(rand1 - 0.5,rand2-0.5,rand3-0.5), time * 0.1);
}