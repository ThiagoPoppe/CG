import glfw

import OpenGL.GL.shaders as gl_shaders

from sys import argv
from time import time
from struct import unpack
from OpenGL.GLU import gluPerspective

from OpenGL.GL import *

# Definindo uma lista com as normais precalculadas
normals = [
    [ -0.525731,  0.000000,  0.850651], 
    [ -0.442863,  0.238856,  0.864188], 
    [ -0.295242,  0.000000,  0.955423], 
    [ -0.309017,  0.500000,  0.809017], 
    [ -0.162460,  0.262866,  0.951056], 
    [  0.000000,  0.000000,  1.000000], 
    [  0.000000,  0.850651,  0.525731], 
    [ -0.147621,  0.716567,  0.681718], 
    [  0.147621,  0.716567,  0.681718], 
    [  0.000000,  0.525731,  0.850651], 
    [  0.309017,  0.500000,  0.809017], 
    [  0.525731,  0.000000,  0.850651], 
    [  0.295242,  0.000000,  0.955423], 
    [  0.442863,  0.238856,  0.864188], 
    [  0.162460,  0.262866,  0.951056], 
    [ -0.681718,  0.147621,  0.716567], 
    [ -0.809017,  0.309017,  0.500000], 
    [ -0.587785,  0.425325,  0.688191], 
    [ -0.850651,  0.525731,  0.000000], 
    [ -0.864188,  0.442863,  0.238856], 
    [ -0.716567,  0.681718,  0.147621], 
    [ -0.688191,  0.587785,  0.425325], 
    [ -0.500000,  0.809017,  0.309017], 
    [ -0.238856,  0.864188,  0.442863], 
    [ -0.425325,  0.688191,  0.587785], 
    [ -0.716567,  0.681718, -0.147621], 
    [ -0.500000,  0.809017, -0.309017], 
    [ -0.525731,  0.850651,  0.000000], 
    [  0.000000,  0.850651, -0.525731], 
    [ -0.238856,  0.864188, -0.442863], 
    [  0.000000,  0.955423, -0.295242], 
    [ -0.262866,  0.951056, -0.162460], 
    [  0.000000,  1.000000,  0.000000], 
    [  0.000000,  0.955423,  0.295242], 
    [ -0.262866,  0.951056,  0.162460], 
    [  0.238856,  0.864188,  0.442863], 
    [  0.262866,  0.951056,  0.162460], 
    [  0.500000,  0.809017,  0.309017], 
    [  0.238856,  0.864188, -0.442863], 
    [  0.262866,  0.951056, -0.162460], 
    [  0.500000,  0.809017, -0.309017], 
    [  0.850651,  0.525731,  0.000000], 
    [  0.716567,  0.681718,  0.147621], 
    [  0.716567,  0.681718, -0.147621], 
    [  0.525731,  0.850651,  0.000000], 
    [  0.425325,  0.688191,  0.587785], 
    [  0.864188,  0.442863,  0.238856], 
    [  0.688191,  0.587785,  0.425325], 
    [  0.809017,  0.309017,  0.500000], 
    [  0.681718,  0.147621,  0.716567], 
    [  0.587785,  0.425325,  0.688191], 
    [  0.955423,  0.295242,  0.000000], 
    [  1.000000,  0.000000,  0.000000], 
    [  0.951056,  0.162460,  0.262866], 
    [  0.850651, -0.525731,  0.000000], 
    [  0.955423, -0.295242,  0.000000], 
    [  0.864188, -0.442863,  0.238856], 
    [  0.951056, -0.162460,  0.262866], 
    [  0.809017, -0.309017,  0.500000], 
    [  0.681718, -0.147621,  0.716567], 
    [  0.850651,  0.000000,  0.525731], 
    [  0.864188,  0.442863, -0.238856], 
    [  0.809017,  0.309017, -0.500000], 
    [  0.951056,  0.162460, -0.262866], 
    [  0.525731,  0.000000, -0.850651], 
    [  0.681718,  0.147621, -0.716567], 
    [  0.681718, -0.147621, -0.716567], 
    [  0.850651,  0.000000, -0.525731], 
    [  0.809017, -0.309017, -0.500000], 
    [  0.864188, -0.442863, -0.238856], 
    [  0.951056, -0.162460, -0.262866], 
    [  0.147621,  0.716567, -0.681718], 
    [  0.309017,  0.500000, -0.809017], 
    [  0.425325,  0.688191, -0.587785], 
    [  0.442863,  0.238856, -0.864188], 
    [  0.587785,  0.425325, -0.688191], 
    [  0.688191,  0.587785, -0.425325], 
    [ -0.147621,  0.716567, -0.681718], 
    [ -0.309017,  0.500000, -0.809017], 
    [  0.000000,  0.525731, -0.850651], 
    [ -0.525731,  0.000000, -0.850651], 
    [ -0.442863,  0.238856, -0.864188], 
    [ -0.295242,  0.000000, -0.955423], 
    [ -0.162460,  0.262866, -0.951056], 
    [  0.000000,  0.000000, -1.000000], 
    [  0.295242,  0.000000, -0.955423], 
    [  0.162460,  0.262866, -0.951056], 
    [ -0.442863, -0.238856, -0.864188], 
    [ -0.309017, -0.500000, -0.809017], 
    [ -0.162460, -0.262866, -0.951056], 
    [  0.000000, -0.850651, -0.525731], 
    [ -0.147621, -0.716567, -0.681718], 
    [  0.147621, -0.716567, -0.681718], 
    [  0.000000, -0.525731, -0.850651], 
    [  0.309017, -0.500000, -0.809017], 
    [  0.442863, -0.238856, -0.864188], 
    [  0.162460, -0.262866, -0.951056], 
    [  0.238856, -0.864188, -0.442863], 
    [  0.500000, -0.809017, -0.309017], 
    [  0.425325, -0.688191, -0.587785], 
    [  0.716567, -0.681718, -0.147621], 
    [  0.688191, -0.587785, -0.425325], 
    [  0.587785, -0.425325, -0.688191], 
    [  0.000000, -0.955423, -0.295242], 
    [  0.000000, -1.000000,  0.000000], 
    [  0.262866, -0.951056, -0.162460], 
    [  0.000000, -0.850651,  0.525731], 
    [  0.000000, -0.955423,  0.295242], 
    [  0.238856, -0.864188,  0.442863], 
    [  0.262866, -0.951056,  0.162460], 
    [  0.500000, -0.809017,  0.309017], 
    [  0.716567, -0.681718,  0.147621], 
    [  0.525731, -0.850651,  0.000000], 
    [ -0.238856, -0.864188, -0.442863], 
    [ -0.500000, -0.809017, -0.309017], 
    [ -0.262866, -0.951056, -0.162460], 
    [ -0.850651, -0.525731,  0.000000], 
    [ -0.716567, -0.681718, -0.147621], 
    [ -0.716567, -0.681718,  0.147621], 
    [ -0.525731, -0.850651,  0.000000], 
    [ -0.500000, -0.809017,  0.309017], 
    [ -0.238856, -0.864188,  0.442863], 
    [ -0.262866, -0.951056,  0.162460], 
    [ -0.864188, -0.442863,  0.238856], 
    [ -0.809017, -0.309017,  0.500000], 
    [ -0.688191, -0.587785,  0.425325], 
    [ -0.681718, -0.147621,  0.716567], 
    [ -0.442863, -0.238856,  0.864188], 
    [ -0.587785, -0.425325,  0.688191], 
    [ -0.309017, -0.500000,  0.809017], 
    [ -0.147621, -0.716567,  0.681718], 
    [ -0.425325, -0.688191,  0.587785], 
    [ -0.162460, -0.262866,  0.951056], 
    [  0.442863, -0.238856,  0.864188], 
    [  0.162460, -0.262866,  0.951056], 
    [  0.309017, -0.500000,  0.809017], 
    [  0.147621, -0.716567,  0.681718], 
    [  0.000000, -0.525731,  0.850651], 
    [  0.425325, -0.688191,  0.587785], 
    [  0.587785, -0.425325,  0.688191], 
    [  0.688191, -0.587785,  0.425325], 
    [ -0.955423,  0.295242,  0.000000], 
    [ -0.951056,  0.162460,  0.262866], 
    [ -1.000000,  0.000000,  0.000000], 
    [ -0.850651,  0.000000,  0.525731], 
    [ -0.955423, -0.295242,  0.000000], 
    [ -0.951056, -0.162460,  0.262866], 
    [ -0.864188,  0.442863, -0.238856], 
    [ -0.951056,  0.162460, -0.262866], 
    [ -0.809017,  0.309017, -0.500000], 
    [ -0.864188, -0.442863, -0.238856], 
    [ -0.951056, -0.162460, -0.262866], 
    [ -0.809017, -0.309017, -0.500000], 
    [ -0.681718,  0.147621, -0.716567], 
    [ -0.681718, -0.147621, -0.716567], 
    [ -0.850651,  0.000000, -0.525731], 
    [ -0.688191,  0.587785, -0.425325], 
    [ -0.587785,  0.425325, -0.688191], 
    [ -0.425325,  0.688191, -0.587785], 
    [ -0.425325, -0.688191, -0.587785], 
    [ -0.587785, -0.425325, -0.688191], 
    [ -0.688191, -0.587785, -0.425325]
]

