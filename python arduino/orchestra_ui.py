import pygame
import sys
import math

class OrchestraUI:
    def __init__(self, width=1200, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Digital Symphony - Orchestra Conductor")

        # Colors
        self.colors = {
            'background': (20, 20, 30),
            'active': (255, 215, 0),      # Gold for active sections
            'inactive': (60, 60, 80),     # Dark gray for inactive
            'text': (255, 255, 255),      # White text
            'tempo_slow': (100, 200, 255), # Light blue
            'tempo_normal': (255, 255, 255), # White
            'tempo_fast': (255, 100, 100),   # Light red
            'circle_outline': (100, 100, 120), # Circle border
            'arrow': (255, 100, 100),     # Red arrow
            'section_border': (200, 200, 200) # Section dividers
        }

        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        # Circle parameters
        self.circle_center = (width // 2, height // 2 + 50)
        self.circle_radius = 200
        self.inner_radius = 50

        # Orchestra sections
        self.sections = {
            'UP': {
                'name': 'BRASS',
                'active': False,
                'start_angle': 225, # Left section
                'end_angle': 315,
                'text_angle': 270
              
            },
            'RIGHT': {
                'name': 'WOODWINDS',
                'active': False,
                'start_angle': 315,  # Top section
                'end_angle': 45,
                'text_angle': 0
                
            },
            'DOWN': {
                'name': 'PERCUSSION',
                'active': False,
                'start_angle': 45,   # Right section
                'end_angle': 135,
                'text_angle': 90
            },
            'LEFT': {
                'name': 'STRINGS',
                'active': False,
                
                'start_angle': 135,  # Bottom section
                'end_angle': 225,
                'text_angle': 180
            }
        }

        self.current_tempo = "normal"
        self.current_gesture = None  # Track current gesture for arrow
        
    def update_section_status(self, section, is_active):
        """Update whether a section is currently playing"""
        if section in self.sections:
            self.sections[section]['active'] = is_active
    
    def update_tempo(self, tempo):
        """Update the current tempo display"""
        self.current_tempo = tempo
    
    def update_current_gesture(self, gesture):
        """Update which gesture is currently being detected"""
        self.current_gesture = gesture
    
    def draw_circle_section(self, section_key, section_data):
        start_angle = math.radians(section_data['start_angle'])
        end_angle = math.radians(section_data['end_angle'])

        if end_angle < start_angle:
            end_angle += 2 * math.pi

        cx, cy = self.circle_center  # ✅ Fix added
        text = section_data['name']  # ✅ Fix added

        color = self.colors['active'] if section_data['active'] else self.colors['inactive']

        points = [(cx, cy)]

        num_points = 20
        for i in range(num_points + 1):
            angle = start_angle + (end_angle - start_angle) * i / num_points
            x = cx + self.circle_radius * math.cos(angle)
            y = cy + self.circle_radius * math.sin(angle)
            points.append((x, y))

        for i in range(num_points, -1, -1):
            angle = start_angle + (end_angle - start_angle) * i / num_points
            x = cx + self.inner_radius * math.cos(angle)
            y = cy + self.inner_radius * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, self.colors['section_border'], points, 2)

        text_angle = math.radians(section_data['text_angle'])
        text_radius = (self.circle_radius + self.inner_radius) / 2
        text_x = cx + text_radius * math.cos(text_angle)
        text_y = cy + text_radius * math.sin(text_angle)

        text_surface = self.font_small.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=(text_x, text_y + 15))
        self.screen.blit(text_surface, text_rect)

    # Fix: handle wrapping (e.g., 315° to 45° should cover the top part)
        if end_angle < start_angle:
             end_angle += 2 * math.pi

            
            # Choose color based on active state
             color = self.colors['active'] if section_data['active'] else self.colors['inactive']
            
            # Create points for the arc segment
        points = [(cx, cy)]  # Center point
            
            # Add points along the outer arc
        num_points = 20
        for i in range(num_points + 1):
                angle = start_angle + (end_angle - start_angle) * i / num_points
                x = cx + self.circle_radius * math.cos(angle)
                y = cy + self.circle_radius * math.sin(angle)
                points.append((x, y))
            
            # Add points along the inner arc (reverse direction)
        for i in range(num_points, -1, -1):
                angle = start_angle + (end_angle - start_angle) * i / num_points
                x = cx + self.inner_radius * math.cos(angle)
                y = cy + self.inner_radius * math.sin(angle)
                points.append((x, y))
            
            # Draw the filled section
        pygame.draw.polygon(self.screen, color, points)
            
            # Draw section border
        pygame.draw.polygon(self.screen, self.colors['section_border'], points, 2)
            
            # Draw section name
        text_angle = math.radians(section_data['text_angle'])
        text_radius = (self.circle_radius + self.inner_radius) / 2
        text_x = cx + text_radius * math.cos(text_angle)
        text_y = cy + text_radius * math.sin(text_angle)
            
            
            
            
            
            # Draw text
        text_surface = self.font_small.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=(text_x, text_y + 15))
        self.screen.blit(text_surface, text_rect)
        
    def draw_gesture_arrow(self):
        """Draw an arrow pointing to the current gesture direction"""
        if self.current_gesture is None:
            return
            
        cx, cy = self.circle_center
        arrow_length = self.circle_radius + 50
        arrow_width = 20
        
        # Define arrow directions
        arrow_angles = {
            'UP': -90,    # Point up
            'RIGHT': 0,   # Point right
            'DOWN': 90,   # Point down
            'LEFT': 180   # Point left
        }
        
        if self.current_gesture not in arrow_angles:
            return
            
        angle = math.radians(arrow_angles[self.current_gesture])
        
        # Calculate arrow tip position
        tip_x = cx + arrow_length * math.cos(angle)
        tip_y = cy + arrow_length * math.sin(angle)
        
        # Calculate arrow base points
        base_length = 30
        base_angle1 = angle + math.radians(150)
        base_angle2 = angle + math.radians(-150)
        
        base_x1 = tip_x + base_length * math.cos(base_angle1)
        base_y1 = tip_y + base_length * math.sin(base_angle1)
        base_x2 = tip_x + base_length * math.cos(base_angle2)
        base_y2 = tip_y + base_length * math.sin(base_angle2)
        
        # Draw arrow
        arrow_points = [(tip_x, tip_y), (base_x1, base_y1), (base_x2, base_y2)]
        pygame.draw.polygon(self.screen, self.colors['arrow'], arrow_points)
        
        # Draw gesture label
        label = f"GESTURE: {self.current_gesture}"
        label_surface = self.font_medium.render(label, True, self.colors['arrow'])
        label_rect = label_surface.get_rect(center=(tip_x, tip_y - 40))
        self.screen.blit(label_surface, label_rect)
    
    def draw_center_circle(self):
        """Draw the center circle of the orchestra"""
        cx, cy = self.circle_center
        
        # Draw inner circle
        pygame.draw.circle(self.screen, self.colors['background'], (cx, cy), self.inner_radius)
        pygame.draw.circle(self.screen, self.colors['circle_outline'], (cx, cy), self.inner_radius, 3)
        
    
    def draw_tempo_display(self):
        """Draw the current tempo information"""
        tempo_colors = {
            'slow': self.colors['tempo_slow'],
            'normal': self.colors['tempo_normal'],
            'fast': self.colors['tempo_fast']
        }
        
        tempo_names = {
            'slow': 'SLOW TEMPO',
            'normal': 'NORMAL TEMPO',
            'fast': 'FAST TEMPO'
        }
        
        # Draw tempo box at top
        tempo_rect = (450, 50, 300, 60)
        pygame.draw.rect(self.screen, tempo_colors[self.current_tempo], tempo_rect)
        pygame.draw.rect(self.screen, self.colors['text'], tempo_rect, 3)
        
        # Draw tempo text
        tempo_text = self.font_medium.render(tempo_names[self.current_tempo], True, (0, 0, 0))
        tempo_text_rect = tempo_text.get_rect(center=(tempo_rect[0] + tempo_rect[2]//2, 
                                                    tempo_rect[1] + tempo_rect[3]//2))
        self.screen.blit(tempo_text, tempo_text_rect)
    
    def draw_instructions(self):
        """Draw gesture instructions"""
        instructions = [
            "CONDUCTING INSTRUCTIONS:",
            "RIGHT: WOODWIND || LEFT: STRINGS",
            "DOWN: PERCUSSION || UP: BASS",
            "FORWARD: Speed Up | BACKWARD: Slow Down", 
            "DOUBLE UP/DOWN: Reset Tempo"
        ]
        
        # Position instructions at bottom of screen
        y_start = self.height - 120
        for i, instruction in enumerate(instructions):
            color = self.colors['text'] if i > 0 else self.colors['active']
            text = self.font_small.render(instruction, True, color)
            text_rect = text.get_rect(center=(self.width//2, y_start + i * 25))
            self.screen.blit(text, text_rect)
    
    def draw_title(self):
        """Draw the main title"""
        title = self.font_large.render("DIGITAL SYMPHONY CONDUCTOR", True, self.colors['active'])
        title_rect = title.get_rect(center=(self.width//2, 25))
        self.screen.blit(title, title_rect)
    
    def update_display(self):
        """Main drawing function - call this every frame"""
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Draw all components
        self.draw_title()
        self.draw_tempo_display()
        
        # Draw circular orchestra
        for section_key, section_data in self.sections.items():
            self.draw_circle_section(section_key, section_data)
        
        self.draw_center_circle()
        self.draw_gesture_arrow()
        self.draw_instructions()
        
        # Update display
        pygame.display.flip()
    
    def handle_events(self):
        """Handle pygame events (like closing window)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def close(self):
        """Clean up pygame"""
        pygame.quit()