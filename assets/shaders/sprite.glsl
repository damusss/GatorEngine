#shader vertex
#version 330 core

layout (location = 0) in vec4 aPos;
layout (location = 1) in vec4 aCol;
layout (location = 2) in vec2 aTexCoords;
layout (location = 3) in int aTexID;

uniform mat4 uProj;
uniform mat4 uView;

out vec2 fTexCoords;
out vec4 fCol;
flat out int fTexID;

void main() {
	fTexCoords = aTexCoords;
	fCol = aCol;
	fTexID = aTexID;
	gl_Position = uView * uProj * aPos;
}

#shader fragment
#version 330 core

in vec2 fTexCoords;
in vec4 fCol;
flat in int fTexID;

uniform sampler2D uTextures[8];

out vec4 color;

void main() {
	if (fTexID > -1) {
        color = fCol * texture(uTextures[int(fTexID)], fTexCoords);
    } else {
        color = fCol;
    }
	if (color.a == 0.0)
		discard;
}