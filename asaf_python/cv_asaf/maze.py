
import numpy as np
import multiprocessing
import pygame as pg
from numba import njit


def main():
    size = 25  # size of the map
    posx, posy, posz = (1, np.random.randint(1, size - 1), 0.5)
    rot, rot_v = (np.pi / 4, 0)
    lx, ly, lz = (size / 2 - 0.5, size / 2 - 0.5, 1)
    mapc, maph, mapr, exitx, exity, treasx, treasy = maze_generator(posx, posy, size)

    res, res_o = 2, [64, 96, 112, 160, 192, 224]
    width, height, mod, inc, sky, floor = adjust_resol(res_o[res])

    nuc = 1
    pool = multiprocessing.Pool(processes=nuc)

    running = True
    pg.init()
    font = pg.font.SysFont("Arial", 18)
    screen = pg.display.set_mode((800, 600))

    clock = pg.time.Clock()
    pg.mouse.set_visible(False)
    pg.mouse.set_pos([400, 300])

    traceray = False

    while running:
        distance_to_treasure = calculate_distance(posx, posy, treasx, treasy)
        # בתוך לולאת המשחק


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == ord('r'):  # switch ray tracing
                    traceray = not traceray
                    rot_v = 0
                    if traceray:
                        print('Ray tracing on!')
                    else:
                        print('Ray tracing off!')

                if event.key == ord('q'):  # change resolution
                    if res > 0:
                        res = res - 1
                        width, height, mod, inc, sky, floor = adjust_resol(res_o[res])
                if event.key == ord('e'):
                    if res < len(res_o) - 1:
                        res = res + 1
                        width, height, mod, inc, sky, floor = adjust_resol(res_o[res])

        if traceray:

            param_values = []
            for j in range(height):  # vertical loop
                rot_j = rot_v + np.deg2rad(24 - j / mod)
                for i in range(width):  # horizontal vision loop
                    param_values.append([rot, i, j, inc, rot_j])
            tam = len(param_values)
            lista = []
            pixels = []

            for i in range(nuc):
                lista.append([i, param_values[i * int(tam / nuc):(i + 1) * int(tam / nuc)],
                              mapc, maph, lx, ly, lz, exitx, exity, mapr, posx, posy, posz, mod])

            retorno = pool.map(caster, lista)

            for i in range(nuc):
                pixels.append(retorno[i][1])

            pixels = np.reshape(pixels, (height, width, 3))
            pixels = np.asarray(pixels) / np.sqrt(np.max(pixels))

        else:
            pixels = np.ones([height, width, 3])
            for i in range(width):  # vision loop
                rot_i = rot + np.deg2rad(i / mod - 30)
                pixels[0:len(sky), i] = sky * (0.7 + np.sin((rot_i - np.pi / 2) / 2) ** 2 / 3)
                pixels[int(height / 2) + 1:height - 1, i] = floor[:-1] * (
                            0.75 + np.sin((rot_i + np.pi / 2) / 2) ** 2 / 4)
                x, y = (posx, posy)
                sin, cos = (0.05 * np.sin(rot_i) / mod, 0.05 * np.cos(rot_i) / mod)

                n, half = 0, None
                c, h, x, y, n, half, ty, tc = ray_caster(x, y, i / mod, exitx, exity, maph, mapc, sin, cos, n, half,
                                                         mod)
                if mapr[int(x)][int(y)]:
                    pixels, ty, tc = reflection_caster(x, y, i, exitx, exity, maph, mapc, sin, cos, n, c, h, half,
                                                       pixels, ty, tc, height, mod)
                else:
                    pixels[int((height - h * height) / 2):int((height + h * height) / 2), i] = c
                    if half != None:
                        pixels[int(height / 2):int((height + half[0] * height) / 2), i] = half[1]
                if len(ty) > 0:
                    ty = (np.asarray(ty) * 1.01 * height / 2 + height / 2).astype(int)
                    ty2, ind = np.unique(ty, return_index=True)
                    pixels[ty2, i] = (np.asarray(tc)[ind] * 3 + pixels[ty2, i]) / 4

        surf = pg.surfarray.make_surface((np.rot90(pixels * 255)).astype('uint8'))
        surf = pg.transform.scale(surf, (800, 600))
        screen.blit(surf, (0, 0))
        distance_text = font.render(f"Distance to treasure: {int(distance_to_treasure)}", True, pg.Color("white"))
        screen.blit(distance_text, (10, 20))
        pg.display.flip()

        # player's movement
        if (int(posx) == exitx and int(posy) == exity):
            break

        pressed_keys = pg.key.get_pressed()
        posx, posy, rot, rot_v = movement(pressed_keys, posx, posy, rot, rot_v, maph, clock.tick() / 500)
        pg.mouse.set_pos([400, 300])
    stop_thread = True
    pg.quit()
    pool.close()

