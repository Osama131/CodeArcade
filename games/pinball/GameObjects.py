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
        #ball properties
        self.radius = self.rect.w/2 #needed for collison
        self.position = pygame.Vector2(x,y) # represents the position from the ball center
        self.velocity = pygame.Vector2(0,0) # represents the velocity in x y vectors
        self.mass = 100 # needed for gravity
        self.bounciness = 0.7

        self.collided = False

        #point collision
        self.group = balls_Group #get the group the ball is in
        self.scoreObstacle_Group = scoreObstacle_Group # needed to check if points are earned


    #simulate gravity and movement
    def simulate(self, map_sprite, step_size,combinedMask,flippers):
        
        screen = pygame.display.get_surface() 
        tail = self.mask.to_surface(setcolor="red")
        tail.set_colorkey("black")
        screen.blit(tail,self.rect) #draw the red tail

        #the return value of the function
        earnedPoints = 0

        #handle collisions
        combinedMask.draw(flippers[0].mask,flippers[0].rect.topleft) #add flipper hitbox. can probably be optimized by only drawing on flipper button press 
        combinedMask.draw(flippers[1].mask,flippers[1].rect.topleft) #add flipper hitbox
        
        intersection = combinedMask.overlap_mask(self.mask,(self.position[0]-self.radius,self.position[1]-self.radius)) #get all collided pixel with the static objects in a new mask
        
        
        collisionAreaSize = intersection.count()
        if collisionAreaSize != 0: #if there is a collision
            intersectionPoint = intersection.centroid() # get the center of the collision to average out the point of contact
            

            if not self.collided: #if we are in the first frame of a collision
                
                for obstacle in self.scoreObstacle_Group: #check if collision brings points
                    if obstacle.rect.collidepoint(intersectionPoint):
                        earnedPoints += obstacle.score
                        self.velocity *= 1.5

                  
                
                
               
               
                mirrorVector = self.position - intersectionPoint  #draw vector from center of point to collision point.
                
                #print("MIRROR VECTOR:" + str(mirrorVector))
                #print ("MIRROR VECTOR MAGNITUDE:"+ str(pygame.Vector2.magnitude(mirrorVector)))
                
                
                self.velocity = self.velocity.reflect(mirrorVector) #mirror velocity around vector of circle center to collision point
                
                                     
                self.velocity *= self.bounciness #reduce magnitude to account for friction losses

                  
                #push away from collider. makes collision more reliable, but more inaccurate
                self.position += mirrorVector*0.1

                #stop more direction changed until hitbox was left
                self.collided = True
                
            else: #not first frame of collision
                pass
                
   
            intersection = None

        

        else:        
            self.collided = False
            self.velocity[1] += 0.2/step_size #increase velocity only when not in collision
        
        
        
        
        
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

#HACKATHON CHALLENGE 3
#complete the function.
#step_size refers to the simulation steps and is called 50 times per frame. Use this to get a smooth animation. 
# a and d are true when these buttons are pressed and are the triggers for the rotation of the flippers you need to implement.
# use the pygame functions for rotating an image
    def moveFlipper(self, step_size, a, d):
        
        screen = pygame.display.get_surface()

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
        self.rect.center = (x,y) #set position
        self.mask = pygame.mask.from_surface(self.image) #create collision mask from image
        self.score = score #the amount of point the target brings on a hit
        self.type = obstacleType #smallcircle,circle or rhombus (for showing points on screen)

