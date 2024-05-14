import json
from ast import parse
from ast2json import ast2json
import sys
from pathlib import Path

if (args_count := len(sys.argv)) > 2:
    print(f"2 argument expected, got {args_count - 1}")
    raise SystemExit(2)
elif args_count < 2:
    print("You must specify the target directory")
    raise SystemExit(2)



ast1 = ast2json(parse(open(sys.argv[1]).read()))
astj=(json.dumps(ast1, indent=4))
print(astj)