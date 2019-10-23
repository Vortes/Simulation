# CS 111 Problem Set 6
# Simulating robots
#
# Name:
# Collaborators:
# Time:
 
import math
import random
 
import ps6_visualize
import matplotlib.pyplot as plt
 
# === Provided classes

"""
* _____________________
* POSITION SUPER CLASS! 
* ---------------------
"""
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
 
    def getX(self):
        return self.x
 
    def getY(self):
        return self.y
 
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.
 
        Does NOT test whether the returned position fits inside the room.
 
        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed
 
        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)
 
# === Problem 1
"""
* _________________
* ROOM SUPER CLASS!
* -----------------
"""
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.
 
    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clean_tile = []
        # raise NotImplementedError
    
    def cleanTileAtPosition(self, pos):
        point = (int(pos.getX()), int(pos.getY()))
        if point not in self.clean_tile:
            self.clean_tile.append(point)
        # raise NotImplementedError
 
    def isTileCleaned(self, m, n):
        position = [m,n]
 
        if position in self.clean_tile:
            return True
        else:
            return False
 
        raise NotImplementedError
    
    def getNumTiles(self):
        return self.width * self.height
        raise NotImplementedError
 
    def getNumCleanedTiles(self):
        return len(self.clean_tile)
        raise NotImplementedError
 
    def getRandomPosition(self):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        return Position(x, y)
        
 
    def isPositionInRoom(self, pos):
        if pos.x >= 0 and pos.x < self.width and pos.y >= 0 and pos.y < self.height:
            return True
        else:
            return False
 
"""
* __________________
* ROBOT SUPER CLASS!
* ------------------
"""
class Robot(object):
    """
    Represents a robot cleaning a particular room.
 
    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.
 
    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        self.room = room
        self.speed = speed
        self.direction = random.randint(0,365)
        self.position = room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)
        # raise NotImplementedError
 
    def getRobotPosition(self):
        return self.position
        # raise NotImplementedError
    
    def getRobotDirection(self):
        return self.direction
        # raise NotImplementedError
 
    def setRobotPosition(self, position):
        self.position = position
 
    def setRobotDirection(self, direction):
        self.direction = direction
 
    def updatePositionAndClean(self): 
        """
        Simulate the raise passage of a single time-step.
 
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """         
        raise NotImplementedError
 
 
# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.
 
    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
 
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.
  
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        new_position = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)

        if self.room.isPositionInRoom(new_position):
            self.setRobotPosition(new_position)            
            self.room.cleanTileAtPosition(new_position)
        else:
            self.setRobotDirection(random.randint(0, 359))
 
# === Problem 3
 
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.
 
    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.
 
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    mean = []
 
    for i in range(num_trials):
        anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        steps = 0
        room = RectangularRoom(width, height)
        robot = [robot_type(room, speed) for j in range(num_robots)]
 
    while (room.getNumCleanedTiles() / room.getNumTiles()) < min_coverage:
            steps += 1
            anim.update(room, robot)
            for k in robot:
                k.updatePositionAndClean()
            if (room.getNumCleanedTiles()/room.getNumTiles()) >= min_coverage:
                mean.append(steps)
                anim.done()
            else:
                continue
 
    return sum(mean)/len(mean)
 
 
print(runSimulation(3, 1.0, 15, 10, 1.0, 30, StandardRobot))
# === Problem 4
#
# 1) How long does it take to clean 80% of a 20◊20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#    20◊20, 25◊16, 40◊10, 50◊8, 80◊5, and 100◊4?
 
# def showPlot1():
#     """
#     Produces a plot showing dependence of cleaning time on number of robots.
#     """ 
#     raise NotImplementedError
 
# def showPlot2():
#     """
#     Produces a plot showing dependence of cleaning time on room shape.
#     """
#     raise NotImplementedError
 
# === Problem 5
 
# class RandomWalkRobot(Robot):
#     """
#     A RandomWalkRobot is a robot with the "random walk" movement strategy: it
#     chooses a new direction at random after each time-step.
#     """
#     raise NotImplementedError
 
 
# === Problem 6
 
# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
# def showPlot3():
#     """
#     Produces a plot comparing the two robot strategies.
#     """
#     raise NotImplementedError
 