# Criando o vertex_shader
vertex_shader_phong = """
#version 330 compatibility

// Iremos passar para o fragment shader as posições dos vértices e as suas normais
out vec4 position;
out vec3 normal;

void main() {
    // Computando a normal (aplicando a transposta da inversa)
    normal = normalize(gl_NormalMatrix * gl_Normal);
    
    // Computando as posições dos vértices (aplicando a matriz de ModelView)
    position = gl_ModelViewMatrix * gl_Vertex;
    
    // Aplicando a matriz de ModelView e Projection sobre o nosso vértice de entrada
    gl_Position = ftransform();
}
"""

# Criando o fragment_shader
fragment_shader_phong = """
#version 330 compatibility

// Recebemos do vertex shader os valores das posições dos vértices e as suas normais
in vec4 position;
in vec3 normal;

// Uniform para a posição da fonte luz
uniform vec3 lightPosition;

// Uniform para a cor do nosso objeto
uniform vec3 objColor;

// Váriaveis const float para guardar a contribuição especular e difusa
const float specularContrib = 0.4;
const float diffuseContrib = 1.0 - specularContrib;

// Cor de saída
out vec4 outColor;

void main() {
    // Vec3 para a posição do nosso vértice e normal
    vec3 p = vec3(gl_ModelViewMatrix * position);
    vec3 n = normalize(gl_NormalMatrix * normal);

    // Computando a direção da nossa luz
    vec3 lightDir = normalize(lightPosition - p);
    
    // Computando o R
    vec3 R = reflect(lightDir, n);
    
    // Computando o viewVec
    vec3 viewVec = normalize(-p);
    
    // Computando o componente difuso (produto escalar entre a direção da luz e a normal)
    float diffuse = max(0.0, dot(lightDir, n));
    
    // Computando o componente especular
    float spec = 0.0;
    if (diffuse > 0.0) {
        // Cosseno do ângulo entre R e viewVec (em outras palavras, produto escalar)
        spec = max(0.0, dot(R, viewVec));
        
        // Parte da fórmula do cosseno elevado a um "n"
        spec = pow(spec, 64.0);
    }

    // Calculando a intensidade da luz
    float intensity = (diffuse * diffuseContrib) + (spec * specularContrib);
    
    // Definindo uma luz de ambiente
    vec3 ambientLight = vec3(0.15, 0.1, 0.1);
    
    // Exibindo a cor
    outColor = vec4(ambientLight + objColor * intensity, 1.0);
}
"""