# function generates a random maze by creating matrices to represent the maze's color, height, and reflective surfaces.
# It carves paths from the starting point to the exit, ensuring accessibility.
# Additionally, it randomly selects a treasure location within the maze and returns the maze structure along with the exit and treasure coordinates.
def maze_generator(x, y, size):
    mapc = np.random.uniform(0, 1, (size, size, 3))
    mapr = np.random.choice([0, 0, 0, 0, 1], (size, size))
    maph = np.random.choice([0, 0, 0, 0, 0, 0, 0, .2, .4, .6, .8], (size, size))
    maph[0, :], maph[size - 1, :], maph[:, 0], maph[:, size - 1] = (1, 1, 1, 1)

    mapc[x][y], maph[x][y], mapr[x][y] = (0, 0, 0)
    count = 0
    while 1:
        testx, testy = (x, y)
        if np.random.uniform() > 0.5:
            testx = testx + np.random.choice([-1, 1])
        else:
            testy = testy + np.random.choice([-1, 1])
        if testx > 0 and testx < size - 1 and testy > 0 and testy < size - 1:
            if maph[testx][testy] == 0 or count > 5:
                count = 0
                x, y = (testx, testy)
                mapc[x][y], maph[x][y], mapr[x][y] = (0, 0, 0)
                if x == size - 2:
                    exitx, exity = (x, y)
                    break
            else:
                count = count + 1
    treasx, treasy = np.random.randint(1, size - 1), np.random.randint(1, size - 1)
    while maph[treasx][treasy] != 0 or (treasx == x and treasy == y):
        treasx, treasy = np.random.randint(1, size - 1), np.random.randint(1, size - 1)
    return mapc, maph, mapr, exitx, exity, treasx, treasy

# This function calculates the Euclidean distance between the player's position
# (posx, posy) and the treasure's position
# (treasx, treasy) in the maze.
# It's used to display the distance to the treasure  on the screen.

def calculate_distance(posx, posy, treasx, treasy):
    return np.sqrt((posx - treasx)**2 + (posy - treasy)**2)


# This function handles the player's movement within the maze.
# It takes the current position (posx, posy), rotation rot, vertical rotation rot_v,
# the maze map maph, and the elapsed time et as inputs.
# It processes the player's movement based on the keys pressed and updates the player's position and rotation accordingly.
def movement(pressed_keys, posx, posy, rot, rot_v, maph, et):
    x, y = (posx, posy)

    # Adjust rotation based on 'a' (left) or 'd' (right) key presses
    if pressed_keys[pg.K_RIGHT]:
        rot -= et * 2  # Adjust rotation speed as needed
    if pressed_keys[pg.K_LEFT]:
        rot += et * 2  # Adjust rotation speed as needed

    # Process forward (w) and backward (s) movement
    if pressed_keys[pg.K_UP]:
        x, y = (x + et * np.cos(rot), y + et * np.sin(rot))
    if pressed_keys[pg.K_DOWN]:
        x, y = (x - et * np.cos(rot), y - et * np.sin(rot))

    # Process strafing movement: left (a) and right (d) with adjusted camera angle
    if pressed_keys[pg.K_LEFT]:
        x, y = (x - et * np.sin(rot), y + et * np.cos(rot))
    if pressed_keys[pg.K_RIGHT]:
        x, y = (x + et * np.sin(rot), y - et * np.cos(rot))

    # Check if the new position is within bounds and not colliding
    if maph[int(x)][int(y)] == 0:
        posx, posy = (x, y)

    return posx, posy, rot, rot_v

@njit(fastmath=True)
def fast_ray(x, y, z, cos, sin, sinz, maph):
    while 1:
        x, y, z = x + cos, y + sin, z + sinz
        if (z > 1 or z < 0):
            break
        if maph[int(x)][int(y)] > z:
            break
    return x, y, z



