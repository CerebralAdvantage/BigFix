# BigFix
"building a better perceptron"

BigFix is a work in progress.  I started working on this in 2018, with an eye toward BigInt fractions.  It seemed fraught, due to the need of "GCD" details.
In 2023, I resumed working toward a solution. \
Two weeks ago (June 22 2024) I switched from fractions to fixed point math, which, considerring how incredibly well python and numpy were designed, has been a rocket sled.  Today (2024-07-08) I am committing BigFix.py, which has gone very far toward being a general purpose "extreme precision" fixed point plug-n-play class. \
My high hope is to seamlessly (as much as possible) interface with all of the latest modern ML tools, slowing them down dramatically!  (It's a trade-off... speed for a precision that IEEE float (even float128) will not apprach.) This should make for much more precise hurricane prediction, aid in the early recognition of cancer, all the things we wish ML might do a little more precisely. \
I have more to do to get everything to work together, but the closer I get, the more joy I experience in the process.

Thank you, Python!  Thank you, Guido!
James Huddle 2024-07-08

Details to follow...
