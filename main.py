import pygame,math



class Charge:
    def __init__(self, **kwargs):
        self.magnitude = kwargs.get('magnitude')
        self.position = kwargs.get('position')

    def get_sign(self):
        return self.magnitude/math.fabs(self.magnitude)

    def get_sq_distance_from(self, position: tuple):
        return (self.position[0] - position[0]) ** 2 + (self.position[1] - position[1]) ** 2

    def get_shifted_position(self):
        return self.position[0] - 10, self.position[1] - 10

    def get_component_factors(self, position: tuple):
        if self.position[0] == position[0]:
            return 0, 1
        angle = math.fabs(math.atan((self.position[1] - position[1]) / (self.position[0] - position[0])))
        if self.position[0] > position[0] and self.position[1] > position[1]:
            angle = math.pi - angle
        elif self.position[0] > position[0] and self.position[1] < position[1]:
            angle = math.pi + angle
        elif self.position[0] < position[0] and position[1] > self.position[1]:
            angle = -angle
        return math.cos(angle), math.sin(angle)



def get_particles(charges,size):
    n = int(input("number of charged particles: "))
    for i in range(n):
        mag = int(input("Enter charge of particle number "+str(i+1)+": "))
        x = int(input("Enter x coordinate of charge: "))
        y = int(input("Enter y coordinate of charge: "))
        charges.append(Charge(magnitude=mag, position=((size[0]/2+x,size[1]/2+ y))))
    return charges

def grid():    # draw grid
    for row in range(0, size[0], 30):
        pygame.draw.line(screen, (50, 50, 50), (0, row), (size[0], row))
    for col in range(0, size[1], 30):
        pygame.draw.line(screen, (50, 50, 50), (col, 0), (col, size[1]))


def display_field():   # this will draw the electric field
    for j in range(0, size[0], 30):
        for k in range(0, size[1], 30):
            [x_net,y_net] = [0,0]
            success = True
            for charge in charges:
                if charge.get_sq_distance_from((j, k)) == 0:
                    success = False
                else:
                    field = 10e5 * charge.magnitude / (charge.get_sq_distance_from((j, k)))
                    cos, sin = charge.get_component_factors((j, k))
                    x_net += (cos * field)
                    y_net += (sin * field)
            if success:
                if x_net != 0:
                    angle = math.atan(y_net / x_net)
                else:
                    angle = math.pi / 2
                del_x = arrow_len * math.cos(angle)
                del_y = arrow_len * math.sin(angle)
                pygame.draw.line(screen, (200, 235, 0), (j, k), (j + del_x, k - del_y), 1)


def display_charges():
    for each_charge in charges:
        if each_charge.magnitude < 0:
            screen.blit(negative, each_charge.get_shifted_position())
        else:
            screen.blit(positive, each_charge.get_shifted_position())


if __name__ == '__main__':

    charges = []
    size = [720, 720]
    charges=get_particles(charges,size)

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Electric Field Visualization')
    arrow_len = 12
    negative = pygame.image.load('images/negative.png')
    negative = pygame.transform.scale(negative, (20, 20))
    positive = pygame.image.load('images/positive.png')
    positive = pygame.transform.scale(positive, (20, 20))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        grid()
        display_field()
        display_charges()
        pygame.display.update()
