import json

__version__ = "0.1.dev0"


def main() -> None:
    with open("Pipfile.lock") as fp:
        content = json.load(fp)

    deps = {}
    for sec_name in "default", "develop":
        for k, v in content[sec_name].items():
            dep_info = ""
            if "version" in v:
                if "markers" in v:
                    dep_info = f'{v["version"]}; {v["markers"]}'
                else:
                    dep_info = v["version"]

            elif "git" in v:
                dep_info = f' @ {v["git"]}#egg={k}'
            if dep_info:
                deps[k] = dep_info

    with open("constraints.txt", "w") as fpw:
        for k in sorted(deps):
            fpw.write(f"{k}{deps[k]}\n")


if __name__ == "__main__":
    main()  # pragma: no cover
