"""
Bangladeshi Mobile Number Generator (Text File Output)
=====================================================
Generates valid Bangladeshi mobile numbers with country code (+880)
and saves them in a text file (one number per line).
"""

import random
import argparse
from typing import Set
from pathlib import Path

class BangladeshiMobileGenerator:
    """Generate Bangladeshi mobile numbers and save to text file"""
    
    # Bangladeshi mobile operator prefixes
    OPERATOR_PREFIXES = {
        'grameenphone': ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                         '140', '141', '142', '143', '144', '145', '146', '147', '148', '149'],
        'robi': ['150', '151', '152', '153', '154', '155', '156', '157', '158', '159'],
        'airtel': ['160', '161', '162', '163', '164', '165', '166', '167', '168', '169'],
        'teletalk': ['170', '171', '172', '173', '174', '175', '176', '177', '178', '179',
                     '190', '191', '192', '193', '194', '195', '196', '197', '198', '199'],
        'banglalink': ['180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    }
    
    COUNTRY_CODE = "+880"
    NUMBER_LENGTH = 11  # Without country code
    DEFAULT_COUNT = 5000

    def __init__(self):
        self.all_prefixes = [
            prefix for operator in self.OPERATOR_PREFIXES.values() for prefix in operator
        ]

    def generate_number(self, prefix: str = None) -> str:
        """Generate a single Bangladeshi mobile number"""
        selected_prefix = prefix if prefix else random.choice(self.all_prefixes)
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(self.NUMBER_LENGTH - len(selected_prefix))])
        return f"{self.COUNTRY_CODE}{selected_prefix}{suffix}"
    
    def generate_numbers(self, count: int = DEFAULT_COUNT, prefix: str = None) -> Set[str]:
        """Generate unique Bangladeshi mobile numbers"""
        numbers = set()
        while len(numbers) < count:
            numbers.add(self.generate_number(prefix))
        return numbers
    
    @staticmethod
    def save_to_text(numbers: Set[str], filename: str) -> None:
        """Save numbers to text file (one per line)"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(numbers)))
            print(f"\nSuccessfully saved {len(numbers):,} numbers to {filename}")
        except IOError as e:
            print(f"\nError saving file: {str(e)}")
            raise

def main():
    parser = argparse.ArgumentParser(
        description='Generate Bangladeshi mobile numbers and save to text file'
    )
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=BangladeshiMobileGenerator.DEFAULT_COUNT,
        help=f'Number of mobile numbers to generate (default: {BangladeshiMobileGenerator.DEFAULT_COUNT:,})'
    )
    parser.add_argument(
        '-o', '--output',
        default='bd_mobile_numbers.txt',
        help='Output text file path (default: bd_mobile_numbers.txt)'
    )
    parser.add_argument(
        '-p', '--prefix',
        help='Specific prefix to use (e.g., 171 for Teletalk)'
    )
    parser.add_argument(
        '--operator',
        choices=list(BangladeshiMobileGenerator.OPERATOR_PREFIXES.keys()),
        help='Generate numbers for specific operator only'
    )
    
    args = parser.parse_args()
    
    try:
        generator = BangladeshiMobileGenerator()
        
        # Get specific prefix if operator is specified
        prefix = args.prefix
        if args.operator and not prefix:
            prefix = random.choice(generator.OPERATOR_PREFIXES[args.operator])
        
        print(f"Generating {args.count:,} Bangladeshi mobile numbers...")
        numbers = generator.generate_numbers(args.count, prefix)
        
        # Save to text file
        generator.save_to_text(numbers, args.output)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        parser.print_help()
        exit(1)

if __name__ == "__main__":
    main()
