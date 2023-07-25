import pygame 

class PysicsEngine2D:

    COLLISION_TOLERANCE = 10
    
    def __init__(self,game):
        self.running = True
        # Motor gráfico
        self.game_engine = game.game_engine
        self.screen = game.screen
        
        self.width, self.height = game.WIN_SIZE
        
        # Elementos que irao ser desenhados na tela
        self.moving_rect = self.game_engine.Rect(100,100,100,100)
        
        self.static_rect = self.game_engine.Rect(300,300,100,100)

        self.x_speed, self.y_speed = 5, 4
        
        self.other_speed = 2
        
    def update(self):
        """
        Loop principal
        """
        # Verificando se ha colissao
        if self.aabb_colision(self.moving_rect.x,self.moving_rect.y,self.moving_rect.width,self.moving_rect.height,self.static_rect.x,self.static_rect.y,self.static_rect.width,self.static_rect.height):
            self.collision_side()

        self.border_collision()
        
        self.draw()
       
    def draw(self):
        self.screen.fill((255,255,255))

        self.game_engine.draw.rect(self.screen,(0,0,0),self.moving_rect)
        self.game_engine.draw.rect(self.screen,(255,0,0),self.static_rect)
        # aplicando alteracoes
        self.game_engine.display.flip()
    
    def border_collision(self):
        
        # Fazendo o retangulo se movimentar horizontalmente
        self.moving_rect.x += self.x_speed
        # Fazendo o retangulo se movimentar verticalmente
        self.moving_rect.y += self.y_speed
        # Fazendo o retangulo se movimentar verticalmente
        self.static_rect.y += self.other_speed

        # Colisao com a borda
        if self.moving_rect.right >= self.width or self.moving_rect.left <= 0:
            self.x_speed *= -1
        if self.moving_rect.bottom >= self.height or self.moving_rect.top <= 0:
            self.y_speed *= -1

        # Colisao do retangulo em movimento com a borda do topo e de baixo
        if self.static_rect.bottom >= self.height or self.static_rect.top <= 0:
            self.other_speed *= -1
    
    @staticmethod
    def aabb_colision(A_x,A_y,A_width,A_height,B_x,B_y,B_width,B_height):
        # Axis Aligned Bounding box aabb
    
        # Apenas verifica se colidiu
        x_collision = A_x < B_x + B_width and A_x + A_width > B_x
        y_collision = A_y < B_y + B_height and A_y + A_height > B_y
        
        return x_collision and y_collision
    
    def collision_side(self):
            # Bug: Os retângulos precisam ser do mesmo tamanho para funcionar 
            
            # Se parte do topo do retângulo tiver a mesma cordenada que a parte de baixo de outro retângulo, então houve uma colissao
            # Mas não consigo entender porque é maior do que 0, as vezes 15, as vezes 10, deveria ser sempre 0 uma colisão perfeita.
            # Talvez seja uma questão lentidão para calcular a colisão

            # Bottom collision
            if abs(self.static_rect.top - self.moving_rect.bottom) < self.COLLISION_TOLERANCE and self.y_speed > 0:
                self.y_speed *= -1
                return 1
            # Top collison
            if abs(self.static_rect.bottom - self.moving_rect.top) < self.COLLISION_TOLERANCE and self.y_speed < 0:
                self.y_speed *= -1
                return 2
            # Left collision
            if abs(self.static_rect.right - self.moving_rect.left) < self.COLLISION_TOLERANCE and self.x_speed < 0:
                self.x_speed *= -1
                return 3
            # Right collision
            if abs(self.static_rect.left - self.moving_rect.right) < self.COLLISION_TOLERANCE and self.x_speed > 0:
                self.x_speed *= -1
                return 4


