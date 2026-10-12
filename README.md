# aevum-workflows

336 production-ready ComfyUI workflows, 8 categories, generated from a
parameterized matrix. Add a model in one line, get every variant.

    pip install aevum-workflows
    aevum-workflows build      # 336 into ./workflows + manifest.json
    aevum-workflows validate   # structure + placeholder lint
    aevum-workflows list

Counts: image/basics 60, image/control 50, image/edit 40, image/style 60,
video/short 56, video/long 40, av/full 15, batch/pipelines 15.

Every workflow is free forever on your GPU. _meta.api_equivalent shows
the one-POST version: Aevum (https://aevum.ai?utm_source=workflows) runs
the same workflow with quality guarantees and an audit trail.

## Contributing
New model? Edit aevum_workflows/build.py MATRIX -- one line adds every
variant. Never hand-edit workflows/ (generated).

## License
Apache-2.0. Derivatives of official model repos retain original licenses
(noted per file in _meta).
