import json

__version__ = "0.1.dev3"


def main() -> None:
    with open("Pipfile.lock") as fp:
        content = json.load(fp)

    deps = {}
    for sec_name in "default", "develop":
        for k, v in content[sec_name].items():

            # Editable requirements are not allowed as constraints
            if v.get("editable"):
                continue

            dep_info = ""
            if "version" in v:
                dep_info = f'{k}{v["version"]}'
                if "markers" in v:
                    dep_info = f'{dep_info}; {v["markers"]}'

            elif "git" in v:
                dep_info = f'{k} @ git+{v["git"]}@{v["ref"]}'

            if dep_info:
                deps[k] = dep_info

    with open("constraints.txt", "w") as fpw:
        for k in sorted(deps):
            fpw.write(f"{deps[k]}\n")


if __name__ == "__main__":
    main()  # pragma: no cover
