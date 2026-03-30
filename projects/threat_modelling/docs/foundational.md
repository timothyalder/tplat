# Foundational

Everybody threat models. For example, when you leave your parked car you lock the door and hide your valuables. This decision is derived from a subconcious action of threat modelling whereby you consider where your car is parked and what threats it may face (i.e., somebody breaking in). When your car is parked in secure garage, you might not think it necessary to hide your valuables. But when your car is parked on a secluded street in a sketchy part of town, your threat model is probably different and, thus, so is the precautions that you take.

Threat modelling will often identify threats that cannot be effectively mitigated. Alas, it is better to be uncomfortably aware than blissfully ignorant. Effective threat modelling creates a more secure product by managing the intersection of attacks, mitigations, and requirements.

## Why Threat Model?

In the context of product design, threat modelling offers several advantages; namely:

* find security bugs early;
* understand your security requirements;
* engineer and deliver better products;
* and address issues other techniques won't.

Adam Shostack makes a notable comparison between threat modelling and version control, whereby he postulates that threat modelling should be treated as a fundamental skill (not a specialist discipline), much the same as familiarity with a version control system (e.g., Git) is a fundamental skill for a software developer.

## Threat Modelling in Four Steps

Threat modelling can be broken down into four key questions:

1. What are you building?
2. What can go wrong with it once it's built?
3. What should you do about those things that can go wrong?
4. Did you do a decent job of analysis?

These questions resolve to the following four activities:

1. Model the system you're building, deploying, or changing.
2. Find threats using that model in conjunction with formal threat identification techniques (e.g. [Stride](identify/index.md)).
3. Address threats using formal threat mitigation techniques.
4. Validate your work for completeness and effectiveness.

## Do NOT "Think Like an Attacker"

A common pitfall in threat modelling is to, "think like an attacker". This can lead to implicit or incorrect assumptions about how an attacker will think and what they will choose to do. This strategy does not help most people threat model.

## Threat Modelling vs Risk Analysis

There is a great deal of overlap between threat modelling and risk analysis. The primary distinction to keep in mind is that threat modelling is a pragmatic activity focused on quickly and informally identifying threats and choosing mitigations.

Risk analysis is a more formal discipline focused on evaluating likelihood weighted by impact, often using quantitative structured methods, to prioritise risks and justfiy decisions -- especially in governance, compliance, or enterprise risk contexts.

Basically, risk analysis goes deeper on justification, prioritisation, and often quantification, whereas threat modelling is typically more design and engineering-oriented.