#This function simulates the path of a ray from the player's viewpoint and calculates the color of the pixel corresponding to that ray.
# It considers the position (x, y, z) of the ray, the direction (cos, sin, sinz),
# the colors of the map and objects, and the position of the light source (lx, ly, lz).
def view_ray(x, y, z, cos, sin, sinz, mapc, lx, ly, lz, maph, exitx, exity):
    x, y, z = fast_ray(x, y, z, cos, sin, sinz, maph)
    dtol = np.sqrt((x - lx) ** 2 + (y - ly) ** 2 + (lz - 1) ** 2)

    if z > 1:  # ceiling
        ##        c = np.asarray([0.3,0.7,1])
        if (x - lx) ** 2 + (y - ly) ** 2 < 0.1:  # light source
            c = np.asarray([1, 1, 1])
        elif int(np.rad2deg(np.arctan((y - ly) / (x - lx))) / 6) % 2 == 1:
            c = np.asarray([0.3, 0.7, 1]) * (abs(np.sin(y + ly) + np.sin(x + lx)) + 2) / 5
            c = c + 1 - max(c)
        else:
            c = np.asarray([.2, .6, 1]) * (abs(np.sin(y + ly) + np.sin(x + lx)) + 2) / 5
            c = c + 1 - max(c)
    elif z < 0:  # floor
        if int(x) == exitx and int(y) == exity:
            c = np.asarray([0, 0, .6])
        elif int(x * 2) % 2 == int(y * 2) % 2:
            c = np.asarray([.1, .1, .1])
        else:
            c = np.asarray([.8, .8, .8])
    elif z < maph[int(x)][int(y)]:  # walls
        c = np.asarray(mapc[int(x)][int(y)])
    else:
        c = np.asarray([.5, .5, .5])  # if all fails

    h = 0.3 + 0.7 * np.clip(1 / dtol, 0, 1)
    c = c * h
    return c, x, y, z, dtol





#This function calculates the effect of shadows on the pixel color based on the presence
# of obstacles between the player's viewpoint and the light source.
# It takes into account the position (x, y, z) of the ray,
# the position of the light source (lx, ly, lz), the maze map maph,
# the current pixel color c, the incidence inc, and the distance dtol between the player and the light source.
@njit(fastmath=True)
def shadow_ray(x, y, z, lx, ly, lz, maph, c, inc, dtol):
    dx, dy, dz = inc * 5 * (lx - x) / dtol, inc * 5 * (ly - y) / dtol, inc * 5 * (lz - z) / dtol
    mod = 1
    while 1:
        x, y, z = (x + dx, y + dy, z + dz)
        if maph[int(x)][int(y)] != 0 and z <= maph[int(x)][int(y)]:
            mod = mod * 0.9
            if mod < 0.5:
                break
        elif z > 0.9:
            break
    return c * mod

#: This function calculates the reflection of light rays off reflective surfaces in the maze.
# It considers the position (x, y, z) of the ray, the direction (cos, sin, sinz), the colors of the map and objects,
# the position of the light source (lx, ly, lz),
# the maze map maph, the exit position (exitx, exity),
# the current pixel color c, the player's position posz, the incidence inc,
# the reflectivity map mapr, and a flag recur to prevent infinite recursion.
def reflection(x, y, z, cos, sin, sinz, mapc, lx, ly, lz, maph, exitx, exity, c, posz, inc, mapr, recur):
    if abs(z - maph[int(x)][int(y)]) < abs(sinz):
        sinz = -sinz
    elif maph[int(x + cos)][int(y - sin)] != 0:
        cos = -cos
    else:
        sin = -sin
    c2, x, y, z, dtol = view_ray(x, y, z, cos, sin, sinz, mapc, lx, ly, lz, maph, exitx, exity)
    if z < 1:
        c2 = shadow_ray(x, y, z, lx, ly, lz, maph, c2, inc, dtol)
    if (mapr[int(x)][int(y)] != 0 and z < 1 and z > 0 and not recur):
        c2 = reflection(x, y, z, cos, sin, sinz, mapc, lx, ly, lz, maph, exitx, exity, c2, posz, inc, mapr, recur=True)
    c = (c + c2) / 2
    return c



