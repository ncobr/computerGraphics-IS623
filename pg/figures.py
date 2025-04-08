import pygame
import sys
import math

class DrawAlgorithms():
    def __init__(self):
        pass

    def dda(self, screen, x1, y1, x2, y2, color):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_inc = dx / steps
        y_inc = dy / steps
        x = x1
        y = y1
        for _ in range(steps):
            pygame.draw.circle(screen, color, (int(x), int(y)), 1)
            x += x_inc
            y += y_inc

        self.draw_arrowhead(screen, x2, y2, dx, dy, color)

    def to_pygame_coords(self, vec):
        """Convierte coordenadas matemáticas a coordenadas de pygame"""
        return int(WIDTH // 2 + vec[0] * TICK_SPACING), int(HEIGHT // 2 - vec[1] * TICK_SPACING)


    def draw_vectors(self, vectors, draw_alg):
        """Dibuja los vectores en secuencia y su suma vectorial"""
        origin = (WIDTH // 2, HEIGHT // 2)  # Centro del plano
        position = origin  # Inicio en el origen

        for i, v in enumerate(vectors):
            end_pos = to_pygame_coords((v[0] + (position[0] - WIDTH // 2) / TICK_SPACING,
                                        v[1] + (HEIGHT // 2 - position[1]) / TICK_SPACING))

            draw_alg.dda(screen, position[0], position[1], end_pos[0], end_pos[1], VECTOR_COLOR)
            label = font.render(f"V{i+1}", True, BLACK)
            screen.blit(label, (end_pos[0] + 5, end_pos[1] - 5))
            position = end_pos  # Mover el origen al final del vector actual

        # Dibujar el vector resultante desde el origen
        resultant = sum(vectors)
        resultant_end = to_pygame_coords(resultant)
        draw_alg.dda(screen, origin[0], origin[1], resultant_end[0], resultant_end[1], RESULTANT_COLOR)

        label = font.render("Resultante", True, BLACK)
        screen.blit(label, (resultant_end[0] + 5, resultant_end[1] - 5))

if "__main__" == __name__:
    draw_alg = DrawAlgorithms()
    pygame.init()
    WIDTH, HEIGHT = 640, 640
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)

    draw_alg.dda(screen, 0, 320, 640, 640, BLACK)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
