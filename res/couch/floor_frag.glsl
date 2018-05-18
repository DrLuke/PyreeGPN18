#version 450 core
layout (location = 0) in vec3 posIn;
layout (location = 1) in vec2 uvIn;
layout (location = 2) in vec3 normIn;

layout(binding=0) uniform sampler2D tex1;
layout(binding=1) uniform sampler2D tex2;

layout (location = 0) out vec4 colorOut;

uniform float time;

vec3 pal( in float t, in vec3 a, in vec3 b, in vec3 c, in vec3 d )
{
    return a + b*cos( 6.28318*(c*t+d) );
}

void main()
{
    vec3 lightdir = vec3(0., 1., -0.4);
    float diff = max(dot(normIn, lightdir), 0.0);
    float amb = 0.2;
    float light = amb + diff;

    vec2 uv = uvIn * vec2(1., 1);
    vec4 samp = texture(tex1, uv);
    float mask = clamp(samp.r + samp.g + samp.b, 0., 1.);

    float v = 0.;
    v += sin(uv.x*100. + time*0.1);
    v += sin(uv.y*100. + time*0.096);
    v += sin(uv.y*uv.x*100. + time*0.92);
    v += sin(cos(uv.y*10. + time) + time * uv.y * 0.03);
    v += sin(10.*(10.*uv.x*sin(time/20.) + uv.y * 10. * cos(time/30.)) + time*0.1);
    vec2 c = (uv+vec2(0.5))*vec2(sin(time/50.), cos(time/34));
    v += sin(cos(uv.y*sin(time + uv.x) + time) + time * uv.y * 0.06);
    v = clamp(abs(v), 0., 1.);

    //v= 0.6;

    //colorOut = vec4(vec3(199./255., 11./255. + uv.y, 13./255.)*0.8, mask);
    colorOut.rgb = pal(.8-v*1., vec3(0.5),vec3(0.55),vec3(0.45),vec3(0.00,0.10,0.20) + 0.47)*0.5;
    colorOut.rgb += pal(v*0.01 + 0.4, vec3(0.5),vec3(0.55),vec3(0.45),vec3(0.00,0.10,0.20) + 0.47);
    colorOut.rgb = colorOut.rgb*colorOut.rgb;
    //colorOut.b = 1.;
    //colorOut = texture(tex1, vec2(uv.x, 1.-uv.y)).rgbr * light;
    colorOut.a = 1.;
    //colorOut.rgb = vec3(uv, 0.);
}