# This function is used in the ray tracing process to parallelize the ray casting calculations using multiprocessing.
# It takes a list of parameter values lista as input and returns the result of the ray casting computation for a subset of parameters.
def caster(lista):
    param_values = lista[1]
    mapc = lista[2]
    maph = lista[3]
    lx = lista[4]
    ly = lista[5]
    lz = lista[6]
    exitx = lista[7]
    exity = lista[8]
    mapr = lista[9]
    posx = lista[10]
    posy = lista[11]
    posz = lista[12]
    mod = lista[13]

    pixels = []

    for values in param_values:
        rot = values[0]
        i = values[1]
        j = values[2]
        inc = values[3]
        rot_j = values[4]
        rot_i = rot + np.deg2rad(i / mod - 30)
        x, y, z = (posx, posy, posz)
        sin, cos, = (inc * np.sin(rot_i), inc * np.cos(rot_i))
        sinz = inc * np.sin(rot_j)
        c, x, y, z, dtol = view_ray(x, y, z, cos, sin, sinz, mapc, lx, ly, lz,
                                    maph, exitx, exity)
        if z < 1:
            c = shadow_ray(x, y, z, lx, ly, lz, maph, c, inc, dtol)
            if mapr[int(x)][int(y)] != 0 and z > 0:
                c = reflection(x, y, z, cos, sin, sinz, mapc, lx, ly, lz, maph,
                               exitx, exity, c, posz, inc, mapr, recur=False)

        pixels.append(c)

    return lista[0], pixels


def ray_caster(x, y, i, ex, ey, maph, mapc, sin, cos, n, half, mod):
    zz = 0.5
    if half == None:
        zz = 0.1
    x, y, n, tc, ty = fast_ray_caster(x, y, zz, cos, sin, maph, n, i, ex, ey, mod)
    h, c = shader(n, maph, mapc, sin, cos, x, y, i, mod)

    if maph[int(x)][int(y)] < 0.5 and half == None:
        half = [h, c, n]
        x, y, n, tc2, ty2 = fast_ray_caster(x, y, 0.5, cos, sin, maph, n, i, ex, ey, mod)
        ty, tc = ty + ty2, tc + tc2
        h, c = shader(n, maph, mapc, sin, cos, x, y, i, mod)
    return (c, h, x, y, n, half, ty, tc)


@njit(fastmath=True)
def fast_ray_caster(x, y, z, cos, sin, maph, n, i, ex, ey, mod):
    ty, tc = [], []
    while 1:
        n = n + 1
        x, y = x + cos, y + sin
        if z < 0.5 and int(x * 2) % 2 == int(y * 2) % 2:
            th = 1 / (0.05 / mod * n)  # *np.cos(np.deg2rad(i/mod - 30)))
            if th < 1 and th >= 0:
                ty.append(th)
                if int(x) == ex and int(y) == ey:
                    tc.append(np.asarray([0, 0, 1]))
                else:
                    tc.append(np.asarray([0, 0, 0]))
        if maph[int(x)][int(y)] > z:
            break
    return x, y, n, tc, ty


def shader(n, maph, mapc, sin, cos, x, y, i, mod):
    h = np.clip(1 / (0.05 / mod * n), 0, 1)  # *np.cos(np.deg2rad(i/mod-30))), 0, 1)
    c = np.asarray(mapc[int(x)][int(y)]) * (0.4 + 0.6 * h)

    if maph[int(x + cos)][int(y - sin)] == 1:
        c = 0.85 * c

        if maph[int(x - cos)][int(y + sin)] == 1 and sin > 0:
            c = 0.7 * c
    return h, c


def reflection_caster(x, y, i, ex, ey, maph, mapc, sin, cos, n, c, h, half, pixels, ty, tc, height, mod):
    hor = int(height / 2)
    hh = int((h * height) / 2)
    pixels[hor - hh:hor + hh, i] = np.add(pixels[hor - hh:hor + hh, i], np.asarray([c] * (hh * 2))) / 2

    if maph[int(x + cos)][int(y - sin)] > 0.5:
        cos = -cos

    else:
        sin = -sin

    c2, h2, x, y, n2, half2, ty2, tc2 = ray_caster(x, y, i, ex, ey, maph, mapc, sin, cos, n, half, mod)

    ty, tc = ty + ty2, tc + tc2
    hh = int((h2 * height) / 2)
    pixels[hor - hh:hor + hh, i] = (c + c2) / 2

    if half2 != None and half == None:
        hh = int((half2[0] * height) / 2)
        pixels[hor:hor + hh, i] = (c + half2[1]) / 2

    elif half != None:
        hh = int((half[0] * height) / 2)
        pixels[hor:hor + hh, i] = half[1]

    return pixels, ty, tc


def adjust_resol(width):
    height = int(0.75 * width)
    mod = width / 64
    inc = 0.05 / mod
    gradient = np.linspace(0, 1, int(height / 2 - 1))
    sky = np.asarray([gradient / 3, gradient / 2 + 0.25, gradient / 3 + 0.5]).T
    floor = np.asarray([gradient, gradient, gradient]).T
    print('Resolution: ', width, height)
    return width, height, mod, inc, sky, floor


if __name__ == '__main__':
    main()