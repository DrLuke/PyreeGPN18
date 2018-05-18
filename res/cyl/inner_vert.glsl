#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout (location = 0) out vec3 posOut;
layout (location = 1) out vec2 uvOut;
layout (location = 2) out vec3 normOut;

uniform mat4 MVP;

layout(binding=0) uniform sampler2D tex1;
layout(binding=1) uniform sampler2D tex2;

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

mat2 rot2(float a) {
	return mat2(cos(a), -sin(a), sin(a), cos(a));
}

void main()
{
    vec3 pos = (MVP * vec4(posIn, 1)).xyz;

    //pos.xy += (texture(tex2, uvIn).xy - vec2(0.5)) * jerk * 0.4;

    float toggle = (rand1 * 2 - 1.);
    pos.xz *= rot2(pos.y*rand2*10. + time*toggle);

    vec3 norm = normalize( transpose(inverse(mat3(MVP))) * normIn );

    vec2 uv = uvIn;

    //pos.xy *= tan(uv.y*3.1415*0.5);

    vec3 samp = texture(tex2, vec2(uvIn.x*3., uvIn.y + beat)).rgb;
    float l = length(samp)*0.6*jerk;
    pos += norm*l*l*l * clamp(tan(snare + uv.x * 3.1415*2.*4.), 0., 1.) * 1.;

    //pos -= norm * abs(sin(uv.y + time));
    //pos += norm*jerk*-0.4;

    //pos.y += cos(uv.x * 3.1415 * 2. * 3 + beat*3.1415*0.5) * jerk * 0.2;

    gl_Position = vec4(pos, 1);

    posOut = pos;
    uvOut = uvIn;
    normOut = normIn;
}