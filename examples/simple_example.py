"""
Simple example script to demonstrate P2E usage.
This script can be converted to an executable.
"""

def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"


def main():
    """Main function."""
    print("=" * 50)
    print("  Welcome to P2E Example Application")
    print("=" * 50)
    print()
    
    name = input("Enter your name: ")
    greeting = greet(name)
    
    print(f"\n{greeting}")
    print("\nThis application was built with P2E!")
    print("GitHub: https://github.com/Varun-SV/P2E")
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
