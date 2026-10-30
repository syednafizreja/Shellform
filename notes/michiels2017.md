# Reading notes: Michiels & Adriaenssens, seismic form-finding

Written by Claude on 29 Oct 2026 from what is openly readable: the abstract and highlights of the C&S paper (ScienceDirect abstract page) and the abstract of the J. IASS paper (academia.edu). **The full texts have not been read.** Everything marked [check] must be confirmed against the full text before it enters `docs/preregistration.md`.

## 1. Citations

- **C&S:** Michiels T., Adriaenssens S. Form-finding algorithm for masonry arches subjected to in-plane earthquake loading. *Computers & Structures* 195 (2018) 85-98, online 12 Oct 2017. doi:10.1016/j.compstruc.2017.10.001.
- **J. IASS:** Michiels T. (with Adriaenssens and Jorquera-Lucerga per the data contract [check]). Parametric study of masonry shells form-found for seismic loading. doi:10.20898/j.iass.2017.194.892. 9 pages.

## 2. How the lateral load is applied

- **C&S (arches, 2D):** "Horizontal acceleration is used as a first-order approximation of seismic action" (highlights). Self-weight plus an in-plane horizontal acceleration. Forms for **0.15, 0.3 and 0.45 g** and rise-to-span **1/2, 1/4, 1/8** (abstract).
- **J. IASS (shells, 3D):** an "inversed hanging chain model subjected to lateral loading in a dynamic relaxation solver" (abstract). The academia.edu summary says 0.3 g represents moderate-to-high seismicity [check: machine-generated summary, not the paper].
- Distribution over the mass: horizontal force = acceleration x nodal mass, presumably [check].
- Sign cases (load reversal): not in the abstracts [check]. The IASS paper produces **double-layer** shells. The likely reason is that one layer carries the thrust surface for each direction of shaking [check]. This matters for ShellForm; see F1.

## 3. Form-finding method

- **C&S:** thrust line analysis (lower bound) plus kinematic limit analysis (upper bound), with "a series of geometric manipulations of the thrust line". The result guarantees a compression-only load path at the design acceleration. Not force density.
- **J. IASS:** dynamic relaxation, not force density.
- **ShellForm's difference:** ShellBench floor-r1 is a force density method. ShellForm's lateral-load extension is our own formulation "after" Michiels, so the paper must not claim to reproduce their algorithm.

## 4. Constraints and how the final form is chosen

- C&S: the form must hold a compression-only load path under gravity and the design acceleration. Result: up to 65 % less material than constant-thickness circular arches at the same acceleration (highlights).
- J. IASS: a parametric study over boundary conditions and net stiffness [check: which parameters exactly].

## 5. Finding F1 (Claude, checked by test): uniform lateral load only shears the gravity form

In a force density network with fixed nodal loads and supports at z = 0, adding p_x = a w to every node (a = Sa in g, w = nodal weight) gives exactly

x_seismic = x_gravity - a z_gravity, with y and z unchanged.

Reason: the force density equations solve each coordinate separately, D x = p_x - D_f x_fixed, and p_x = -a p_z. So the "seismic-aware" form is the gravity form leaning into the load. `tests/test_checks.py::test_uniform_lateral_acceleration_shears_the_gravity_form` confirms it to 1e-12.

Consequences for the pre-registration [J]:

1. A single sheared form suits shaking in one direction only. Earthquakes reverse, and a square plan has two axes, so strategy 2 must consider +x, -x, +y and -y.
2. Options: (a) the shell must contain the thrust surfaces of all four cases within its thickness (closest to Michiels' double layer [check]); (b) an envelope or average form, sized for all four cases; (c) change the force densities, not only the loads, so the form is not just a shear.
3. With (a) the extra thickness comes directly from the shear a z. Rise-to-span then trades off directly against seismic demand, which is a clean and testable result for the paper.
4. Self-weight that updates with geometry, as in dynamic relaxation, breaks the exact shear slightly. ShellForm must say which it uses.

**This is the main decision for 30 Oct:** pick (a), (b) or (c) before approving the pre-registration.

## 5b. Finding F2 (30 Oct, unit-test nets only, not a result)

On 10 m test nets (21 x 21, rise 1.5 m), the strategy 2 mid-surface (the midrange of the four sheared thrust surfaces) changes the envelope thickness t_env by less than 4 % compared with the gravity form, at Sa = 0.1 to 0.5 g, for both support cases. The reason is the four-direction symmetry: shaking in +x and in -x lean the thrust surface opposite ways, so no single surface centres them much better than the gravity form does. This is an early warning that, under the uniform-acceleration model, the answer may be "no meaningful difference". If so, that is reported as it is (pre-registration, section 7). Any differences between the strategies in the FE checks (bending under lateral load) may still matter.

## 6. S4 candidate (published case to reproduce)

The C&S arch cases (rise/span 1/2, 1/4, 1/8 at 0.15, 0.3, 0.45 g) are the most reproducible: 2D, with stated inputs. The thrust line of a given arch under gravity + a g can be computed with a 2D force density chain and compared with their figure. Figure or table number and readable tolerance: [check full text].

## 7. To copy into docs/preregistration.md section 4 (after the full-text check)

- Lateral load = Sa x nodal weight, horizontal, applied in +x, -x, +y, -y.
- The reversal rule chosen from F1 (a, b or c).
- The S4 case and its tolerance.

## Still to get

Full texts of both papers (ResearchGate request to Tim Michiels), plus Michiels, Adriaenssens & DeJong 2018 (Engineering Structures) and the 2017 Engineering Structures paper.
