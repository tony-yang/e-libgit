# e-libgit
This is an experimental git core implementation for fun and for hacking some interesting ideas/questions I had about git and its relevant technologies.

## Goals
I was interested in the underlying implementation of git and its distributed nature, and I was curious about its relationship with the recent hype about blockchain. Here is a list of goals that I want to achieve or questions that I want to answer through this project:

- Implement a git core in both Python and Ruby in a similar fashion using the language's respective styling and idiom, and compare their performance.
- How does the git's commit hash chain differs from the blockchain technology? Preliminary research suggested that they are both based on the Merkel tree and there are some differences but I want to dig deeper.
  - Follow up question: if they are different, does it hold any merit to implement git using blockchain and for what purpose?
- How to distribute the git server and make it even more scalable and highly available so that it could handle very large load (or perhaps misused load such as committing large binary objects)? Does it hold any merit to use distributed hashing strategy over the current cluster mirror strategy (both active-active or active-slave disk RAID/DRBD) or DGit?

## Dev Guide
After repo checkout, the Python git is under the `py_libgit` directory. The Ruby git is under the `ruby_libgit`. Each version has its own Makefile and setup. There is a master Makefile that builds the container and runs the tests from each directory. After change just run `make` from the top level directory.

## Just a Self Reminder
Use libgit2 if you are serious about implementing some kind of real or toy application based on git core :p

## References
Some very useful explanation of git core videos that inspired this project:
https://www.youtube.com/watch?v=MYP56QJpDr4
https://www.youtube.com/watch?v=ig5E8CcdM9g
https://www.youtube.com/watch?v=P7n6G2IL6eo
