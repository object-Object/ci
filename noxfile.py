import nox


@nox.session(python=False)
def build(session: nox.Session):
    session.run_install("npm", "ci")
    for name in [
        "parse-cdk-outputs",
    ]:
        session.run(
            "npx",
            "ncc",
            "build",
            f"{name}/index.js",
            f"--out=dist/{name}",
            "--minify",
        )
