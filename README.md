# Group 14 - Learning Machines Robobo

This is the GitHub repository for the Learning Machines course.

If you're a student, everything you need for the course itself is in the [examples](https://github.com/ci-group/learning_machines_robobo/tree/master/examples) directory. It contains all the documentation and code you need. Just clone this repository, cd into examples, and start at that readme, which will guide you through the whole thing.

### There is an issue/bug with the code.

If you find a problem with the code, please create an issue [here](https://github.com/ci-group/learning_machines_robobo/issues) on the GitHub repository. For this, please make sure you include these three things:

- Some example code with instructions on how to run and include it. This should preferably be a minimum failing example, just linking to your entire assignment won't cut it. You might think this is a lot of extra work, but the amount of times I personally found a bug in my own code by trying to construct an example like this is staggering. It's a really good test to make sure that what you think is happening is actually what is happening. Also, it helps whoever wants to fix it understand what is going wrong.
- The behaviour you would expect from this minimum failing example. No "it should work," be specific in what output you expect.
- The actual behaviour you observed, and that anyone can observe by running the example code you provided. Here, also provide the platform you ran it under, in case it cannot be reproduced.

## Contributing / maintaining

If you are working on the project, you should notice that all code you write yourself should be in `maintained/`. All code in the examples is automatically generated (or, well, copied over) from there. This architecture is quite weird, but I couldn't find a better option. Because everything is ROS, it is hard to distribute the individual packages without having to teach students how to install ROS packages, making the code too much of a black box. Alternatively, having only one template (e.g. only `full_project_setup`), which is what was here before, has issues with documentation, as that makes it quite a large project to just dump students into. With the way it currently is, everything is in one place while maintaining, but students can still cd from example to example to explore the codebase.

To work on the project, first, `cd` into maintained. Here, you can edit the code and test it, (though it might be easier to test it inside the directory of the relevant example.) Once you are confident it is good, you can type `python3 ./build.py`, this will copy all files over to the right examples. If you created new scripts or catkin packages, this build script is also where to make the needed changes to always copy over the files to the appropriate examples. The build script will ask for confirmation for every file it wants to delete. If you're confident everything is backed up, you can pass the `-y` flag to answer yes to all prompts.

After you have built, it is important to go through the READMEs in the examples, and assert all of them are still correct.

If you change anything with the docker setup or run scripts it is important to test everything under Linux (X11), Windows, and MacOS before pushing to master, making sure the behaviour is consistent.

If you changed the Lua scripts, make sure to update all affected models and scenes to match. This is quite tedious, and if you find a way to automate it, please let me know.


## Rules for all tasks:

## Submit your slides PDF, links to videos of the demos in simulation and hardware, and a link to your code.

## Link to the paper report in OverLeaf: 

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

## + Two extra slides at the end: 1) the contribution sheet describing the contribution of each team member and 2) a buddy-group summary describing what you learned from them.

 

====================================

 

## Task 0 - System exploration

 

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
 

## Task 1 - Obstacle avoidance

 

Design/choose an environment with obstacles to be avoided (sorrowing walls must also be avoided).
You can use the environment models available in scenes/arena_obstacles.tttLinks to an external site., but you can also modify it or make your own.
Define the specific task/challenge, e.g., the robot should displace in the environment as further and as fast as possible with minimal collision.
 

 ## Task 2 - Foraging: find and approach an object

 

Design/choose an environment with “food” to be “eaten”, e.g., packages to be touched.
You can use the environment models available in scenes/arena_approach.tttLinks to an external site., but you can also modify them or make your own.
An auxiliary script for counting touched packages is available: food.luaLinks to an external site.
Your robot should learn to touch the largest number of packages per minute.
This task includes a competition:
There will be one winning group that will get one extra point for their final grade.
The winner group: the hardware robot collects the largest number of packages in the shortest period.
The verification of the results will be done by your supervisor during your presentation: The supervisor will start a countdown timer (3 minutes) and signal that you can run your script.
The supervisor will register how many packages were collected before the timer goes off.
 

## Task 3 - Foraging: pushing an object to a location

 

Choose between the “easier” and the “harder” environment/task.
You can use the environment models available at scenes/arena_push_easy.ttt or scenes/arena_push_hard.tttLinks to an external site., but you can also modify them or make your own.
Your robot should learn to push the red object to the green area as fast as possible.
 
