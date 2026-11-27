# Reflection

## Challenges

Connecting the xArm to WSL proved difficult, so I switched to a virtual machine. The VM was easier to configure and use, but it provided fewer resources and examples for setting up the required packages. Some commands also required additional troubleshooting because relevant setup steps were missing or easy to overlook.

## Implementation

Creating the code that communicated with the xArm was straightforward because the previous assessment had already covered that area. Pygame required more research, particularly for loading and displaying images and for using a colour picker to determine the target-ring colours and score values.

Overall, this was an enjoyable project to design and build.

## Improvements

If I were to repeat the project, I would improve the scoring system. Instead of detecting a ring by its pixel colour, I would calculate distance from the centre of the target. This would avoid problems caused by text, such as the black `"10"` text covering part of the yellow ring.

I would also display an arrow or marker at the position of the most recent click. This would show the target location clearly and make the interface more interactive.

## Use of AI

I used AI assistance to help organise project files and improve documentation, including `README.md` and `ARCHITECTURE.md`. AI also helped set up and generate the package API documentation with pdoc.