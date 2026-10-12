# Contributing
1. New model -> MATRIX in build.py (one line per model).
2. Parameter improvements -> PR with source (community thread / benchmark).
3. Never hand-edit files in workflows/ -- they are generated. Edit build.py.
4. CI must pass: aevum-workflows build /tmp/wf && aevum-workflows validate /tmp/wf
5. Placeholder contract: PLACEHOLDERS in build.py is the single source of
   truth, synced with the Aevum platform (app/backends/comfyui.py).