# Definindo a largura e altura da janela
width, height = 800, 600

# Definindo o tamanho em bytes dos tipos de dados
sizeof = {
    'int': 4, 'md2_t': 68, 'vertex_t': 4, 'frame_t': 40
}

# Definindo as 21 animações do modelo MD2 (nome: primeiro, último, fps)
animations = {
    'STAND': [0, 39, 9], 'RUN': [40,  45, 10], 'ATTACK': [46, 53, 10], 'PAIN_A': [54, 57, 7],
    'PAIN_B': [58, 61, 7], 'PAIN_C': [62, 65, 7], 'JUMP': [66, 71, 7], 'FLIP': [72, 83, 7],
    'SALUTE': [84, 94, 7], 'FALLBACK': [95, 111, 10], 'WAVE': [112, 122, 7], 'POINT': [123, 134, 6],
    'CROUCH_STAND': [135, 153, 10], 'CROUCH_WALK': [154, 159, 7], 'CROUCH_ATTACK': [160, 168, 10],
    'CROUCH_PAIN': [169, 172, 7], 'CROUCH_DEATH': [173, 177, 5], 'DEATH_FALLBACK': [178, 183, 7],
    'DEATH_FALLFORWARD': [184, 189, 7], 'DEATH_FALLBACKSLOW': [190, 197, 7], 'BOOM': [198, 198, 5]
}

