import pygame

SPEED = 2


pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

car = pygame.image.load('CarRed64.png')
# car  = pygame.Surface((50, 30))
# car.fill((255, 0, 0))  
position = pygame.math.Vector2(window.get_rect().center)
direction = pygame.math.Vector2(SPEED, 0)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        position += direction
    if keys[pygame.K_DOWN]:
        position -= direction
    if keys[pygame.K_LEFT]:
        direction.rotate_ip(-1)
    if keys[pygame.K_RIGHT]:
        direction.rotate_ip(1)

    window.fill(0)
    angle = direction.angle_to((1, 0))
    rotated_car = pygame.transform.rotate(car, angle)
    window.blit(rotated_car, rotated_car.get_rect(center = (round(position.x), round(position.y))))
    pygame.display.flip()

pygame.quit()
exit()