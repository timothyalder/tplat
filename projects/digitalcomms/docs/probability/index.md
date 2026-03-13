# Communication Channel, Probability, and Random Variables

Communication channels are imperfect. Their impact on a signal is stochastic - i.e., it cannot be predicted in a deterministic manner. Instead, random variables and random processes are used to characterise the behaviour of the system.

## Random Experiment

**Random experiment:** an experiment whose outcome cannot be predicted - e.g., flipping a coin, rolling a dice, etc.

**Sample space:** the set of all possible outcomes of a random experiment - e.g., $\Omega = \{1, 2, 3, 4, 5, 6\}$ for rolling a dice.

## Probability

Probability describes the likelihood of any event occurring when conducting a random experiment.

The probabilities of all outcomes in a random experiments sample space form the probability distribution function (PDF). The sum of these probabilities (i.e., the integral of the PDF) must equal one.

Probability is denoted by $Pr$ or $P$.

## Random Variables

A random variable (RV) is a mapping from the sample space of a random experiment to a set of real numbers - i.e., it is a function that assigns each outcome in the sample space to a real number.

There are many different mappings given the same sample space. For example, when rolling a dice you may have the mapping $\{`1',`3',`5'\} \mapsto \{0\}$ and $\{`2',`4',`6'\} \mapsto \{1\}$.

RVs must obey the following rules:
* the entire mapping must encompass the entire sample space;
* each outcome of the sample space should only be assigned to one number (or symbol).

RVs are typically denoted by capital letters - e.g., $X$.

$Pr(X=x)$ indicates the probability random variable $X$ takes on the value $x$.

### Discrete Random Variables

A discrete RV can take on values from a finite or countably infinite set of numbers (e.g., the points scored in a game).

### Continuous Random Variables

A continuous RV can take on values from an interval of real numbers (e.g., the volume of water in a container).