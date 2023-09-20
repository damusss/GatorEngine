#shader vertex
#version 330 core

layout (location = 0) in vec4 aPos;
layout (location = 1) in vec4 aCol;

uniform mat4 uProj;
uniform mat4 uView;

out vec4 fCol;

void main() {
	fCol = aCol;
	gl_Position = uView * uProj * aPos;
}

#shader fragment
#version 330 core

in vec4 fCol;

uniform float uTime;

out vec4 color;

void main() {
	color = fCol * vec4(sin(uTime)/2,1,1,1);
	if (color.a == 0.0)
		discard;
}