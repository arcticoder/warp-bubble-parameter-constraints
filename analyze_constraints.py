#!/usr/bin/env python3
import sympy as sp
import requests, re
from sympy import symbols, Function, sin, pi, integrate, diff
from sympy.parsing.latex import parse_latex

# 1. Fetch LaTeX source of exotic-matter density
URL = "https://raw.githubusercontent.com/arcticoder/warp-bubble-exotic-matter-density/refs/heads/main/exotic_matter_density.tex"
resp = requests.get(URL)
text = resp.text

# 2. Extract \widetilde T^{00}(r,t) definition
m = re.search(r'\\widetilde T\^\{00\}.*?=([\s\S]*?)\]', text)
if not m:
    raise ValueError("Could not find T00 definition in LaTeX")
latex_str = m.group(1).strip()

# 3. Parse into SymPy
T00 = parse_latex(latex_str)

# 4. Static profile: drop time dependence (t -> 0)
t = sp.symbols('t')
T00_r = T00.subs(t, 0)

# 5. Define symbols
r, theta, phi, R, sigma, A = symbols('r theta phi R sigma A', positive=True)

# 6. Compute total negative energy
dV = r**2 * sin(theta)
E_neg = integrate(T00_r * dV, (r, 0, R), (theta, 0, pi), (phi, 0, 2*pi))

# 7. Extremum conditions for R and sigma
dE_dR = diff(E_neg, R)
dE_dsigma = diff(E_neg, sigma)
sol_R = sp.solve(dE_dR, R)
sol_sigma = sp.solve(dE_dsigma, sigma)

# 8. Finiteness bounds on A
from sympy import oo
A_bounds = sp.solve_univariate_inequality(E_neg < oo, A)

# 9. Export results to LaTeX
from sympy import latex
E_neg_ltx = latex(E_neg)
R_ltx = ', '.join(latex(s) for s in sol_R)
sigma_ltx = ', '.join(latex(s) for s in sol_sigma)
A_bounds_ltx = latex(A_bounds)

tex_doc = f"""\documentclass{{article}}
\usepackage{{amsmath}}
\begin{{document}}

\section*{{Total Negative Energy}}
\[
  E_{{\rm neg}}(R,\sigma,A) = {E_neg_ltx}
\]

\section*{{Extremum Conditions}}
\[
  \frac{{\partial E_{{\rm neg}}}}{{\partial R}} = 0
  \quad\Longrightarrow\quad
  R = {R_ltx}
\]
\[
  \frac{{\partial E_{{\rm neg}}}}{{\partial \sigma}} = 0
  \quad\Longrightarrow\quad
  \sigma = {sigma_ltx}
\]

\section*{{Finiteness and Smoothness Bounds}}
\[
  {A_bounds_ltx}
\]

\end{{document}}
"""

with open('parameter_constraints.tex', 'w') as f:
    f.write(tex_doc)
