# TermProject

Community Immunity Simulation

This project creates a simulation of a virus spreading through a population. The user will enter several parameters regarding the virus before the simulation begins, including:
- a virus name, the user will enter text to name their virus
- a radius of infection, all healthy individuals within this radius of an infected person will become infected, similar to the 6 foot radius of COVID-19
- a population size
- transmissibility of the virus, the percent of healthy people within the radius of infection that will become infected
- a starting number of infected individuals
- a starting number of immunized individuals

After defining the parameters, the user presses the space bar and the simulation begins.
The simulation will show the virus spreading across the population over time and can be paused or made to continue any time. The user can click on a healhty person to vaccinate that person, or hold down and drag the mouse across multiple people to vaccinate them. Pressing the MUTATE! button pauses the simulation and generates a random mutation. This means that a random parameters of the virus will change. The user can then press play and see how the mutation has affected the simulation. Once there are no eligable individuals to infect, the simulation will stop and present a graph summary of the infection.

How to run:

Open the main.py file of the package. Ensure that CMU graphics are installed locally. Open the main.py file in VS code, and run the main file using 'command+B' on a Mac, or equivalent on a PC.

