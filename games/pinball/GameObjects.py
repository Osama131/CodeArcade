import pygame


class Ball(pygame.sprite.Sprite):
    #pImage is the Surface/Image.
    def __init__(self, pImage, x, y, scoreObstacle_Group, balls_Group):
        super().__init__()
        
        self.initialPosition = (x,y)#needed for debugging purposes
        #ball rendering
        self.image = pImage
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.mask = pygame.mask.from_surface(self.image)
        self.biggerMask = self.mask.scale((self.mask.get_size()[0]*1.5,self.mask.get_size()[1]*1.5))
        #ball properties
        self.radius = self.rect.w/2 #needed for collison
        self.position = pygame.Vector2(x,y) # represents the position from the ball center
        self.velocity = pygame.Vector2(0,0) # represents the velocity in x y vectors
        self.mass = 100 # needed for gravity
        self.bounciness = 0.8

        self.collided = False

        #point collision
        self.group = balls_Group #get the group the ball is in
        self.scoreObstacle_Group = scoreObstacle_Group # needed to check if points are earned


    #simulate gravity and movement
    def simulate(self, map_sprite, step_size,combinedMask,flippers, pressed_a, pressed_d):
        #DEBUG draw hitbox
        screen = pygame.display.get_surface()
        ballCollisionSurface = self.mask.to_surface(setcolor="red")
        ballCollisionSurface.set_colorkey("black")
        screen.blit(ballCollisionSurface,self.rect) #draw tail of ball

        #the return value of the function
        earnedPoints = 0

        #handle collisions
        if not pressed_a: #check if button pressed to not check for collision on press to avoid weird behaviour 
            combinedMask.draw(flippers[0].mask,flippers[0].rect.topleft) #add flipper hitbox. can probably be optimized by only drawing on flipper button press 
        if not pressed_d:
            combinedMask.draw(flippers[1].mask,flippers[1].rect.topleft) #add flipper hitbox
        
        intersection = combinedMask.overlap_mask(self.mask,(self.position[0]-self.radius,self.position[1]-self.radius)) #get all collided pixel with the static objects in a new mask
        
        
        
        if intersection.count() != 0: #if there is a collision
            intersectionPoint = intersection.centroid() # get the center of the collision to average out the point of contact
            
            #debug show hit mask element
            

            if not self.collided: #if we are in the first frame of a collision
                


                for obstacle in self.scoreObstacle_Group: #calculate points earned on a collision
                    if obstacle.rect.collidepoint(intersectionPoint):
                        earnedPoints += obstacle.score
                        self.velocity *= 1.3 #creates a mask for the hit component
                        hitted_surface = obstacle.mask.to_surface(setcolor="green")
                        hitted_surface.set_colorkey("black")
                        screen.blit(hitted_surface,(obstacle.rect.x,obstacle.rect.y))

                
                #print("Intersection point:" + str(intersectionPoint))
                #print("Own position on Map" + str(self.screenToMapCoords(self.position,map_sprite)))

                #draw vector from center of point to collision point.
                mirrorVector = self.position - intersectionPoint
                #print("MIRROR VECTOR:" + str(mirrorVector))
                #print ("MIRROR VECTOR MAGNITUDE:"+ str(pygame.Vector2.magnitude(mirrorVector)))
                #mirror velocity around vector of circle center to collision point
                self.velocity = self.velocity.reflect(mirrorVector)
                
                                     
                self.velocity *= self.bounciness #reduce magnitude to account for friction losses

                  
                #push away from collider. makes collision more reliable, but more inaccurate
                self.position += mirrorVector*0.05

                #stop more direction changed until hitbox was left
                self.collided = True
                
            else: #not first frame of collision
                pass
                
   
            intersection = None

        

        else:        
            self.collided = False
            self.velocity[1] += 0.3/step_size #increase velocity only when not in collision
        
        
        
        
        
        #handle general movement 
        self.position += self.velocity/step_size
        self.rect.center = self.position
        
        #remove flipper hitbox to allow redrawing next frame
        combinedMask.erase(flippers[0].mask,flippers[0].rect.topleft) #add flipper hitbox 
        combinedMask.erase(flippers[1].mask,flippers[1].rect.topleft) #add flipper hitbox
        
        
        return earnedPoints

    #adds the power vector to the velocity vector
    def addImpulse(self,powerVector):
        self.velocity+=powerVector

        

        
class Flipper(pygame.sprite.Sprite):
    def __init__(self, pImage, x, y, direction):
        super().__init__()
        self.image = pImage
        self.img_copy = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.degree = 0
        self.max_angle = 45
        self.mask = pygame.mask.from_surface(self.image)

    def moveFlipper(self, step_size, a, d):
        
        screen = pygame.display.get_surface()
        #screen.blit(self.mask.to_surface(setcolor="red"),self.rect)

        degree_before = self.degree
        if (a and self.direction == "left" or d and self.direction == "right") and self.degree < self.max_angle:
            self.degree += 15/step_size
        if (not a and self.direction == "left" or not d and self.direction == "right") and self.degree > 0:
            self.degree -= 15/step_size

        if not degree_before == self.degree:#für performance
            deg = self.degree if self.direction == "left" else -self.degree
            self.image = pygame.transform.rotate(self.img_copy, deg)
            self.rect = self.image.get_rect(center = self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)
        return

class Board(pygame.sprite.Sprite):
    def __init__(self, pImage, x, y):
        super().__init__()
        self.image = pImage
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.mask = pygame.mask.from_surface(self.image) #create collision mask from image

class ScoreObstacle(pygame.sprite.Sprite):
    def __init__(self, pImage, x, y, score, obstacleType):
        super().__init__()
        self.image = pImage
        self.rect = self.image.get_rect() # get rect for position
        self.rect.topleft = (x,y) #set position
        self.mask = pygame.mask.from_surface(self.image) #create collision mask from image
        self.score = score #the amount of point the target brings on a hit
        self.type = obstacleType  # smallcircle,circle or rhombus (for showing points on screen)

