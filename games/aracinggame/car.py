import pygame
from math import sin, cos, pi, tau
Vec2 = pygame.math.Vector2

LSTEER, NSTEER, RSTEER = -1, 0, 1
NEUTRAL, REVERSE = 0, -1


# to keep it simple, these cars lack a clutch despite trying to model a manual car
# we will call it manual, but technically it's semi-automatic or automated manual
def newCar():
    return {
        "pos" : Vec2(0,0),      # x,y       position
        "posmul" : 1.0,         # positional change multiplier
        "friction" : 1.0,       # surface friction, to limit acceleration/velocity on grass etc.
        "speed" : 0,            # m/s       velocity
        "accel" : 0,            # m/s²      acceleration
        "angle" : 0,            # rad       angle (direction) of car
        "wheelangle" : 0,       # rad       angle of wheels
        "wheelaccel" : 0,       # rad/s     wheel direction acceleration
        "wheelmax" : pi/1.5,    # rad       max wheel turn angle
        "tunehandling" : 6,     # multiplier on how fast wheelangle changes
        "tuneaccel" : 4,        # multiplier on how fast accel changes
        "tunebrake" : 1,        # multiplier on how hard brakes brake
        "reverse" : False,      # used to keep backwards velocity when shifting from reverse to some other gear
        "automatic" : False,    # disable manual input and let car shift automatically
        "accelmax" : 7,         # m/s²      max allowed acceleration by engine
        "enginemax" : 33.3334,  # m/s       max engine velocity (will be multiplied with gear ratio)
        "enginemin" : 8.3334,   # m/s       min ...
        "rpm" : 800,            # self-explanatory
        "rpmmax" : 6400,        # max rpm engine will go by accelerating in some correct gear
        "rpmred" : 6000,        # redline starting point
        "rpmmin" : 800,         # idle rpm, Car will automatically add gas if rpm subceeds this value
        "ratio" : [1.0, 2.66, 1.448, 0.96, 0.745, 0.612, 0.5, 2.66],     # gear ratios: neutral, 1-6, reverse
        # these last four are directly controlled by the driver
        "gear" : NEUTRAL,       # gears are 1-6, reverse and neutral
        "gas" : False,          # accelerator pedal pressed?
        "brake" : False,        # brake pedal pressed?
        "steer" : NSTEER,       # direction to turn steering wheel (left, straight, right)
    }


def handleCarEvents(car, events, keys):
    # load state
    gear = car["gear"]
    gas = car["gas"]
    brake = car["brake"]
    steer = car["steer"]

    gas = keys[pygame.K_w]
    brake = keys[pygame.K_s]
    left = keys[pygame.K_a]
    right = keys[pygame.K_d]
    if left and right: steer = NSTEER
    elif left: steer = LSTEER
    elif right: steer = RSTEER
    else: steer = NSTEER

    # keydown events are only used to change gears
    # in implementing an automatic transmission, you should just IGNORE this input,
    # but NOT REMOVE/ALTER this code
    for e in events:
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                gear -= 6 >= gear > NEUTRAL
            elif e.key == pygame.K_e:
                gear += NEUTRAL <= gear < 6
            elif e.key in (pygame.K_0, pygame.K_KP0):
                gear = NEUTRAL
            elif e.key in (pygame.K_1, pygame.K_KP1):
                gear = 1
            elif e.key in (pygame.K_2, pygame.K_KP2):
                gear = 2
            elif e.key in (pygame.K_3, pygame.K_KP3):
                gear = 3
            elif e.key in (pygame.K_4, pygame.K_KP4):
                gear = 4
            elif e.key in (pygame.K_5, pygame.K_KP5):
                gear = 5
            elif e.key in (pygame.K_6, pygame.K_KP6):
                gear = 6

    return (gear, gas, brake, steer)


# saturated arithmetic
def __clamp(l, r, x):
    if x < l: return l
    if x > r: return r
    return x

def __steerdir(angle):
    if angle > 0: return RSTEER
    if angle < 0: return LSTEER
    return NSTEER

# acceleration curve relating to rpm of engine
def __accelcurve(car, gear):
    if gear == NEUTRAL:
        return 2
    elif gear <= 1:
        return 3
    elif car["rpm"] < car["rpmmin"]:
        return max(car["rpm"] / car["rpmmin"], 0.1)
    else:
        return (2 * car["rpm"]) / car["rpmmax"]


def __accelmax(car, gear):
    if gear <= 1:
        a = car["accelmax"]
    elif car["rpm"] < car["rpmmin"]:
        a = max((car["rpm"] / car["rpmmin"]) * car["accelmax"], 1)
    else:
        a = min((car["rpm"] / (car["rpmmax"] * 0.75)) * car["accelmax"], car["accelmax"])
    return a * car["friction"]


deg = lambda rad: rad * 180/pi      # rad to deg
rad = lambda deg: deg * pi/180      # deg to rad


