#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout (location = 0) out vec3 posOut;
layout (location = 1) out vec2 uvOut;
layout (location = 2) out vec3 normOut;

uniform mat4 MVP;

layout(binding=0) uniform sampler2D tex1;

void main()
{
    vec4 pos = MVP * vec4(posIn, 1);
    vec3 norm = normalize( transpose(inverse(mat3(MVP))) * normIn );

    //vec3 samp = texture(tex1, vec2(uvIn.x, 1-uvIn.y)).rgb;
    //pos.xyz += norm*0.1;

    gl_Position = pos;

    posOut = pos.xyz;
    uvOut = uvIn;
    normOut = norm;
}