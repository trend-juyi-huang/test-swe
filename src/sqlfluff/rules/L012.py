"""Implementation of Rule L012."""

from sqlfluff.rules.L011 import Rule_L011


class Rule_L012(Rule_L011):
    """Implicit/explicit aliasing of columns.

    Aliasing of columns to follow preference
    (explicit using an `AS` clause is default).

    NB: This rule inherits its functionality from :obj:`Rule_L011` but is
    separate so that they can be enabled and disabled separately.

    | **Anti-pattern**
    | In this example, the alias for column 'a' is implicit.

    .. code-block:: sql

        SELECT
            a alias_col
        FROM foo

    | **Best practice**
    | Add `AS` to make it explicit.

    .. code-block:: sql

        SELECT
            a AS alias_col
        FROM foo

    """

    config_keywords = ["aliasing"]

    _target_elems = ("select_clause_element",)
