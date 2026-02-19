# Tags: Release v1.0.0

## Objective
Create an annotated tag and verify it points to HEAD.

## Requirements
Running:
  sh task.sh
must:
1) Create repo sandbox/repo (main) with one commit
2) Create an ANNOTATED tag: v1.0.0 with message "Release v1.0.0"
3) Write:
   - outputs/tag_type.txt  (git cat-file -t v1.0.0) => must be "tag"
   - outputs/tag_target.txt (git rev-parse v1.0.0^{}) => must equal HEAD
