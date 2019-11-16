import sys
import numpy as np

from time import time
from numpy.random import uniform as rand

# ------------- VARIÁVEIS GLOBAIS ------------- #
gravity = np.array([0.0, -0.005, 0.0])


# ------------- FUNÇÕES AUXILIARES ------------- #

# Função que retorna um vetor normalizado
def normalize(v):
    norm = np.linalg.norm(v)

    if norm == 0:
        return v
    else:
        return v / norm

# Função para refletir um raio
def reflect(v, n):
        return v - 2 * np.dot(v, n) * n

# Função que refrata um raio
def refract(v, n, factor):
    uv = normalize(v)
    dt = np.dot(uv, n)

    delta = 1 - (factor**2 * (1 - dt**2))
    if delta > 0:
        refracted = (factor * (uv - n * dt)) - (n * np.sqrt(delta))
        return [True, refracted]
    else:
        return [False, None]

# Função que implementa a equação de Schlick
def schlick(cos, ref_index):
    r0 = (1 - ref_index) / (1 + ref_index)
    r0 **= 2
    return r0 + (1 - r0) * np.power((1 - cos), 5)

# Função que retorna a cor de um pixel
def raytrace(ray_in, world, depth):
    hit, _, point, normal, material = world.hit(ray_in, 0.001, sys.float_info.max)
    if hit:
        scattered, attenuation, ray_out = material.scatter(ray_in, point, normal)
        if depth < 50 and scattered:
            return attenuation * raytrace(ray_out, world, depth + 1)
        else:
            return np.array([.0, .0, .0])

    else:
        unit_dir = normalize(ray_in.dir())
        t = 0.5 * (unit_dir[1] + 1)
        return (1 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array([0.5, 0.7, 1.0])

# Função que retorna um ponto aleatório em um disco (círculo)
def random_point_in_disk():
    r = np.sqrt(rand())
    theta = 2 * np.pi * rand()

    return np.array([r * np.cos(theta), r * np.sin(theta), .0])

# ------------- CLASSES ------------- #

class Ray:
    """
        Classe para representar um raio
    """

    # Método para inicializar um objeto Ray
    def __init__(self, origin, direction):
        self.__origin = origin
        self.__dir = direction

    # Método para retornarmos a origem do raio
    def origin(self):
        return self.__origin

    # Método para retornarmos a direção do raio
    def dir(self):
        return self.__dir

    # Método para retornamos um ponto no raio
    def point(self, t):
        return self.__origin + t * self.__dir

class Camera:
    """
        Classe para representar nossa camera
    """

    # Método para inicializar uma classe do tipo Camera
    def __init__(self, origin, look_at, vup, fov, aspect, aperture, focus_dist):
        theta = np.radians(fov)
        half_height = np.tan(theta / 2)
        half_width = aspect * half_height

        self.__w = normalize(origin - look_at)
        self.__u = normalize(np.cross(vup, self.__w))
        self.__v = np.cross(self.__w, self.__u)
        self.__len_radius = aperture / 2

        self.__origin = origin
        self.__lower_left_corner = origin - focus_dist * (self.__u * half_width + self.__v * half_height + self.__w)
        self.__horizontal = 2 * self.__u * focus_dist * half_width
        self.__vertical = 2 * self.__v * focus_dist * half_height

    # Método para retornar a posição da câmera
    def origin(self):
        return self.__origin

    # Método para dispararmos um raio
    def shoot_ray(self, s, t):
        rd = self.__len_radius * random_point_in_disk()
        offset = self.__u * rd[0] + self.__v * rd[1]

        origin = self.origin() + offset
        direction = self.__lower_left_corner + s * self.__horizontal + t * self.__vertical - self.__origin - offset
        return Ray(origin, direction)

class Material:
    """
        Classe abstrata para representar materiais
    """

    # Método abstrato para computar o comportamento o espalhamento de raios
    def scatter(self, ray):
        raise NotImplementedError

class Lambertian(Material):
    """
        Classe para representar materiais lambertianos
    """

    # Método para inicializar uma classe do tipo Lambertian
    def __init__(self, albedo):
        self.__albedo = albedo

    # Método para retornar o albedo do objeto
    def albedo(self):
        return self.__albedo

    # Método que define a função scatter
    def scatter(self, ray, point, normal):
        target = point + normal + Sphere.random_point()
        scattered = Ray(point, target - point)
        attenuation = self.albedo()

        return [True, attenuation, scattered]

class Metal(Material):
    """
        Classe para representar materiais metálicos
    """

    # Método para inicializar uma classe do tipo Metal
    def __init__(self, albedo, fuzz):
        self.__albedo = albedo

        if fuzz < 1.0:
            self.__fuzz = fuzz
        else:
            self.__fuzz = 1.0

    # Método para retornar o albedo do objeto
    def albedo(self):
        return self.__albedo

    # Método para retornar o fuzz do objeto
    def fuzz(self):
        return self.__fuzz

    # Método que define a função scatter
    def scatter(self, ray, point, normal):
        reflected = reflect(normalize(ray.dir()), normal)
        scattered = Ray(point, reflected + self.fuzz() * Sphere.random_point())
        attenuation = self.albedo()

        return [np.dot(scattered.dir(), normal) > 0, attenuation, scattered]

class Dielectric(Material):
    """
        Classe para representar materiais dielétricos
    """

    # Método para inicializar uma classe do tipo Dielectric
    def __init__(self, ref_index):
        self.__ri = ref_index

    # Método para retornar o índice de refração do objeto
    def ref_index(self):
        return self.__ri

    # Método que define a função scatter
    def scatter(self, ray, point, normal):
        reflected = reflect(ray.dir(), normal)
        attenuation = np.array([1.0, 1.0, 1.0])
        
        outward_normal = normal
        factor = 1 / self.ref_index()
        cos = -1 * np.dot(ray.dir(), normal) / np.linalg.norm(ray.dir())

        if np.dot(ray.dir(), normal) > 0:
            outward_normal = -normal
            factor = self.ref_index()
            cos = self.ref_index() * np.dot(ray.dir(), normal) / np.linalg.norm(ray.dir())

        has_refracted, refracted = refract(ray.dir(), outward_normal, factor)
        if has_refracted:
            reflect_prob = schlick(cos, self.ref_index())
        else:
            reflect_prob = 1.0

        if rand() < reflect_prob:
            scattered = Ray(point, reflected)
        else:
            scattered = Ray(point, refracted)

        return [True, attenuation, scattered]

class Hitable:
    """
        Classe abstrata para representar "hits" nos objetos da cena
    """
    
    # Método abstrato para computar um hit de um raio em um objeto
    def hit(self, ray, t_min, t_max):
        raise NotImplementedError

class Sphere(Hitable):
    """
        Classe que vai representar uma esfera
    """

    # Método para inicializar uma classe do tipo Sphere
    def __init__(self, center, radius, bounce, material):
        self.__center = center
        self.__radius = radius
        self.__material = material

        self.__bounce = bounce
        self.__init_height = center[1]
        self.__velocity = np.array([0.0, 0.05, 0.0])

    # Método para retornar a posição do centro da esfera
    def center(self):
        return self.__center

    # Método para retornar o raio da esfera
    def radius(self):
        return self.__radius

    # Método para retornar a velocidade da esfera
    def vel(self):
        return self.__velocity

    # Método para retornar o material da esfera
    def material(self):
        return self.__material

    # Método que atualiza a posição da esfera
    def update(self):
        if self.__bounce == True:
            self.__center += self.__velocity
            self.__velocity += gravity

        if self.__center[1] < self.__init_height:
            self.__velocity = np.array([0.0, 0.05, 0.0])

    # Método estático para 
    @staticmethod
    def random_point():
        r = np.sqrt(rand())
        theta = 2 * np.pi * rand()

        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = rand()

        return np.array([x, y, z])

    # Método que define a função hit
    def hit(self, ray, t_min, t_max):
        # Definindo o vetor que parte do ponto de origem do raio até o centro da esfera
        oc = ray.origin() - self.center()

        # Definindo os coeficientes do polinômio para vermos os pontos de interseção
        a = np.dot(ray.dir(), ray.dir())
        b = np.dot(oc, ray.dir())
        c = np.dot(oc, oc) - self.radius()**2

        # Computando o discriminante
        delta = b**2 - a * c
        if delta > 0:
            # Computamos a menor raiz e vemos se ela está no intervalo
            t = (-1*b - np.sqrt(delta)) / a
            if t_min < t and t < t_max:
                # Computamos o ponto e a normal dado esse t
                point = ray.point(t)
                normal = (point - self.center()) / self.radius()

                return [True, t, point, normal]

            # Caso contrário, computamos a maior raiz e vemos se ela está no intervalo
            t = (-1*b + np.sqrt(delta)) / a
            if t_min < t and t < t_max:
                # Computamos o ponto e a normal dado esse t
                point = ray.point(t)
                normal = (point - self.center()) / self.radius()

                return [True, t, point, normal]

        # Caso o discriminante seja menor que 0, retornamos falso e coisas inválidas
        return [False, -1, -1, -1]
    

class HitableList(Hitable):
    """
        Classe para agrupar objetos do tipo Hitable
    """
    
    # Método para inicializar uma classe do tipo HitableList
    def __init__(self, l):
        self.__list = l

    # Método para retornar a lista de objetos
    def objects(self):
        return self.__list

    # Método que define a função hit
    def hit(self, ray, t_min, t_max):
        # Definindo o status do nosso hit e o ponto mais próximo
        hit_status = [False, -1, -1, -1, None]
        closest = t_max

        # Iterando sobre cada objeto da nossa lista
        for obj in self.objects():
            hit, t, point, normal = obj.hit(ray, t_min, closest)

            # Caso tivermos um hit, atualizamos hit_status e closest
            if hit:
                hit_status[0] = True
                hit_status[1] = t
                hit_status[2] = point
                hit_status[3] = normal
                hit_status[4] = obj.material()

                closest = t

        # Retornamos hit_status
        return hit_status

    # Método que atualiza os objetos da lista
    def update(self):
        for obj in self.objects():
            obj.update()

    # Método static para gerar uma cena aleatória
    @staticmethod
    def random_scene(n_obj):
        objects = []

        # Inserindo uma esfera que será o chão da nossa cena
        objects.append(Sphere(np.array([0, -1000, 0]), 1000, False, Lambertian([0.5, 0.5, 0.5])))

        # Inserindo objetos
        for _ in range(n_obj):
            material = rand()
            center = np.array([rand(-9, 9) + 0.9 * rand(), 0.2, rand(-9, 9) + 0.9 * rand()])
            if np.linalg.norm(center - np.array([4, 0.2, 0])) > 0.9:
                # Escolhendo um material Lambertiano
                if material < 0.8:
                    objects.append(Sphere(center, 0.2, True, Lambertian([rand(), rand(), rand()])))
                
                # Escolhendo um material metálico
                elif material < 0.95:
                    albedo = np.array([0.5 * (1 + rand()), 0.5 * (1 + rand()), 0.5 * (1 + rand())])
                    fuzz = 0.5 * rand()
                    objects.append(Sphere(center, 0.2, False, Metal(albedo, fuzz)))

                # Escolhendo um material dielétrico, mais especificamente vidro
                else:
                    objects.append(Sphere(center, 0.2, False, Dielectric(1.5)))

        # Inserindo uma esfera grande do tipo Dielectric
        objects.append(Sphere(np.array([0.0, 1.0, 0.0]), 1, False, Dielectric(1.5)))

        # Inserindo uma esfera grande do tipo Lambertian
        objects.append(Sphere(np.array([-4.0, 1.0, 0.0]), 1, False, Lambertian(np.array([0.4, 0.2, 0.1]))))

        # Inserindo uma esfera grande do tipo Metal
        objects.append(Sphere(np.array([4.0, 1.0, 0.0]), 1, False, Metal(np.array([0.7, 0.6, 0.5]), 0.0)))

        return objects


# Definindo a main do programa
def main():
    # Obtendo o nome do arquivo via linha de comando
    filename = sys.argv[1]

    # Abrindo o arquivo em modo de escrita
    f = open(filename, 'w')

    # Definindo as dimensões da tela
    try:
        width, height = int(sys.argv[2]), int(sys.argv[3])
    except:
        width, height = 340, 480

    # Definindo o "fator" de antialiasing
    factor_antialiasing = 100

    # Inserindo o formato, dimensões e valor máximo para cor no arquivo
    print('P3', file=f)
    print('{} {}'.format(width, height), file=f)
    print('255', file=f)

    # Definindo nossa câmera
    cam_origin = np.array([13.5, 1.5, 3.0])
    cam_look_at = np.array([0.0, 0.5, -1])
    focus_dist = 9.8
    aperture = 0.1
    cam = Camera(cam_origin, cam_look_at, np.array([0, 1, 0]), 20, width / height, aperture, focus_dist)

    # Definindo os objetos da nossa cena
    try:
        objects = HitableList.random_scene(int(sys.argv[4]))
    except:
        objects = HitableList.random_scene(200)

    world = HitableList(objects)

    # Loop para gerar a cor de cada pixel
    for j in range(height-1, -1, -1):
        for i in range(width):
            # Inicializando nosso vetor de cor
            col = np.array([.0, .0, .0])

            # Loop para o processo de antialiasing (disparar vários raios para o mesmo pixel)
            for _ in range(factor_antialiasing):
                u = (i + rand()) / width
                v = (j + rand()) / height

                # world.update()

                # Disparando um raio e acumulando a cor
                ray = cam.shoot_ray(u, v)
                col += raytrace(ray, world, 0)

            # Calculando a média da cor
            col /= factor_antialiasing

            # Aplicando o processo de gamma-2 correction
            col = np.sqrt(col)

            # Inserindo no arquivo a cor de cada pixel
            col *= 255.99
            print(*col.astype(np.int64), file=f)

    # Fechando o arquivo
    f.close()

# Chamando a nossa main
if __name__ == '__main__':
    start = time()
    main()
    print('----- Took {} seconds to create .ppm file -----'.format(int(time() - start)))