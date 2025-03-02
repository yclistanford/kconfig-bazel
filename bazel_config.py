import pathlib
import argparse
import kconfiglib
import sys


def write_bzl_file(ostream, kconfig: kconfiglib.Kconfig) -> None:
    ostream.write('load("@bazel_skylib//rules:common_settings.bzl", "bool_flag", "int_flag")\n')
    for sym_name, sym in kconfig.syms.items():
        if sym is None:
            continue
        for sym_str in str(sym).splitlines():
            ostream.write(f"# {sym_str}\n")
        if sym.type == kconfiglib.INT:
            ostream.write(f"""int_flag(
    name = "CONFIG_{sym_name}",
)
"""
        )

def generate_bzl_file(kconfig_path: pathlib.Path, out: pathlib.Path | None) -> None:
    kconfig = kconfiglib.Kconfig()
    kconfig.load_allconfig(kconfig_path)
    if out:
        with open(out, "w", encoding='utf-8') as f:
            write_bzl_file(ostream=f, kconfig=kconfig)
    else:
        write_bzl_file(ostream=sys.stdout, kconfig=kconfig)
        


def main() -> None:
    parser = argparse.ArgumentParser(description="Kconfig bazel port")

    parser.add_argument(
        "--kconfig",
        type=pathlib.Path,
        help="Kconfig to load",
        required=True,
    )

    subparsers = parser.add_subparsers(
        dest="subcommand",
        required=True,
    )

    gen_bzl_parser = subparsers.add_parser(
        "gen_bzl",
        help="Generate .bzl settings",
    )
    gen_bzl_parser.add_argument(
        "-o",
        type=pathlib.Path,
        help="Output file",
    )

    args = parser.parse_args()

    kconfig_path = args.kconfig
    subcommand = args.subcommand

    if subcommand == "gen_bzl":
        generate_bzl_file(
            kconfig_path=kconfig_path,
            out=args.o,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
