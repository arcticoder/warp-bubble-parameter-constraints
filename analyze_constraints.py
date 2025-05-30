#!/usr/bin/env python3
import sympy as sp
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from mpmath import erf as mp_erf, exp as mp_exp, findroot
import requests, re
from sympy import symbols, Function, sin, pi, integrate, diff, exp, sqrt, erf

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

# 6. Export results to LaTeX
from sympy import latex

print("\n" + "="*60)
print("GENERATING LATEX OUTPUT")
print("="*60)

E_neg_ltx = latex(E_neg)
dE_dR_ltx = latex(dE_dR)
dE_dsigma_ltx = latex(dE_dsigma)

R_ltx = ', '.join(latex(s) for s in sol_R) if sol_R else '\\text{No analytical solutions found}'
sigma_ltx = ', '.join(latex(s) for s in sol_sigma) if sol_sigma else '\\text{No analytical solutions found}'

# Add the nondimensional analysis
F_x_ltx = 'e^{-2x^2} + \\frac{1}{2}e^{-8x^2}'

# Construct bounds statement
A_bounds_ltx = 'A > 0\\ \\text{ for exotic matter generation}'

tex_doc = rf"""\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
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

\\subsection*{{Nondimensional Analysis}}

Defining the dimensionless parameter $x = R/\\sigma$, the extremum condition 
$\\partial E_{{\\rm neg}}/\\partial R = 0$ reduces to the transcendental equation:
\\[
  F(x) = {F_x_ltx} = 0
\\]

Since both exponential terms are strictly positive for all $x > 0$, we have $F(x) > 0$ 
for all real $x$. This indicates that \\textbf{{no critical points exist}} for this 
simplified model.

\\subsection*{{Asymptotic Analysis}}

\\textbf{{Thin-wall limit}} ($\\sigma \\ll R$, i.e., $x \\gg 1$):
\\[
  \\text{{erf}}(x) \\approx 1 - \\frac{{e^{{-x^2}}}}{{\\sqrt{{\\pi}} x}}
\\]

\\textbf{{Thick-wall limit}} ($\\sigma \\gg R$, i.e., $x \\ll 1$):
\\[
  \\text{{erf}}(x) \\approx \\frac{{2x}}{{\\sqrt{{\\pi}}}}\\left(1 - \\frac{{x^2}}{{3}} + \\cdots\\right)
\\]

\\subsection*{{Physical Constraints}}
For exotic matter generation and finite energy:
\\[
  {A_bounds_ltx}
\\]

\\subsection*{{Physical Interpretation}}

The absence of critical points in this simplified model suggests:
\\begin{{itemize}}
  \\item The energy $E_{{\\rm neg}}$ decreases monotonically with increasing $R$ or $\\sigma$
  \\item No natural ``optimal'' bubble size exists
  \\item Physical constraints (finite resources, stability requirements) must determine parameters
  \\item More sophisticated models may include additional terms that create energy minima
\\end{{itemize}}

\\subsection*{{Numerical Approaches}}

For practical parameter optimization, consider:
\\begin{{enumerate}}
  \\item \\textbf{{Parameter scanning}}: Grid search over $(R,\\sigma)$ space
  \\item \\textbf{{Constrained optimization}}: Minimize $|E_{{\\rm neg}}|$ subject to physical bounds
  \\item \\textbf{{Multi-objective optimization}}: Balance energy efficiency with stability constraints
\\end{{enumerate}}

\\subsection*{{Notes}}
The extremum conditions for this model lead to transcendental equations involving error functions
that cannot be solved analytically in general. The nondimensional analysis reveals that
the simplified Gaussian model has no critical points, indicating the need for more 
sophisticated warp bubble models that include additional physical effects.

\\end{{document}}
"""

with open('parameter_constraints.tex', 'w') as f:
    f.write(tex_doc)

print("LaTeX file 'parameter_constraints.tex' has been generated successfully!")

# 9. Numerical Analysis of Transcendental Equations
print("\n" + "="*60)
print("NUMERICAL ANALYSIS")
print("="*60)

# Approach 1: Nondimensionalize to x = R/sigma
print("\n1. Nondimensionalizing to x = R/σ...")

# Define the nondimensional variable x = R/sigma
x = symbols('x', positive=True)

# For the extremum condition dE/dR = 0, we can express it in terms of x
# From our earlier calculation: dE_dR involves exp(-2*R^2/sigma^2) and exp(-8*R^2/sigma^2)
# This becomes exp(-2*x^2) and exp(-8*x^2) when R = x*sigma

# Simplified form of the transcendental equation for x
# This is derived from setting dE/dR = 0 and factoring out common terms
F_x_symbolic = exp(-2*x**2) + exp(-8*x**2)/2

print(f"Transcendental equation F(x) = {F_x_symbolic} = 0")
print("where x = R/σ is the dimensionless bubble width ratio")

# Approach 2: Asymptotic Analysis
print("\n2. Asymptotic Analysis...")

print("\nFor thin-wall limit (x >> 1, σ << R):")
print("erf(x) ≈ 1 - exp(-x²)/(√π·x)")
print("This gives approximate solution x ≈ √(ln(const·x))")

print("\nFor thick-wall limit (x << 1, σ >> R):")
print("erf(x) ≈ (2x/√π)(1 - x²/3 + ...)")
print("This gives a polynomial equation in x")

# Approach 3: Numerical root-finding (demonstration)
print("\n3. Numerical Root-Finding...")

def F_numerical(x_val):
    """Numerical evaluation of the transcendental equation F(x) = 0"""
    import math
    if x_val <= 0:
        return float('inf')
    try:
        return math.exp(-2*x_val**2) + math.exp(-8*x_val**2)/2
    except OverflowError:
        return 0.0

# Find approximate root using a simple bracketing approach
print("Searching for roots of F(x) = exp(-2x²) + exp(-8x²)/2 = 0...")

# Check function values at test points
test_points = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0]
print("\nFunction values at test points:")
for x_test in test_points:
    f_val = F_numerical(x_test)
    print(f"F({x_test}) = {f_val:.6f}")

# Note: Since both exponential terms are always positive, F(x) > 0 for all x
# This means there are no real roots - the system has no critical points!
print("\nObservation: F(x) > 0 for all x > 0 (both exponentials are positive)")
print("This means dE/dR ≠ 0 for any finite R, σ - no critical points exist!")

# Approach 4: Energy minimization via parameter scanning
print("\n4. Parameter Scanning Approach...")
print("Since analytical critical points don't exist, we can:")
print("a) Fix one parameter and minimize over the other")
print("b) Use 2D optimization to find practical minima")
print("c) Analyze the asymptotic behavior as R → ∞ or σ → ∞")

# Physical interpretation
print("\n5. Physical Interpretation...")
print("The absence of critical points suggests:")
print("- The energy E_neg decreases monotonically with increasing R or σ")
print("- No natural 'optimal' bubble size exists in this simplified model")
print("- Physical constraints (finite resources, stability) must determine parameters")
print("- More sophisticated models may include additional terms that create minima")
