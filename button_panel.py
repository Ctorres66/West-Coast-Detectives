import pygame

class Button:
    def __init__(self, x, y, width, height, color, text, text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 30)  # Use the default system font, size 30

    def draw(self, screen):
        # Draw the button rectangle
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw the button text
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class ButtonPanel:
    def __init__(self, x, y, button_width, button_height, button_color, buttons_info):
        self.buttons = []
        for i, (text, text_color) in enumerate(buttons_info):
            button_x = x + (button_width + 10) * i  # 10 pixels between buttons
            button = Button(button_x, y, button_width, button_height, button_color, text, text_color)
            self.buttons.append(button)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def check_click(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                print(f"{button.text} button was clicked")  # Placeholder for actual button click handling
                return button.text  # You can also call a method here or pass a callback to each button
        return None
