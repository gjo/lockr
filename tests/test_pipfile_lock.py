import os
import shutil
import tempfile
import pytest


@pytest.yield_fixture
def tempdir():
    dir = tempfile.mkdtemp()
    os.chdir(dir)
    yield dir
    shutil.rmtree(dir)


@pytest.mark.parametrize(
    "pipfile_lock, constraints_txt",
    [
        (
            """\
{
    "default": {
        "appnope": {
            "hashes": [
                "sha256:5b26757dc6f79a3b7dc9fab95359328d5747fcb2409d331ea66d0272b90ab2a0",
                "sha256:8b995ffe925347a2138d7ac0fe77155e4311a0ea6d6da4f5128fe4b3cbe5ed71"
            ],
            "markers": "sys_platform == 'darwin'",
            "version": "==0.1.0"
        },
        "pyramid": {
            "editable": true,
            "git": "https://github.com/Pylons/pyramid.git",
            "ref": "683bc742f7b08db563f3385796809c09babf004b"
        }
    },
    "develop": {
        "pyramid-debugtoolbar": {
            "hashes": [
                "sha256:1c5c16ff71a3f0b0992656e3c3a2a642c096460b0ae7ffe0330f0c9179065c85",
                "sha256:9b52c349cda3eed3d6321693ee5a9c5cd22854e69fc53046512f9564113ebfa0"
            ],
            "index": "pypi",
            "version": "==4.6.1"
        }
    }
}
""",
            """\
appnope==0.1.0; sys_platform == 'darwin'
pyramid @ https://github.com/Pylons/pyramid.git#egg=pyramid
pyramid-debugtoolbar==4.6.1
""",
        ),
    ],
)
def test_pipfile_lock(tempdir, pipfile_lock, constraints_txt):
    import lockr

    with open("Pipfile.lock", "w") as fpw:
        fpw.write(pipfile_lock)

    lockr.main()

    with open("constraints.txt") as fpr:
        content = fpr.read()
    assert content == constraints_txt