class MD2Header:
    """ Classe para o header do arquivo MD2"""

    # Método construtor da classe
    def __init__(self, header):
        self.ident = header[0].decode()  # String identificadora para o tipo IDP2
        self.version = header[1]  # Versão, deve ser 8

        self.skinWidth = header[2]  # Largura da textura
        self.skinHeight = header[3]  # Altura da textura 

        self.frameSize = header[4]  # Tamanho em bytes de cada frame

        self.numSkins = header[5]  # Quantidade de texturas
        self.numVertices = header[6]  # Quantidade de vértices de cada frame
        self.numSt = header[7]  # Quantidade de coordenadas de textura
        self.numTriangles = header[8]  # Quantidade de triângulos no modelo
        self.numGLCmds = header[9]  # Quantidade de comandos da OpenGL
        self.numFrames = header[10]  # Quantidade de frames

        # ----- OFFSETS ----- #
        self.offsetSkins = header[11]  # Offset para os dados das texturas
        self.offsetSt = header[12]  # Offset para os dados das coordenadas de textura
        self.offsetTriangles = header[13]  # Offset para os dados dos triângulos
        self.offsetFrames = header[14]  # Offset para os dados dos frames
        self.offsetGLCmds = header[15]  # Offset para os dados dos comandos da OpenGL

class AnimState:
    """ Classe para o estado da animação """

    # Método construtor da classe
    def __init__(self, anim, currTime, oldTime, interpol, typeName, currFrame, nextFrame):
        self.startFrame = anim[0]
        self.endFrame = anim[1]
        self.fps = anim[2]
        self.currTime = currTime
        self.oldTime = oldTime
        self.interpol = interpol
        self.type = typeName
        self.currFrame = currFrame
        self.nextFrame = nextFrame

class Vertex:
    """ Classe para os vértices do frame """

    # Método construtor da classe
    def __init__(self, v, normalIndex):
        self.v = v
        self.normalIndex = normalIndex

class Frame:
    """ Classe para os frames do modelo """
    
    # Método construtor da classe
    def __init__(self, name, vertices):
        self.name = name
        self.vertices = vertices

