"""Tests the python routines within L020."""

import sqlfluff


def test__rules__std_L020_one_aliases_one_duplicate():
    """Verify correct error message for one duplicate table aliases occur one times."""
    sql = """
        SELECT
            a.pk
        FROM table_1 AS a
        JOIN table_2 AS a ON a.pk = a.pk
    """
    result = sqlfluff.lint(sql)
    assert "L020" in [r["code"] for r in result]
    assert [r["code"] for r in result].count("L020") == 1


def test__rules__std_L020_one_aliases_two_duplicate():
    """Verify correct error message for one duplicate table aliases occur two times."""
    sql = """
        SELECT
            a.pk
        FROM table_1 AS a
        JOIN table_2 AS a ON a.pk = a.pk
        JOIN table_3 AS a ON a.pk = a.pk
    """
    result = sqlfluff.lint(sql)
    result_filter = [r for r in result if r["code"] == "L020"]
    # Error message only show two times, not three
    assert len(result_filter) == 2
    assert (
        len(
            [
                r
                for r in result_filter
                if "Duplicate table alias 'a'" in r["description"]
            ]
        )
        == 2
    )
    # Test specific line number
    assert result_filter[0]["line_no"] == 5
    assert result_filter[1]["line_no"] == 6


def test__rules__std_L020_complex():
    """Verify that L020 returns the correct error message for complex example."""
    sql = """
        SELECT
            a.pk,
            b.pk
        FROM table_1 AS a
        JOIN table_2 AS a ON a.pk = a.pk
        JOIN table_3 AS b ON a.pk = b.pk
        JOIN table_4 AS b ON b.pk = b.pk
        JOIN table_5 AS a ON b.pk = a.pk
    """
    result = sqlfluff.lint(sql)
    result_filter = [r for r in result if r["code"] == "L020"]
    # Error message only show two times, not three
    assert len(result_filter) == 3
    assert (
        len(
            [
                r
                for r in result_filter
                if "Duplicate table alias 'a'" in r["description"]
            ]
        )
        == 2
    )
    assert (
        len(
            [
                r
                for r in result_filter
                if "Duplicate table alias 'b'" in r["description"]
            ]
        )
        == 1
    )
    # Test specific line number
    assert result_filter[0]["line_no"] == 6
    assert result_filter[1]["line_no"] == 8
    assert result_filter[2]["line_no"] == 9
