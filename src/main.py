import argparse
import os
import sys
from integrity_checker import IntegrityChecker

__version__ = "1.0.0"

def main():
    print(f"HexGuard Security — v{__version__}")
    parser = argparse.ArgumentParser(description="🛡️ HexGuard — File Integrity Monitor (FIM)")
    parser.add_argument("--init", help="Initialize or update baseline for a directory", metavar="DIR")
    parser.add_argument("--check", help="Scan directory against saved baseline", metavar="DIR")
    parser.add_argument("--baseline", help="Custom baseline file path", default="baseline.json")
    parser.add_argument("--ignore", help="Custom ignore file path", default=".fim-ignore")
    
    args = parser.parse_args()
    
    if args.init:
        if not os.path.isdir(args.init):
            print(f"[-] Error: {args.init} is not a directory.")
            sys.exit(1)
        checker = IntegrityChecker(args.init, ignore_file=args.ignore)
        checker.generate_baseline(args.baseline)
    elif args.check:
        if not os.path.isdir(args.check):
            print(f"[-] Error: {args.check} is not a directory.")
            sys.exit(1)
        checker = IntegrityChecker(args.check, ignore_file=args.ignore)
        results = checker.verify_integrity(args.baseline)
        
        if results is None:
            return

        print("\n" + "="*40)
        print("🔍 INTEGRITY SCAN RESULTS")
        print("="*40)
        
        if not all(not v for v in results.values()):
            if results["modified"]:
                print(f"⚠️  MODIFIED ({len(results['modified'])}):")
                for f in results["modified"]: print(f"   [!] {f}")
            if results["deleted"]:
                print(f"❌ DELETED ({len(results['deleted'])}):")
                for f in results["deleted"]: print(f"   [-] {f}")
            if results["new"]:
                print(f"🆕 NEW ({len(results['new'])}):")
                for f in results["new"]: print(f"   [+] {f}")
        else:
            print("✅ No integrity violations detected. Files are consistent.")
        print("="*40 + "\n")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
