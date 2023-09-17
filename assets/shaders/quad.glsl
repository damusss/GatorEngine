#shader vertex
#version 330 core
		
layout (location = 0) in vec3 aPos;
layout(location = 1) in vec4 aCol;

uniform mat4 uProj;
uniform mat4 uView;

out vec4 fCol;
		
void main() {
	fCol = aCol;
	gl_Position = uView * uProj *  vec4(aPos, 1);
}

#shader fragment
#version 330 core

in vec4 fCol;

out vec4 color;
		
void main() {
	vec4 col = vec4(fCol);
	color = col;
}