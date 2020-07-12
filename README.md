# Link(Notion)

[https://www.notion.so/Formulation-f09ccda1675f40368ad4fb009dfab906](https://www.notion.so/Formulation-f09ccda1675f40368ad4fb009dfab906)

# Formulation

Created: Jul 10, 2020 9:33 AM

[https://whimsical.com/PABRrid4mdhYffUsKe2WnB](https://whimsical.com/PABRrid4mdhYffUsKe2WnB)

[https://whimsical.com/5U52qwR7ngGR3LtRdBhegC](https://whimsical.com/5U52qwR7ngGR3LtRdBhegC)

# Mediator $A$

[https://whimsical.com/RSH5BC9QEexM7EKXheLgNE](https://whimsical.com/RSH5BC9QEexM7EKXheLgNE)

- Let X be certain mediator like retail. Divide the range of $X$ into intervals $[x_{l1},\,x_{u1}),\,\ldots,[x_{lk},\,x_{uk})$.
- $A=X_1\times\ldots\times X_6$ has subsets $A_1,\ldots,A_k$

# Causal graphs

- Choose a country at random
- Given the selected country, sample a time period in a grouped_bin $i$
- The outcome is the mortality rates as in the original paper

# Assumptions

- Causal sufficiency

$$\begin{aligned}P(A\vert do(C)) &= P(A\vert C)\\P(M\vert do(A,C)) &=P(M\vert A,C)\end{aligned}$$

# Tables

[Case fatility rates by intervals](https://docs.google.com/spreadsheets/d/1D7kilZU6Nv_SWvKMQAZHUVDKu_4E9NJQPQdMqcG3cwU/edit?usp=drivesdk)

[percentage of confirmed in each group](https://docs.google.com/spreadsheets/d/1BDlk-PtLYiKYPmcXUm0Y8ZVUEf7uSUB-VBSqUcq2nqU/edit?usp=drivesdk)

# Formulas for NDE and NIE

# Total causal effect (TCE)

$$\begin{aligned}TCE_{UK->Belgium} &= E[M\vert do(C=Belgium)]-E[M\vert do(C=UK)]\\ &= \sum_a P(M=1\vert do(A=a, C=Belgium))\times P(A=a\vert do(C=Belgium))- \sum_a P(M=1\vert do(A=a, C=UK))\times P(A=a\vert do(C=UK))\\ &\stackrel{\text{causal sufficiency}}{=} \sum_a P(M=1\vert A=a, C=Belgium)\times P(A=a\vert C=Belgium)-\sum_a P(M=1\vert A=a, C=UK)\times P(A=a\vert C=UK)\\&=\text{difference of total CFRs reported in the last column of table 1}\end{aligned}$$

# Controlled direct effect (CDE)

$$\begin{aligned}CDE_{UK->Belgium}(a) &= E[M=1\vert do(C=Belgium, A=a)]-E[M=1\vert do(C=UK, A=a)] \\ &= P(M=1\vert do(C=Belgium, A=a))-P(M=1\vert do(C=UK, A=a)) \\ &\stackrel{\text{causal sufficiency}}{=} P(M=1\vert C=Belgium, A=a)-P(M=1\vert C=UK, A=a)\\ &=\text{difference of CFRs reported in column $a$ of table 1}\end{aligned}$$

# Natural Direct Effect (NDE)

$$\begin{aligned} NDE_{UK->Belgium} &= E_{A\vert C=UK}\Big[CDE_{UK->Belgium}(A)\Big] \\ &= \sum_{a}P(A=a\vert C=UK)\Big[P(M=1\vert A=a, C=Belgium)-P(M=1\vert A=a, C=UK)\Big]\end{aligned}$$

$P(A=a\vert C=UK)$ are all in table 3, $P(M=1\vert A=a, C=UK)$ are all in table 1.

# Natural Indirect Effect

$$\begin{aligned} NIE_{UK->Belgium} &= E\Big[M_{A=A_{Belgium}}\vert do(C=UK)\Big]-E\Big[M_{A=A_{UK}}\vert do(C=UK)\Big]\\ &= \sum_a\Big[P(A=a\vert do(C=Belgium))-P(A=a\vert do(C=UK))\Big]P(M=1\vert do(A=a,C=Belgium))\\ &\stackrel{\text{causal sufficiency}}{=} \sum_a \Big[P(A=a\vert C=Belgium)-P(A=a\vert C=UK)\Big]P(M=1\vert do(A=a,C=Belgium))\end{aligned}$$

# Subtractivity principle

Verify whether

$$TCE_{UK->Belgium}=NDE_{UK->Belgium}+NIE_{UK->Belgium}$$

If there is no equality then there is certain **moderation** happening

# Mediator selection (???)

- which one has the most impacts ? retail, grocery, residential, parks, workplaces, transit
- Combine several mediators in the position of **retail_bins —> (retail, workplaces)**
- compare rates across time ?
