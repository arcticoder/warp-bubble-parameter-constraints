# warp-bubble-parameter-constraints

This repository provides:

1. **analyze_constraints.py**  
   A Python script that:
   - Fetches the LaTeX definition of the exotic‐matter energy density \(\widetilde T^{00}(r,t)\) from the previous repo.
   - Converts it into a SymPy expression.
   - Computes the total negative energy
     \[
       E_{\rm neg}
       = \int_0^R \!\!\int_0^\pi\!\!\int_0^{2\pi}
         \widetilde T^{00}(r)\,r^2\sin\theta\,
         d\phi\,d\theta\,dr
     \]
   - Solves \(\frac{\partial E_{\rm neg}}{\partial R}=0\) and \(\frac{\partial E_{\rm neg}}{\partial \sigma}=0\).
   - Derives bounds on the amplitude \(A\) to ensure finiteness of \(E_{\rm neg}\).
   - Exports the results as LaTeX.

2. **parameter_constraints.tex**  
   A ready‐to‐compile LaTeX document that presents:
   - The analytic form of \(E_{\rm neg}(R,\sigma,A)\).
   - Extremum conditions for \(R\) and \(\sigma\).
   - Inequalities on \(A\) enforcing finite total negative energy.

---

## Prerequisites

- Python 3.7+
- [SymPy](https://www.sympy.org/)  
- [requests](https://pypi.org/project/requests/)

Install dependencies via:
```bash
pip install sympy requests
```

---

## Usage

1.  **Clone the repo**
    
```bash
git clone https://github.com/arcticoder/warp-bubble-parameter-constraints.git
cd warp-bubble-parameter-constraints
```
    
2.  **Run the analysis script**
    
```bash
python analyze_constraints.py
```

    This will:
    
    -   Download the exotic‐matter density LaTeX from  
        `https://raw.githubusercontent.com/arcticoder/warp-bubble-exotic-matter-density/refs/heads/main/exotic_matter_density.tex`
        
    -   Compute and print out the constraints.
        
    -   Write `parameter_constraints.tex` in the project root.
        
3.  **Compile the LaTeX**
    
```bash
pdflatex parameter_constraints.tex
```
    
    to produce a PDF report of your results.
    

---

## Files

-   **analyze\_constraints.py**  
    Python script performing the symbolic computations and exporting LaTeX.
    
-   **parameter\_constraints.tex**  
    LaTeX document detailing the results.