class MD2Model:
    """ Classe para um modelo MD2 """

    # Método construtor da classe
    def __init__(self):
        # Escala do objeto (1.0 -> sem escala) e o id da textura
        self.scl = 1.0
        self.texId = 0

        # Iniciamos o modelo com a animação 0
        self.setAnimation('STAND')

    # Método para carregar um modelo MD2
    def loadModel(self, filename):
        # Abrindo o arquivo .md2 (arquivo binário)
        with open(filename, 'rb') as f:       
            # Lendo o header do arquivo
            data = f.read(sizeof['md2_t'])
            fmt = '4s16i'
            temp = unpack(fmt, data)
            self.header = MD2Header(temp)

            # Verificando se o arquivo possui ident = IPD2 e versão = 8
            if self.header.ident == 'IPD2' and self.header.version != 8:
                print('Bad version or identifier')
                f.close()
                return False

            # Lendo os comandos da OpenGL
            f.seek(self.header.offsetGLCmds)
            data = f.read(self.header.numGLCmds * sizeof['int'])
            fmt = self.header.numGLCmds * 'i'
            self.glcmds = unpack(fmt, data)

            # Criando uma lista para guardar os frames do modelo
            self.frames = []

            # Lendo os frames do modelo
            f.seek(self.header.offsetFrames)
            for _ in range(self.header.numFrames):
                # Lendo os campos scale, translate e name do frame
                data = f.read(sizeof['frame_t'])
                fmt = '3f3f16s'
                temp = unpack(fmt, data)
                
                # Salvando esses valores lidos
                scl = temp[0:3]
                translate = temp[3:6]
                name = temp[6:22][0]

                # Lendo os vértices do frame
                data = f.read(self.header.numVertices * sizeof['vertex_t'])
                fmt = self.header.numVertices * '3B1B'
                temp = unpack(fmt, data)

                # Construindo uma lista de vértices
                vertices = [Vertex(temp[i:i+3], temp[i+3]) for i in range(0, len(temp), 4)]
 
                # "Descomprimindo" os vértices
                for i, vertex in enumerate(vertices):
                    x = vertex.v[0] * scl[0] + translate[0]
                    y = vertex.v[1] * scl[1] + translate[1]
                    z = vertex.v[2] * scl[2] + translate[2]

                    vertices[i] = Vertex([x, y, z], vertex.normalIndex)

                # Adicionando o novo frame à lista
                frame = Frame(name, vertices)
                self.frames.append(frame)

            return True

    # Método para definir a animação do modelo
    def setAnimation(self, name):
        # Verificando se o tipo existe
        if not name in animations:
            print('Animação {} não existe'.format(name))
            return

        # Definindo a animação do modelo
        currFrame = animations[name][0]
        nextFrame = currFrame + 1
        self.animation = AnimState(animations[name], 0, 0, 0, name, currFrame, nextFrame)

    # Método para renderizar o frame do modelo
    def renderFrame(self):
        # Revertendo a orientação da face frontal
        # Usamos polygons pois os comandos da GL usam uma lista de triângulos
        # que possuem contagem no sentido horário
        glPushAttrib(GL_POLYGON_BIT)
        glFrontFace(GL_CW)

        # Habilitando backface culling
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        # Desenhando cada triângulo
        i = 0
        while i < len(self.glcmds):
            # Obtendo o comando
            cmd = self.glcmds[i]
            i += 1

            # Caso o sinal seja negativo usamos GL_TRIANGLE_FAN
            if cmd < 0:
                glBegin(GL_TRIANGLE_FAN)
                cmd *= -1

            # Caso contrário usamos GL_TRIANGLE_STRIP
            else:
                glBegin(GL_TRIANGLE_STRIP)

            # Enquanto o comdando for > 0 iremos fazer o seguinte passo
            while cmd > 0:
                # Obtendo coordenadas de textura e o índice do vértice a ser exibido
                # s = self.glcmds[i]
                # t = self.glcmds[i+1]
                idx = self.glcmds[i+2]

                # Obtendo os vértices dos frames atual e próximo
                curr_vertex = self.frames[self.animation.currFrame].vertices[idx]
                next_vertex = self.frames[self.animation.nextFrame].vertices[idx]

                # Obtendo as normais dos frames atual e próximo
                curr_normal = normals[curr_vertex.normalIndex]
                next_normal = normals[next_vertex.normalIndex]
                
                # Interpolando as normais
                x = curr_normal[0] + self.animation.interpol * (next_normal[0] - curr_normal[0])
                y = curr_normal[1] + self.animation.interpol * (next_normal[1] - curr_normal[1])
                z = curr_normal[2] + self.animation.interpol * (next_normal[2] - curr_normal[2])

                # Passando para a OpenGL a normal interpolada
                glNormal3fv([x, y, z])

                # Interpolando os vértices
                x = curr_vertex.v[0] + self.animation.interpol * (next_vertex.v[0] - curr_vertex.v[0])
                y = curr_vertex.v[1] + self.animation.interpol * (next_vertex.v[1] - curr_vertex.v[1])
                z = curr_vertex.v[2] + self.animation.interpol * (next_vertex.v[2] - curr_vertex.v[2])

                # Desenhando o vértice
                glVertex3fv([x, y, z])

                # Decrementamos o cmd e avançamos para o próximo bloco
                cmd -= 1
                i += 3

            glEnd()

        # Desabilitando o GL_CULL_FACE
        glDisable(GL_CULL_FACE)
        glPopAttrib()

    # Método para animar o modelo
    def animateModel(self, time):
        # Definindo o tempo atual da animação
        self.animation.currTime = time

        # Calculando o frame atual e o próximo
        delta = self.animation.currTime - self.animation.oldTime
        if delta > (1 / self.animation.fps):
            self.animation.currFrame = self.animation.nextFrame
            self.animation.nextFrame += 1

            if self.animation.nextFrame > self.animation.endFrame:
                self.animation.nextFrame = self.animation.startFrame

            self.animation.oldTime = self.animation.currTime

        # Previnindo que os frames atuais e próximos exceda o limite de frames
        if self.animation.currFrame > self.header.numFrames - 1:
            self.animation.currFrame = 0

        if self.animation.nextFrame > self.header.numFrames - 1:
            self.animation.nextFrame = 0

        # Definindo a taxa de interpolação
        self.animation.interpol = self.animation.fps * (self.animation.currTime - self.animation.oldTime )

    # Método para desenhar o modelo
    def drawModel(self, time):
        # Se o tempo for maior que 0, animamos o modelo
        if time > 0:
            self.animateModel(time)

        glPushMatrix()
        # Rotacionando o modelo
        glRotatef(-90, 1, 0, 0)
        glRotatef(-90, 0, 0, 1)
        
        # Renderizando o modelo
        self.renderFrame()
        glPopMatrix()

