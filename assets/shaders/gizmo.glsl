#shader vertex
#version 330 core

layout (location = 0) in vec4 aPos;
layout (location = 1) in vec4 aCol;
layout (location = 2) in vec2 aTexCoord;

uniform mat4 uProj;
uniform mat4 uView;

out vec2 fTexCoord;
out vec4 fCol;

void main() {
	fTexCoord = aTexCoord;
	fCol = aCol;
	gl_Position = uView * uProj * aPos;
}

#shader fragment
#version 330 core

uniform sampler2D uTex;

in vec2 fTexCoord;
in vec4 fCol;

out vec4 color;

void main() {
	vec4 texColor = texture(uTex, fTexCoord);
	color = fCol * texColor;
	if (color.a == 0.0)
		discard;
}