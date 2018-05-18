#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout(binding=0) uniform sampler2D tex1;
layout(binding=1) uniform sampler2D tex2;

layout (location = 0) out vec4 colorOut;

uniform float beat;
uniform float jerk;
uniform float time;

uniform float rand1;
uniform float rand2;
uniform float rand3;
uniform float rand4;
uniform float rand5;
uniform float rand6;

uniform float pad0;
uniform float pad1;
uniform float pad2;
uniform float pad3;
uniform float pad4;
uniform float pad5;
uniform float pad6;
uniform float pad7;

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

float discretize(float a, float s)
{
    return round(a*s)/s;
}
vec2 discretize(vec2 a, float s)
{
    return round(a*s)/s;
}
vec3 discretize(vec3 a, float s)
{
    return round(a*s)/s;
}
vec4 discretize(vec4 a, float s)
{
    return round(a*s)/s;
}

mat2 rot2(float a) {
	return mat2(cos(a), -sin(a), sin(a), cos(a));
}

void main()
{
    vec2 uv = uvIn * vec2(1., 1);
    //uv.x *= 1080/1920;
    uv -= 0.5;
    //uv *= 1 + (rand1*rand2*rand3*100);

    uv.x *= sin(uv.x*10 * jerk) * 0.01 + 1;

    float tanrot2 = dot(rot2(pad3/255*3.14159*2. + sin(time*0.1 + jerk*0.05) * 10) * vec2(1,0), uv) ;
    uv.yx *= rot2(length(uv)*sin(time*0.1)*10) * sin(tanrot2);

    float tanrot = dot(rot2(pad3/255*3.14159*2.) * vec2(1,0), uv);

    uv.x += mix(sin(uv.y*10. * pad1 / 255. + time*0.2*round(pad1 / 255.)), tan(tan(tanrot*105.8*(pad1 / 255.) + time*1.*round(pad1 / 255.))), pad2/255.);
    uv *= rot2(time*0.1 + rand3);


    //uv = cpow(uv, (pad5/20)+0.01);
    uv = cpow(uv, pow(10, pad5/40 - 2));
    uv *= pow(10, -((pad4/255.) * 5 - 3));
    uv.y -= time*1.1 + jerk*1.;

    uv.x = tan(uv.y);
    //uv.y = sin(uv.x);

    vec4 samp = texture(tex1, uv);
    float mask = clamp(samp.r + samp.g + samp.b, 0., 1.);

    //colorOut = vec4(vec3(199./255., 11./255. + uv.y, 13./255.)*0.8, mask);

    colorOut = texture(tex1, vec2(uv.x, 1.-uv.y)).rgbr;

    colorOut.rgb *= (1 + jerk*jerk*jerk * 2. * pad0 / 100.);
    colorOut.r *= (1 + jerk*jerk*jerk * 1.5 * pad0 / 100.);

    colorOut.a = 1.;
    //colorOut.rgb = vec3(uv, 0.);


    colorOut.rgb *= rot3(vec3(rand1 - 0.5, rand2 - 0.5, rand3 - 0.5), length(uv + vec2(0.5))*3);
    //colorOut.rgb = sqrt(colorOut.rgb);
    //colorOut.rgb = sqrt(colorOut.rgb);
    //colorOut.rgb = sqrt(colorOut.rgb);
    colorOut.rgb *= colorOut.rgb * colorOut.rgb;
    //colorOut.rgb = normalize(colorOut.rgb);

    colorOut.rgb *= 1./(length(vec2(dFdx(uv.x), dFdy(uv.y)))*10);
    colorOut.rgb *= 0.0001;

    colorOut += texture(tex2,

    //rot2(time*0.1 * rand4)*(uvIn+0.5)*3
    cpow(rot2(time*0.01 + rand6*10) * uvIn * (rand5 * 0.5 + 0.9) + rand2*1,
    rand4*2 + pow(10, pad6/30 - 2))

    ) * 0.999;

    colorOut.rgb += (pad7/50) * sin(time*80) * 10;// * colorOut.rgb;

    //colorOut.rgb = clamp(colorOut.rgb, 0, 1);
}