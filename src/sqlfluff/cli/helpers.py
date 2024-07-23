"""CLI helper utilities."""

from io import StringIO
import sys
import textwrap
from typing import Optional, List, Dict, Tuple

from colorama import Style

from sqlfluff import __version__ as pkg_version
from sqlfluff.core.enums import Color


def colorize(s: str, color: Optional[Color] = None) -> str:
    """Use ANSI colour codes to colour a string.

    The name of this function is in American. I'm sorry :(.
    """
    if color:
        return f"{color.value}{s}{Style.RESET_ALL}"
    else:
        return s


def get_python_version() -> str:
    """Get the current python version as a string."""
    return "{0[0]}.{0[1]}.{0[2]}".format(sys.version_info)


def get_python_implementation() -> str:
    """Get the current python implementation as a string.

    This is useful if testing in pypy or similar.
    """
    return sys.implementation.name


def get_package_version() -> str:
    """Get the current version of the sqlfluff package."""
    return pkg_version


def wrap_elem(s: str, width: int) -> List[str]:
    """Wrap a string into a list of strings all less than <width>."""
    return textwrap.wrap(s, width=width)


def wrap_field(
    label: str, val: str, width: int, max_label_width: int = 10, sep_char: str = ": "
) -> Dict:
    """Wrap a field (label, val).

    Returns:
        A dict of {label_list, val_list, sep_char, lines}

    """
    if len(label) > max_label_width:
        label_list = wrap_elem(label, width=max_label_width)
        label_width = max(len(line) for line in label_list)
    else:
        label_width = len(label)
        label_list = [label]

    max_val_width = width - len(sep_char) - label_width
    val_list = wrap_elem(val, width=max_val_width)
    return dict(
        label_list=label_list,
        val_list=val_list,
        sep_char=sep_char,
        lines=max(len(label_list), len(val_list)),
        label_width=label_width,
        val_width=max_val_width,
    )


def pad_line(s: str, width: int, align: str = "left") -> str:
    """Pad a string with a given alignment to a specific width with spaces."""
    gap = width - len(s)
    if gap <= 0:
        return s
    elif align == "left":
        return s + (" " * gap)
    elif align == "right":
        return (" " * gap) + s
    else:
        raise ValueError(f"Unknown alignment: {align}")  # pragma: no cover


def cli_table_row(
    fields: List[Tuple[str, str]],
    col_width,
    max_label_width=10,
    sep_char=": ",
    divider_char=" ",
    label_color=Color.lightgrey,
    val_align="right",
) -> str:
    """Make a row of a CLI table, using wrapped values."""
    # Do some intel first
    cols = len(fields)
    last_col_idx = cols - 1
    wrapped_fields = [
        wrap_field(
            field[0],
            field[1],
            width=col_width,
            max_label_width=max_label_width,
            sep_char=sep_char,
        )
        for field in fields
    ]
    max_lines = max(fld["lines"] for fld in wrapped_fields)
    last_line_idx = max_lines - 1
    # Make some text
    buff = StringIO()
    for line_idx in range(max_lines):
        for col_idx in range(cols):
            # Assume we pad labels left and values right
            fld = wrapped_fields[col_idx]
            ll = fld["label_list"]
            vl = fld["val_list"]
            buff.write(
                colorize(
                    pad_line(
                        ll[line_idx] if line_idx < len(ll) else "",
                        width=fld["label_width"],
                    ),
                    color=label_color,
                )
            )
            if line_idx == 0:
                buff.write(sep_char)
            else:
                buff.write(" " * len(sep_char))
            buff.write(
                pad_line(
                    vl[line_idx] if line_idx < len(vl) else "",
                    width=fld["val_width"],
                    align=val_align,
                )
            )
            if col_idx != last_col_idx:
                buff.write(divider_char)
            elif line_idx != last_line_idx:
                buff.write("\n")
    return buff.getvalue()


def cli_table(
    fields,
    col_width=20,
    cols=2,
    divider_char=" ",
    sep_char=": ",
    label_color=Color.lightgrey,
    float_format="{0:.2f}",
    max_label_width=10,
    val_align="right",
) -> str:
    """Make a crude ascii table.

    Assume that `fields` is an iterable of (label, value) pairs.
    """
    # First format all the values into strings
    formatted_fields = []
    for label, value in fields:
        label = str(label)
        if isinstance(value, float):
            value = float_format.format(value)
        else:
            value = str(value)
        formatted_fields.append((label, value))

    # Set up a buffer to hold the whole table
    buff = StringIO()
    while len(formatted_fields) > 0:
        row_buff: List[Tuple[str, str]] = []
        while len(row_buff) < cols and len(formatted_fields) > 0:
            row_buff.append(formatted_fields.pop(0))
        buff.write(
            cli_table_row(
                row_buff,
                col_width=col_width,
                max_label_width=max_label_width,
                sep_char=sep_char,
                divider_char=divider_char,
                label_color=label_color,
                val_align=val_align,
            )
        )
        if len(formatted_fields) > 0:
            buff.write("\n")
    return buff.getvalue()