# Função principal
def main():
    # Criando nosso modelo
    model = MD2Model()

    # Carregando o modelo
    if not model.loadModel(argv[1]):
        print('Não foi possível carregar o arquivo', argv[1])
        exit(1)

    # Inicializando o glfw
    if not glfw.init():
        print('Não foi possível inicializar o glfw')
        exit(1)

    # Criando uma janela
    window = glfw.create_window(width, height, 'Ogro Model', None, None)
    if not window:
        print('Não foi possível criar a janela')
        glfw.terminate()
        exit(1)

    # Definindo a posição da janela na tela
    glfw.set_window_pos(window, 30, 60)

    # Tornando a janela criada o contexto atual
    glfw.make_context_current(window)

    # Exibindo a versão da OpenGL
    print(glGetString(GL_VERSION))

    # Compilando e usando o shader
    shader = gl_shaders.compileProgram(gl_shaders.compileShader(vertex_shader_phong, GL_VERTEX_SHADER),
                                       gl_shaders.compileShader(fragment_shader_phong, GL_FRAGMENT_SHADER))
    glUseProgram(shader)

    # Definindo a cor de limpeza da tela
    glClearColor(0.2, 0.2, 0.2, 1.0)

    # Habilitando o DEPTH_TEST
    glEnable(GL_DEPTH_TEST)

    # Definindo a posição da nossa luz
    lightPositionLoc = glGetUniformLocation(shader, 'lightPosition')
    glUniform3f(lightPositionLoc, 100, -100, 0)

    # Definindo a cor do nosso objeto
    objColorLoc = glGetUniformLocation(shader, 'objColor')
    glUniform3f(objColorLoc, 0.1, 0.8, 0.1)

    # Definindo o tipo de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width/height, 0.1, 1000.0)

    # Transladando o modelo para aparecer na tela
    glTranslatef(0.0, 0.0, -100.0)

    # MAIN LOOP
    while not glfw.window_should_close(window):

        # Capturando eventos
        glfw.poll_events()

        # Limpando os buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Renderizando o modelo
        model.drawModel(time())

        # Desenhando na tela
        glfw.swap_buffers(window)

    # Terminando o glfw
    glfw.terminate()

# Chamando a função principal
if __name__ == '__main__':
    main()