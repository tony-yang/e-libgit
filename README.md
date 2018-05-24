# e-libgit
This is an experimental git core implementation for fun and for hacking some interesting ideas/questions I had about git and its relevant technologies.

## Goals
I previous worked with a team that managed git servers internally and there were problems that intrigued me. In particular, occasionally, we would experience lots of unicorns due to high server loads. This made me wonder about the scalability of the system. In addition, I was interested in the underlying implementation of git and was curious about its relationship with the more recent hype about blockchain. I decided to find out through a series of sub-goals:

- Implement a git core in both Python and Ruby in a similar fashion using the language's respective styling and idiom, and compare their performance. (Though libgit2 is C native with language binding, it will be interesting to see what the performance difference might be. Of course, my implementation might be naive but I'm just curious. I will not implement the entire system as in libgit2 so this might not be a fair comparison. But at least I can compare between my implementation in Python and Ruby)
- How does the git's commit hash chain different from the blockchain technology? Preliminary research said they are both based on the Merkel tree and there are some differences but I want to dig deeper.
  - Follow up: if they are different, does it hold any merit to implement git using blockchain and for what purpose?
- How to distribute the git server and make it even more scalable and highly available so that it could handle loads (perhaps misused load such as large binary objects) as seen in my previous work? Does it hold any merit to use distributed hashing strategy over the current cluster mirror strategy (both active-active and active-slave)?

## Just a Self Reminder
Use libgit2 if you are serious about implementing some kind of real or toy application based on git core :p

## References
Some very useful explanation of git core videos that inspired this project:
https://www.youtube.com/watch?v=MYP56QJpDr4
https://www.youtube.com/watch?v=ig5E8CcdM9g
https://www.youtube.com/watch?v=P7n6G2IL6eo
