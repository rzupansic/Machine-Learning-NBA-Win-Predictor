# Machine Learning NBA Win Predictor
As a huge fan of basketball and sports betting becoming more and more relevant for the NBA, I decided to pursue this project to try and increase the odds of predicting the outcome of an NBA game.

This ML model is created with **Python** and **Tensorflow**, an open-source Machine Learning platform.

The original dataset used for this model is Neil-Paine-1's elo dataset.
This can be found here: https://github.com/Neil-Paine-1/NBA-elo

Using this dataset, I peformed a great deal of feature engineering so that only the most important features were used in training this model. The following sections will explain each feature and why it was used.

# ELO
The ELO rating system is a method for calculating the relative skill levels of players in zero-sum games such as chess. It is named after its creator Arpad Elo, a Hungarian-American physics professor. 

This rating system can be translated to sports as well, where a team or player's ELO rating is a number which may change depending on the outcome of rated games played.
A rating of 1500 is approximately average, although the league average can be slightly higher or lower depending on how recently the league has expanded. With every game played, the outcome of the game will add or subtract from this rating.

ELO ratings have historically shown to affect a team's win probability. More information and an interactive chart can be found here: https://projects.fivethirtyeight.com/complete-history-of-the-nba/#warriors

# AVERAGE PTS SCORED OF LAST 5 GAMES
This feature will average the last five games of each team to compare their scoring outputs. With all the randomness that sports brings, generally if a team has been killing every opponent and averaging 140 ppg, we can say with a higher confidence that said team would win against a team averaging 90 ppg. 

There are plenty of other factors like points allowed, average +/-, etc. that could affect the outcome as well and would be considered in future updates.

# Back-to-Backs
This feature refers to if the team played a game the previous day. This can take a toll on the players if they have not recovered enough from the previous game, especially if the team had to travel to another city between these games.
In recent years, star players would occasionally rest these consecutive games which could affect their team's probability of winning. Fans have protested this idea on many occasions and as a result, the league now has rules in place to penalize those who rest.

Regardless of if the star players play or rest, back-to-backs have shown to still affect the performance of teams. 

More information can be found here: https://medium.com/@kevhopper92/analyzing-the-impact-of-back-to-backs-on-nba-team-performance-88a4b80a5d99