# car physics are frame-locked
def updateCar(car, signals, fps):
    # the driver has these four methods of controlling their car
    gear, gas, brake, steer = signals

    # HACKATHON CHALLENGE 2
    # make the gears change automatically so Speedy doesn't have to shift anymore!
    if car["automatic"]:
        
        pass


    # set acceleration to some value that will correspond to the same rpm the car currently has
    # if the user shifts into neutral
    if gear != car["gear"] and gear == NEUTRAL:
        car["accel"] = car["rpm"] / car["rpmmax"] * car["accelmax"]

    # automatic shifting into reverse and back
    # < 0.1 because Car adds idle gas, so we never really reach 0 if higher gear is selected
    if brake and (car["speed"] < 0.1 or car["reverse"]):
        gear = REVERSE
    if gas and car["speed"] < 0.1 and gear == REVERSE:
        gear = 1
    if gear == REVERSE:     # flip controls in reverse gear
        gas, brake, steer = brake, gas, -steer
        car["reverse"] = True
    if gear != REVERSE and car["reverse"]:
        steer = -steer
    if gear >= 1 and car["reverse"]:
        brake |= gas
        gas = False

    # accelerate steering wheel to desired direction or into straight position
    if steer == NSTEER:
        car["wheelaccel"] = -__steerdir(car["wheelangle"]) * car["tunehandling"] / fps
    else:
        car["wheelaccel"] = -steer * car["tunehandling"] / fps

    # apply steering wheel acceleration to the steering wheel
    # clamp wheel angle to maximum turn angle
    car["wheelangle"] = __clamp(-car["wheelmax"], car["wheelmax"], car["wheelangle"] + car["wheelaccel"])
    if abs(car["wheelangle"]) < rad(2) and steer == NSTEER:
        car["wheelangle"] = 0

    # only rotate when car is moving, full rotation speed at 3 m/s or above
    car["angle"] += (car["wheelangle"] * min(car["speed"] / 3, 1)) / fps
    car["angle"] %= tau


    # if power is connected, increase acceleration
    if gas and gear != NEUTRAL:
        car["accel"] += car["tuneaccel"] * __accelcurve(car, gear) * car["friction"] / fps
        car["accel"] = min(car["accel"], __accelmax(car, gear))
    elif gas and gear == NEUTRAL and car["accel"] <= car["accelmax"]:
        car["accel"] += car["tuneaccel"] * __accelcurve(car, gear) / fps
        #car["accel"] = min(car["accel"], car["accelmax"])
    elif car["accel"] > 0 and gear == NEUTRAL:
        car["accel"] -= 3 / fps       # acceleration in neutral determines rpm, not speed
        car["accel"] = max(car["accel"], 0)
    elif car["accel"] > 0 and car["rpm"] >= car["rpmmin"]:
        car["accel"] = 0    # acceleration stops when not pressing accelerator pedal

    # drop acceleration and velocity when applying brakes
    if brake and car["speed"] > 0:
        if gear != NEUTRAL:
            car["accel"] -= 45 / fps
            car["accel"] = max(car["accel"], 0)
        car["speed"] -= 20 * car["tunebrake"] / fps
        car["speed"] = max(car["speed"], 0)

    # idle gas
    if car["rpm"] < car["rpmmin"] and gear != NEUTRAL:
        car["accel"] += car["tuneaccel"] * __accelcurve(car, gear) * car["friction"] / fps
        car["accel"] = min(car["accel"], __accelmax(car, gear))
    elif car["rpm"] < car["rpmmin"]:
        car["accel"] += car["tuneaccel"] * __accelcurve(car, gear) / fps
        car["accel"] = min(car["accel"], car["accelmax"])

    # the faster you go, the more speed you lose by steering
    if car["wheelangle"] != 0:
        car["speed"] -= (car["speed"] * (abs(car["wheelangle"]) / tau)) / fps
        car["speed"] = max(car["speed"], 0)

    # increase velocity if accelerating and not redlining the engine
    if car["accel"] > 0 and car["rpm"] <= car["rpmmax"] and gear != NEUTRAL:
        car["speed"] += car["accel"] * car["friction"] / fps
    elif car["rpm"] > car["rpmmax"] + 1000:
        # if rpm exceeds safe range by a lot, apply strong braking force
        car["speed"] -= 45 / fps
        car["speed"] = max(car["speed"], 0)
    else:
        # else drop velocity due to friction on road surface
        car["speed"] -= 5 * (1 / car["friction"]) / fps
        car["speed"] = max(car["speed"], 0)

    # limit speed when friction is high
    if car["speed"] > car["enginemax"] / car["ratio"][6] * car["friction"]:
        car["speed"] -= 5 * (1 / car["friction"]) / fps
        car["speed"] = max(car["speed"], 0)


    #if gear == 1 or gear == REVERSE:
        # at velocity 0, rpm shall equal idle rpm as to avoid stalling the engine
        #minspeed = -car["rpmmin"] / car["rpmmax"] * maxspeed
        #car["rpm"] = ((car["speed"] - minspeed) / maxspeed) * car["rpmmax"]
    if gear == NEUTRAL:
        # rpm in neutral is controlled by acceleration
        car["rpm"] = (car["accel"] / car["accelmax"] * car["rpmmax"])
        #car["rpm"] = car["rpmmin"] + (car["accel"] / car["accelmax"]) * (car["rpmmax"] - car["rpmmin"])
    else:
        maxspeed = car["enginemax"] / car["ratio"][gear]
        minspeed = car["enginemin"] / car["ratio"][gear]
        if car["speed"] >= minspeed:
            car["rpm"] = ((car["speed"] - minspeed) / (maxspeed - minspeed)) * (car["rpmmax"] - car["rpmmin"]) + car["rpmmin"]
        else:
            car["rpm"] = car["speed"] / minspeed * car["rpmmin"]



    # calculate angle of car and mirror it if in reverse gear
    # this allows us to calculate the new position of the vehicle
    angle = Vec2(cos(car["angle"]), -sin(car["angle"]))
    if car["reverse"]: angle = -angle
    car["pos"] += angle * car["speed"] * car["posmul"] / fps

    if gear >= 1 and car["reverse"]:
        car["speed"] -= car["enginemax"] / car["ratio"][1] / fps
        car["speed"] = max(car["speed"], 0)
    if car["speed"] < 0.1 and car["reverse"]:
        car["reverse"] = False

    # save state
    car["gear"] = gear
    car["gas"] = gas
    car["brake"] = brake
    car["steer"] = steer

    return car


