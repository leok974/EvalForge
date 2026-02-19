import pytest
import os
from task import generate_report

def test_report_generation(tmp_path, capsys):
    # Setup
    input_file = tmp_path / "sales.csv"
    output_file = tmp_path / "report.txt"
    
    input_file.write_text("id,sales\n1,100\n2,200\n3,300\n", encoding="utf-8")
    
    generate_report(str(input_file), str(output_file))
    
    captured = capsys.readouterr()
    assert "REPORT_GENERATED" in captured.out
    
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "TOTAL_SALES=600.00" in content
    assert "AVG_SALES=200.00" in content
    assert "COUNT=3" in content

def test_missing_input(capsys):
    generate_report("non_existent.csv", "report.txt")
    captured = capsys.readouterr()
    assert "INPUT_MISSING" in captured.out
