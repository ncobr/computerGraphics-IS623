import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
BACKGROUND_COLOR = (30, 30, 30)
AXIS_COLOR = (255, 255, 255)
VECTOR_COLOR = (0, 255, 0)
RESULTANT_COLOR = (255, 0, 0)
GRID_COLOR = (70, 70, 70)
TEXT_COLOR = (200, 200, 200)
TICK_SPACING = 50  # Pixels between grid lines
ARROW_HEAD = 10  # Size of arrowhead

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vector Addition")

# Font
font = pygame.font.Font(None, 24)


def draw_grid():
    """Draws a grid with x and y axes."""
    screen.fill(BACKGROUND_COLOR)

    # Draw x and y axes
    pygame.draw.line(screen, AXIS_COLOR, (WIDTH // 2, 0),
                     (WIDTH // 2, HEIGHT), 2)
    pygame.draw.line(screen, AXIS_COLOR, (0, HEIGHT // 2),
                     (WIDTH, HEIGHT // 2), 2)


def to_pygame_coords(vec):
    """Converts vector coordinates to pygame screen coordinates."""
    return int(WIDTH // 2 + vec[0] * TICK_SPACING), int(HEIGHT // 2 - vec[1] * TICK_SPACING)


def draw_vector(start, vec, color, label):
    end = start[0] + vec[0] * TICK_SPACING, start[1] - vec[1] * TICK_SPACING
    pygame.draw.line(screen, color, start, end, 3)

    # Draw arrowhead
    direction = np.array([vec[0], -vec[1]])  # Invert y for pygame
    direction = direction / np.linalg.norm(direction) * ARROW_HEAD  # Normalize
    left = (-direction[1], direction[0])  # Perpendicular left
    right = (direction[1], -direction[0])  # Perpendicular right

    pygame.draw.polygon(screen, color, [
        end,
        (end[0] - left[0], end[1] - left[1]),
        (end[0] - right[0], end[1] - right[1])
    ])

    # Draw label
    text = font.render(label, True, TEXT_COLOR)
    screen.blit(text, (end[0] + 5, end[1] - 5))



def main():
    # Define vectors (Modify these to test different cases)
    vectors = [
        np.array([9.40, 3.42]),   #
        np.array([9.71, 7.05]),  #
        np.array([-6.93, 4.00]),
        np.array([18.00, 0.00]),
        np.array([-10.5, 21.6])
    ]

    result = sum(vectors)

    # Compute resultant vector (sum of all vectors)
    # resultant = sum(vectors)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid()

        # Draw vectors from the origin sequentially
        origin = (WIDTH // 2, HEIGHT // 2)
        position = origin  # Start at the origin

        for i, v in enumerate(vectors):
            draw_vector(position, v, VECTOR_COLOR, f"V{i+1}")
            # Move start position to end of last vector
            position = to_pygame_coords(v)

        # Draw resultant vector from the origin
        draw_vector(origin, result, RESULTANT_COLOR, "Resultant")

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