def pos(car, set=None):
    p = [car["pos"][0], car["pos"][1]]
    if set: car["pos"][0], car["pos"][1] = set[0], set[1]
    return p


def speed(car):
    return car["speed"]


def rpm(car):
    return car["rpm"]


def redlining(car):
    return car["rpm"] >= car["rpmred"]


def gear(car):
    g = car["gear"]
    if g < 1: g = "N" if g == NEUTRAL else "R"
    return str(g)


def automatic(car, set=None):
    a = car["automatic"]
    if type(set) == bool: car["automatic"] = set
    return a


def friction(car, set=None):
    f = car["friction"]
    if set: car["friction"] = set
    return f


def rotatedTexture(car, tex, mulpos=1.0):
    angle = deg(car["angle"])
    rottex = pygame.transform.rotate(tex, angle)
    posx = car["pos"][0] * mulpos
    posy = car["pos"][1] * mulpos
    rect = rottex.get_rect(center=tex.get_rect(center=(posx, posy)).center)
    return rottex, rect


# everything after this point is just for testing and debugging

def __speed(car):
    a = car["speed"] * 3.6
    return f"Speed {a:0.2f} km/h"

def __rpm(car):
    a = car["rpm"]
    return f"RPM {a:0.2f}"

def __gear(car):
    a = car["gear"]
    if a < 1: a = "N" if a == 0 else "R"
    return f"Gear {a}"

def __accel(car):
    a = car['accel']
    return f"Accel {a:0.2f} m/s²"

def __pos(car):
    a = car['pos'][0]
    b = car['pos'][1]
    return f"Pos ({a:0.2f}|{b:0.2f})"

def __angledeg(car):
    a = deg(car["angle"])
    return f"Angle {a:0.2f}°"

def __steer(car):
    a = car["steer"]
    if car["gear"] == REVERSE: a = -a
    if a == NSTEER: a = "STRAIGHT"
    elif a == RSTEER: a = "RIGHT"
    elif a == LSTEER: a = "LEFT"
    else: a = "ERROR"
    return "Steer " + a


def __main():
    w, h = 1000, 800
    pygame.init()
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    FPS = 144
    car = newCar()
    tex = pygame.image.load("car.png")
    tex = pygame.transform.scale(tex, (48, 24))
    tex = tex.convert_alpha(tex)


    while True:
        events = pygame.event.get()
        if any(e.type == pygame.QUIT for e in events):
            print(__speed(car), __gear(car), __rpm(car), __pos(car), __accel(car), __steer(car), __angledeg(car), sep='\t', flush=True)
            return pygame.quit()

        keys = pygame.key.get_pressed()
        signals = handleCarEvents(car, events, keys)
        updateCar(car, signals, FPS)

        screen.fill("white")
        angle = deg(car["angle"])
        rottex = pygame.transform.rotate(tex, angle)
        posx = car["pos"][0] * 10 % w
        posy = car["pos"][1] * 10 % h
        rect = rottex.get_rect(center=tex.get_rect(center=(posx, posy)).center)
        screen.blit(rottex, rect)
        pygame.display.flip()

        print(__speed(car), __gear(car), __rpm(car), __pos(car), __accel(car), __steer(car), __angledeg(car), sep='\t', end='', flush=True)
        clock.tick(FPS)
        print("\r"," " * 150, end='\r')


# uncomment to test
#__main()
