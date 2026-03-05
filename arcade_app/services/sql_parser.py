def strip_sql_comments(sql: str) -> str:
    """
    Remove -- line comments and /* block comments */ from SQL,
    while preserving single-quoted string literals and newlines.
    """
    if not sql:
        return ""
        
    result = []
    in_string = False
    in_line_comment = False
    in_block_comment = False
    
    i = 0
    n = len(sql)
    
    while i < n:
        c = sql[i]
        
        if in_line_comment:
            if c == '\n':
                in_line_comment = False
                result.append(c)
            i += 1
            continue
            
        if in_block_comment:
            if c == '*' and i + 1 < n and sql[i+1] == '/':
                in_block_comment = False
                i += 2
            elif c == '\n':
                result.append(c)
                i += 1
            else:
                i += 1
            continue
            
        if in_string:
            result.append(c)
            if c == "'":
                in_string = False
            i += 1
            continue
            
        # Not in string or comment
        if c == "'":
            in_string = True
            result.append(c)
            i += 1
            continue
            
        if c == '-' and i + 1 < n and sql[i+1] == '-':
            in_line_comment = True
            i += 2
            continue
            
        if c == '/' and i + 1 < n and sql[i+1] == '*':
            in_block_comment = True
            i += 2
            continue
            
        result.append(c)
        i += 1
        
    return "".join(result)
