import gator.common.error as error
from OpenGL.GL import *


class VertexTypes:
    SHORT: str = "vertex_short"
    INT: str = "vertex_int"
    BYTE: str = "vertex_byte"
    FLOAT: str = "vertex_float"
    DOUBLE: str = "vertex_double"


class IndexUIntTypes:
    BYTE: str = "index_ubyte"
    SHORT: str = "index_ushort"
    INT: str = "index_uint"
    LONG: str = "index_ulong"


vertexTypesTable: dict[str, list[int, int, type]] = {
    "vertex_int": [4, GL_INT, GLint],
    "vertex_short": [2, GL_SHORT, GLshort],
    "vertex_byte": [1, GL_BYTE, GLbyte],
    "vertex_float": [4, GL_FLOAT, GLfloat],
    "vertex_double": [8, GL_DOUBLE, GLdouble],
}

indexUIntTypesTable: dict[str, list[int, int, type]] = {
    "index_ubyte": [1, GL_UNSIGNED_BYTE, GLubyte],
    "index_ushort": [2, GL_UNSIGNED_SHORT, GLushort],
    "index_uint": [4, GL_UNSIGNED_INT, GLuint],
    "index_ulong": [8, GL_UNSIGNED_INT64, GLuint64],
}


class IndexedVertexMesh:
    def __init__(self,
                 vertexCount: int,
                 vertexType: VertexTypes | str,
                 vertexAttribCounts: list[int],
                 vertexStaticDraw: bool,
                 vertexArrayData: list[float] | None,
                 indexUIntType: IndexUIntTypes | str,
                 indexArrayData: list[int]
                 ):

        self.vertexCount: int = vertexCount
        self.vertexAttribCounts: list[int] = vertexAttribCounts
        self.vertexStaticDraw: bool = vertexStaticDraw

        if vertexType not in vertexTypesTable:
            error.fatal(error.GraphicsError,
                        f"Vertex type '{vertexType}' not supported. Check VertexTypes for supported types")
        self.vtSizeBytes, self.vtGlConst, self.vtGlType = vertexTypesTable[vertexType]
        self.vertexTypeStr: str = vertexType

        if indexUIntType not in indexUIntTypesTable:
            error.fatal(error.GraphicsError,
                        f"Index uint type '{indexUIntType}' not supported. Check IndexUIntTypes for supported types")
        self.itSizeBytes, self.itGlConst, self.itGlType = indexUIntTypesTable[indexUIntType]
        self.indexUIntTypeStr: str = indexUIntType

        if vertexArrayData is not None:
            vertexArrayData = (
                self.vtGlType * len(vertexArrayData))(*vertexArrayData)

        self.vertexLen: int = sum(self.vertexAttribCounts)
        self.vertexSizeBytes: int = self.vertexLen*self.vtSizeBytes
        self.vertexArrayLen: int = self.vertexLen*self.vertexCount
        self.vertexArraySizeBytes: int = self.vertexArrayLen*self.vtSizeBytes

        self.indexArrayData: list[int] = indexArrayData
        self.indexArrayLen: int = len(self.indexArrayData)
        self.indexArraySizeBytes: int = self.indexArrayLen * self.itSizeBytes

        self.vaoID: int = glGenVertexArrays(1)
        glBindVertexArray(self.vaoID)

        self.vboID: int = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vboID)

        glBufferData(GL_ARRAY_BUFFER,
                     self.vertexArraySizeBytes,
                     vertexArrayData,
                     GL_STATIC_DRAW if self.vertexStaticDraw else GL_DYNAMIC_DRAW)

        offset = 0
        for i, attribCount in enumerate(self.vertexAttribCounts):
            glVertexAttribPointer(
                i, attribCount, self.vtGlConst, GL_FALSE, self.vertexSizeBytes, GLvoidp(offset))
            glEnableVertexAttribArray(i)
            offset += attribCount*self.vtSizeBytes

        self.iboID: int = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.iboID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indexArraySizeBytes,
                     (self.itGlType * self.indexArrayLen)(*indexArrayData), GL_STATIC_DRAW)

    def render(self, subDataArray: list[float] | None = None, subDataOffset: int = 0, indexArrayLen: int = "all"):
        glBindVertexArray(self.vaoID)

        for i in range(len(self.vertexAttribCounts)-1):
            glEnableVertexAttribArray(i)

        glBindBuffer(GL_ARRAY_BUFFER, self.vboID)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.iboID)

        if subDataArray is not None:
            glBufferSubData(GL_ARRAY_BUFFER, subDataOffset, len(
                subDataArray)*self.vtSizeBytes, (self.vtGlType * len(subDataArray))(*subDataArray))

        glDrawElements(GL_TRIANGLES, self.indexArrayLen if indexArrayLen ==
                       "all" else indexArrayLen, self.itGlConst, None)

        for i in range(len(self.vertexAttribCounts)-1):
            glDisableVertexAttribArray(i)

        glBindVertexArray(GL_NONE)
        glBindBuffer(GL_ARRAY_BUFFER, GL_NONE)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, GL_NONE)

    def destroy(self):
        glDeleteBuffers(1, [self.vboID])
        glDeleteBuffers(1, [self.iboID])
        glDeleteVertexArrays(1, [self.vaoID])
