"""
Bangladeshi Mobile Number Generator
==================================
Generates valid Bangladeshi mobile numbers and saves to emails.txt
"""

import random
from typing import Set

class BangladeshiMobileGenerator:
    """Generate Bangladeshi mobile numbers in +880 format"""
    
    # Bangladeshi mobile operator prefixes
    OPERATOR_PREFIXES = [
        '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
        '140', '141', '142', '143', '144', '145', '146', '147', '148', '149',
        '150', '151', '152', '153', '154', '155', '156', '157', '158', '159',
        '160', '161', '162', '163', '164', '165', '166', '167', '168', '169',
        '170', '171', '172', '173', '174', '175', '176', '177', '178', '179',
        '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',
        '190', '191', '192', '193', '194', '195', '196', '197', '198', '199'
    ]
    
    COUNTRY_CODE = "+880"
    NUMBER_LENGTH = 11  # Without country code

    def generate_number(self) -> str:
        """Generate a single Bangladeshi mobile number"""
        prefix = random.choice(self.OPERATOR_PREFIXES)
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(self.NUMBER_LENGTH - len(prefix))])
        return f"{self.COUNTRY_CODE}{prefix}{suffix}"
    
    def generate_numbers(self, count: int) -> Set[str]:
        """Generate unique Bangladeshi mobile numbers"""
        numbers = set()
        while len(numbers) < count:
            numbers.add(self.generate_number())
        return numbers
    
    @staticmethod
    def save_to_file(numbers: Set[str], filename: str = "emails.txt") -> None:
        """Save numbers to text file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted(numbers)))
        print(f"Successfully saved {len(numbers)} numbers to {filename}")

def main():
    try:
        # Initialize generator
        generator = BangladeshiMobileGenerator()
        
        # Get user input for count
        count = int(input("কতগুলো মোবাইল নম্বর জেনারেট করতে চান? (ডিফল্ট: 5000): ") or 5000)
        
        # Generate numbers
        print(f"\n{count} টি বাংলাদেশি মোবাইল নম্বর জেনারেট করা হচ্ছে...")
        numbers = generator.generate_numbers(count)
        
        # Save to emails.txt
        generator.save_to_file(numbers)
        
        print("\nজেনারেশন সম্পূর্ণ হয়েছে!")
        
    except ValueError:
        print("দুঃখিত! সঠিক সংখ্যা ইনপুট দিন।")
    except Exception as e:
        print(f"ত্রুটি হয়েছে: {str(e)}")

if __name__ == "__main__":
    print("বাংলাদেশি মোবাইল নম্বর জেনারেটর")
    print("===============================")
    main()
