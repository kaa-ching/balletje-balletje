= BALLETJE-BALLETJE

I want to re-create a game from the 80's, but in a modern fashion.
The original game, 'balletje-balletje' was written bij John DRJ Vanderaert for the C64.

In the past, I have created an MSX version in assembly and an Amiga version in C.

The new version should be using pygame, in a 1920x1080 screen.

== Game idea

The basic game is the 'sham game', i.e. we have three cups that shuffle a ball.
At the end of the shuffling, the user is asked to tell where the ball is.

== Game backdrop and layout

During the entire game, there's moving backdrop.
It's geometric, repeating and slightly hypnotic.

Depending on where we are in the game, it is moving down or up, or moving towards one of the corners.

I want to have space for a 100px border surrounding the play field.

At the bottom of the screen (reserve 150px), there is a message bar. It should contain the messages
like "press space bar", "click on the cup" and others.

The cups consist of a brown rounded square, slightly larger than the ball.
The cups should each display the text "CooTV" in a darker brown in the center of the cup.

== Technology

I want the game to be object-oriented.
I expect a 'cup' class that knows if it has a ball and knows how to move from one to the next position.

== Debugging

While developing, I'd like to see a number in the top-left corner of the cup, with a * if that cup contains the ball.

== Game States

We have:

* a Start screen, displaying "balletje-\nballetje" (thus in 2 lines) in large italic letters in the center.
  the message bar should displace "press SPACE to start" and indeed wait for the space key.
* the start text moves up, off screen. It is replaced by a ball, randomly, in one of three locations (left middle right).
  once the ball is visible, the message bar should again display the SPACE text.
* the cups move in from the top of the screen and hide the ball. At this point, the cup should register if it hids the ball or not, the ball itself should be hidden.

Let's stop here, for now.
