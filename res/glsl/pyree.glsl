#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout(binding=0) uniform sampler2D tex1;

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

vec4 range(vec3 p, vec2 uv)
{

    // Sphere with Radius
    vec3 spherepos = vec3(0.0, 0.0, 0.);
    float radius = 0.3;

    //p.x += sin(time*1.0) * max(0.0, p.z/200.0-3.0);

    p = mod(p + vec3(0.5,0.5,0.5), vec3(1.0,1.0,1.0)) - vec3(0.5,0.5,0.5);
    spherepos = mod(spherepos + vec3(0.5,0.5,0.5), vec3(1.0,1.0,1.0)) - vec3(0.5,0.5,0.5);

    vec3 diff = p - spherepos;

    vec3 normal = normalize(diff);


    return vec4(normal, length(diff)-radius);
}


vec4 march(vec2 uv, vec3 cam)
{
    vec3 n = normalize(vec3(sin(uv.x*3.1415),sin(uv.y*3.1415) ,cos(uv.x*3.1415)*cos(uv.y*3.1415)));



    float len = 1.0;
    vec4 ret;

    for(int i = 0; i < MARCHLIMIT; i++)
    {
        ret = range(camPos + len*n, uv)*0.5;
		len += ret.w;
    }

	return vec4(ret.xyz, len);
}


vec4 mainImage(vec2 uvIn)
{
	vec2 uv = uvIn - 0.5;

	uv = cpow(uv, round(sin(beat*3.1415)*1) + 4);
	//uv /= cpow(uv,6)*50;
	uv *= (10 + jerk*100);

    uv = rot2(sin(time) * 2.) * uv;
	uv = rot2(sin(time) * length(uv )*1.05) * uv;

    uv.x *= iResolution.x / iResolution.y;

    camPos = vec3(0.5, 0.5, -time*1.0 - beat*0.9);

    ld = vec3(sin(time), 0.0, cos(time));

    vec4 rangeret = march(uv*1.0, camPos);
    float d = log(rangeret.w / 1.0 + 1.0);
    vec3 normal = rangeret.xyz;
    vec3 n = normalize(up*uv.x + right*uv.y + ld);
    vec3 p = camPos + n*d;
    float angle = acos(dot(normal, n)/length(normal)*length(n));

	return vec4(hsv2rgb_smooth(
	vec3(atan(uv.y, uv.x) * 0.2 +  length(uv)*0.1 + beat*0.01 + d*0.1 + time*0.01 + angle/10.0,
	mod(tan(atan(uv.y, uv.x) + length(cpow(uv, -1))*0), 1.),
	max(1.0 - log(d),0.0))),1.0);
}


void main()
{
    vec2 uv = uvIn;

    //colorOut = texture(tex1, vec2(uv.x, 1.-uv.y)).rgbr;

    colorOut.rgb = mainImage(uv).rgb;
    colorOut.a = 1.;

    colorOut.rgb = rot3(vec3(1,1,1), time * 0.1 + -beat) * colorOut.rbg;
}