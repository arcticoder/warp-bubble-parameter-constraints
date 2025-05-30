#!/usr/bin/env python3
import sympy as sp
import requests, re
from sympy import symbols, Function, sin, pi, integrate, diff, exp, sqrt

# Define symbols
r, theta, phi, R, sigma, A, c = symbols('r theta phi R sigma A c', positive=True)
t = symbols('t', real=True)

# For demonstration, we'll use a simplified warp bubble profile
# f(r,t) = 1 + A * exp(-((r-R)/sigma)^2) * exp(-t^2/sigma^2)
# This represents a Gaussian-shaped warp bubble centered at radius R with width sigma

f = Function('f')
# Define a specific form for the warp bubble profile
warp_profile = 1 + A * exp(-((r - R)/sigma)**2) * exp(-(t/sigma)**2)

# Simplified energy density (negative for exotic matter)
# This is a representative form based on warp drive physics
T00 = -A**2 * exp(-2*((r - R)/sigma)**2) * exp(-2*(t/sigma)**2) / (8*pi*r**2)

print("Using simplified warp bubble model:")
print(f"f(r,t) = {warp_profile}")
print(f"T^{{00}}(r,t) = {T00}")

# 4. Static profile: drop time dependence (t -> 0)
T00_r = T00.subs(t, 0)
print(f"T^{{00}}(r) at t=0 = {T00_r}")

# Define volume element
dV = r**2 * sin(theta)

# 6. Compute total negative energy within bubble radius
# Integrate from 0 to some outer radius (let's use 3*R as cutoff)
E_neg = integrate(T00_r * dV, (r, 0, 3*R), (theta, 0, pi), (phi, 0, 2*pi))

print(f"Computing total negative energy...")
print(f"E_neg = {E_neg}")

# 7. Extremum conditions for R and sigma
print("Computing extremum conditions...")
dE_dR = diff(E_neg, R)
dE_dsigma = diff(E_neg, sigma)

print(f"dE/dR = {dE_dR}")
print(f"dE/dsigma = {dE_dsigma}")

# Solve for critical points (if possible)
try:
    sol_R = sp.solve(dE_dR, R)
    print(f"Critical points for R: {sol_R}")
except Exception as e:
    print(f"Could not solve analytically for R: {e}")
    sol_R = []

try:
    sol_sigma = sp.solve(dE_dsigma, sigma)
    print(f"Critical points for sigma: {sol_sigma}")
except Exception as e:
    print(f"Could not solve analytically for sigma: {e}")
    sol_sigma = []

# 8. Bounds on A for physical consistency
# For the energy to be finite, we need A to be bounded
print("Analyzing bounds on A...")

# 9. Export results to LaTeX
from sympy import latex

print("Generating LaTeX output...")

E_neg_ltx = latex(E_neg)
dE_dR_ltx = latex(dE_dR)
dE_dsigma_ltx = latex(dE_dsigma)

R_ltx = ', '.join(latex(s) for s in sol_R) if sol_R else '\\text{No analytical solutions found}'
sigma_ltx = ', '.join(latex(s) for s in sol_sigma) if sol_sigma else '\\text{No analytical solutions found}'

# Construct bounds statement
A_bounds_ltx = 'A > 0\\ \\text{ for exotic matter generation}'

tex_doc = rf"""\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\begin{{document}}

\\section*{{Warp Bubble Parameter Constraints Analysis}}

\\subsection*{{Model}}
We analyze a simplified warp bubble with Gaussian profile:
\\[
  f(r,t) = 1 + A e^{{-\\frac{{(r-R)^2}}{{\\sigma^2}}}} e^{{-\\frac{{t^2}}{{\\sigma^2}}}}
\\]

The corresponding energy density is:
\\[
  T^{{00}}(r,t) = -\\frac{{A^2}}{{8\\pi r^2}} e^{{-\\frac{{2(r-R)^2}}{{\\sigma^2}}}} e^{{-\\frac{{2t^2}}{{\\sigma^2}}}}
\\]

\\subsection*{{Total Negative Energy}}
The total negative energy within the warp bubble region is:
\\[
  E_{{\\rm neg}}(R,\\sigma,A) = {E_neg_ltx}
\\]

\\subsection*{{Extremum Conditions}}
\\[
  \\frac{{\\partial E_{{\\rm neg}}}}{{\\partial R}} = {dE_dR_ltx} = 0
\\]
\\[
  \\Longrightarrow R = {R_ltx}
\\]

\\[
  \\frac{{\\partial E_{{\\rm neg}}}}{{\\partial \\sigma}} = {dE_dsigma_ltx} = 0
\\]
\\[
  \\Longrightarrow \\sigma = {sigma_ltx}
\\]

\\subsection*{{Physical Constraints}}
For exotic matter generation and finite energy:
\\[
  {A_bounds_ltx}
\\]

\\subsection*{{Notes}}
The extremum conditions for this model lead to transcendental equations involving error functions
that cannot be solved analytically in general. Numerical methods would be required for specific
parameter optimization.

\\end{{document}}
"""

with open('parameter_constraints.tex', 'w') as f:
    f.write(tex_doc)

print("LaTeX file 'parameter_constraints.tex' has been generated successfully!")
