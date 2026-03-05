import pytest
from arcade_app.services.sql_parser import strip_sql_comments

def test_strip_line_comments():
    sql = "SELECT 1; -- HAVING COUNT(\nSELECT 2;"
    stripped = strip_sql_comments(sql)
    assert "HAVING COUNT" not in stripped
    assert "SELECT 1;" in stripped
    assert "\nSELECT 2;" in stripped

def test_strip_block_comments():
    sql = "SELECT /* OVER (PARTITION BY \n ) */ 1;"
    stripped = strip_sql_comments(sql)
    assert "OVER" not in stripped
    assert "SELECT \n 1;" in stripped

def test_keywords_inside_strings_remain():
    sql = "SELECT '-- HAVING COUNT(' AS s;"
    stripped = strip_sql_comments(sql)
    assert "-- HAVING COUNT(" in stripped

def test_mixed_comments():
    sql = """
    SELECT category FROM products
    /* We want to -- group */
    GROUP BY category -- group by 1
    HAVING category = 'A' -- HAVING COUNT(
    """
    stripped = strip_sql_comments(sql)
    
    assert "HAVING COUNT" not in stripped
    assert "We want to" not in stripped
    assert "group by 1" not in stripped
    assert "GROUP BY category" in stripped
    assert "HAVING category = 'A'" in stripped

def test_escaped_quotes_in_strings():
    sql = "SELECT 'It''s a /* comment */ test -- yep' FROM dual;"
    stripped = strip_sql_comments(sql)
    assert "/* comment */" in stripped
    assert "-- yep" in stripped
