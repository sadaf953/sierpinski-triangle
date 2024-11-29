import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 1000
BACKGROUND = (0, 0, 0)
TRIANGLE_COLOR = (0, 255, 0)
POINT_COLOR = (255, 0, 0)
MIN_DEPTH = 0
MAX_DEPTH = 9

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Sierpinski Triangle")

class SierpinskiTriangle:
    def __init__(self):
        # Calculate the vertices of the main triangle
        self.depth = 0
        self.margin = 50
        self.height = HEIGHT - 2 * self.margin
        self.width = WIDTH - 2 * self.margin
        
        # Calculate vertices for an equilateral triangle
        self.vertices = [
            (WIDTH // 2, self.margin),  # Top
            (self.margin, HEIGHT - self.margin),  # Bottom left
            (WIDTH - self.margin, HEIGHT - self.margin)  # Bottom right
        ]
        
        # Points for chaos game method
        self.points = []
        self.current_point = None

    def draw_triangle(self, vertices, depth):
        """Recursively draw the Sierpinski triangle."""
        if depth == 0:
            pygame.draw.polygon(screen, TRIANGLE_COLOR, vertices, 1)
        else:
            # Calculate midpoints
            mid_1 = ((vertices[0][0] + vertices[1][0]) // 2,
                    (vertices[0][1] + vertices[1][1]) // 2)
            mid_2 = ((vertices[1][0] + vertices[2][0]) // 2,
                    (vertices[1][1] + vertices[2][1]) // 2)
            mid_3 = ((vertices[2][0] + vertices[0][0]) // 2,
                    (vertices[2][1] + vertices[0][1]) // 2)

            # Recursively draw three smaller triangles
            self.draw_triangle([vertices[0], mid_1, mid_3], depth - 1)
            self.draw_triangle([mid_1, vertices[1], mid_2], depth - 1)
            self.draw_triangle([mid_3, mid_2, vertices[2]], depth - 1)

    def chaos_game_point(self):
        """Generate a new point using the chaos game method."""
        if not self.current_point:
            # If no current point, create one randomly within the triangle
            self.current_point = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        
        # Choose a random vertex
        target = random.choice(self.vertices)
        
        # Calculate midpoint between current point and chosen vertex
        new_point = ((self.current_point[0] + target[0]) // 2,
                    (self.current_point[1] + target[1]) // 2)
        
        self.points.append(new_point)
        self.current_point = new_point

    def draw(self, method="recursive"):
        """Draw the Sierpinski triangle using specified method."""
        screen.fill(BACKGROUND)
        
        if method == "recursive":
            self.draw_triangle(self.vertices, self.depth)
        else:  # chaos game method
            # Draw main triangle vertices
            for vertex in self.vertices:
                pygame.draw.circle(screen, TRIANGLE_COLOR, vertex, 3)
            
            # Draw all points
            for point in self.points:
                pygame.draw.circle(screen, POINT_COLOR, point, 1)

        # Draw UI text
        font = pygame.font.Font(None, 36)
        depth_text = font.render(f"Depth: {self.depth}", True, (255, 255, 255))
        method_text = font.render(f"Method: {method}", True, (255, 255, 255))
        help_text = font.render("Up/Down: Change Depth | Space: Switch Method | R: Reset", True, (255, 255, 255))
        
        screen.blit(depth_text, (10, 10))
        screen.blit(method_text, (10, 50))
        screen.blit(help_text, (10, HEIGHT - 40))

def main():
    triangle = SierpinskiTriangle()
    clock = pygame.time.Clock()
    method = "chaos"
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    triangle.depth = min(MAX_DEPTH, triangle.depth + 1)
                elif event.key == pygame.K_DOWN:
                    triangle.depth = max(MIN_DEPTH, triangle.depth - 1)
                elif event.key == pygame.K_SPACE:
                    method = "chaos" if method == "recursive" else "recursive"
                    triangle.points = []
                    triangle.current_point = None
                elif event.key == pygame.K_r:
                    triangle.points = []
                    triangle.current_point = None
                    triangle.depth = 0

        if method == "chaos":
            # Generate multiple points per frame for faster visualization
            for _ in range(100):
                triangle.chaos_game_point()

        triangle.draw(method)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
