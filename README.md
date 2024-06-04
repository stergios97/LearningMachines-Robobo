# LearningMachines-Robobo
A project in the context of "Learning Machines" course.


Rules for all tasks:

# Submit your slides PDF, links to videos of the demos in simulation and hardware, and a link to your code.

The presentation should contain (in this order):

+ Simulation demo

+ Live Hardware demo (robot behavior must be interesting, e.g., a robot that repeatedly drives back and forth (displacing just a bit) may qualify as avoiding obstacles and being fast, but could this robot really be useful?)

+ Problem definition and motivation
+ Methodology
+ Experimental setup
+ Results (with plots) and discussion
+ Conclusions

Deadlines can be found on the Assignments page - there will be no tolerance for delays: 1 day of delay deducts 1 point of the grade, 2 days 2 points, and so on.

Individual component: each member must participate in presenting and, most importantly, in answering questions from the teacher or TA during/after the presentation. If the student does not demonstrate enough individual knowledge, their score for that assignment will be individually penalized according to what the supervisor finds suitable. 

 

This rule is for all tasks but task 0

+ Two extra slides at the end: 1) the contribution sheet describing the contribution of each team member and 2) a buddy-group summary describing what you learned from them.

 

====================================

 

Task 0 - System exploration

 

This is a preparation task, and it is not worth any points, but it is mandatory. This task is extremely important because what you learn and develop through it will be the starting point for the other tasks, which build up incrementally. 

Install the system using the tutorials on Canvas.
Design a very simple task and hard code a solution to solve it.
Example 1:the robot has to go straight until it senses any object getting near and then turn right without touching it.
Example 2: the robot has to go straight until it touches the wall, and then it goes backward.
It is recommended to use only infrared sensor for this task.
The robot must perform the task in both simulation and hardware.
Repeat the task with the robot X times.
Plot metrics related to what is being sensed by the robot, e.g., the activation of each sensor across time steps.
Analyze the reality gap: were sensing values different? How?
Report the main challenges you faced and how you tackled them.
Decide which control architecture and learning algorithm you will use.
Install all other libraries/resources necessary to get started next week.
 

Task 1 - Obstacle avoidance

 

Design/choose an environment with obstacles to be avoided (sorrowing walls must also be avoided).
You can use the environment models available in scenes/arena_obstacles.tttLinks to an external site., but you can also modify it or make your own.
Define the specific task/challenge, e.g., the robot should displace in the environment as further and as fast as possible with minimal collision.
 

 Task 2 - Foraging: find and approach an object

 

Design/choose an environment with “food” to be “eaten”, e.g., packages to be touched.
You can use the environment models available in scenes/arena_approach.tttLinks to an external site., but you can also modify them or make your own.
An auxiliary script for counting touched packages is available: food.luaLinks to an external site.
Your robot should learn to touch the largest number of packages per minute.
This task includes a competition:
There will be one winning group that will get one extra point for their final grade.
The winner group: the hardware robot collects the largest number of packages in the shortest period.
The verification of the results will be done by your supervisor during your presentation: The supervisor will start a countdown timer (3 minutes) and signal that you can run your script.
The supervisor will register how many packages were collected before the timer goes off.
 

Task 3 - Foraging: pushing an object to a location

 

Choose between the “easier” and the “harder” environment/task.
You can use the environment models available at scenes/arena_push_easy.ttt or scenes/arena_push_hard.tttLinks to an external site., but you can also modify them or make your own.
Your robot should learn to push the red object to the green area as fast as possible.
 
