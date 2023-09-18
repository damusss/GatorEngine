#shader vertex
#version 330 core

layout (location = 0) in vec4 aPos;
layout (location = 1) in vec4 aCol;
layout (location = 2) in vec2 aTexCoords;
layout (location = 3) in int aTexID;
layout (location = 4) in int aEntityID;

uniform mat4 uProj;
uniform mat4 uView;

out vec2 fTexCoords;
out vec4 fCol;
flat out int fTexID;
flat out int fEntityID;

void main() {
	fTexCoords = aTexCoords;
	fCol = aCol;
    fTexID = aTexID;
	fEntityID = aEntityID;
	gl_Position = uView * uProj * aPos;
}

#shader fragment
#version 330 core

in vec2 fTexCoords;
in vec4 fCol;
flat in int fTexID;
flat in int fEntityID;

uniform sampler2D uTextures[8];

out vec3 color;

void main() {
	vec4 col = fCol;
	if (fTexID > -1) {
        col = fCol * texture(uTextures[int(fTexID)], fTexCoords);
    }

	if (col.a == 0.0)
		discard;

    color = vec3(fEntityID, fEntityID, fEntityID);
}