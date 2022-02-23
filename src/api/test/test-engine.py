import argparse
from api.core.engine import dnx

parser = argparse.ArgumentParser(description="Test for engine.py")
parser.add_argument("string", help="domain to query")
args = parser.parse_args()

print(dnx(args.string))
