def reverse_string(s):
    # Base case: if the string is empty or has only one character, return it as-is
    if len(s) <= 1:
        return s
    # Recursive case: reverse the substring starting from the second character and prepend the first character
    return reverse_string(s[1:]) + s[0]

# Example usage:
input_string = "Hello, World!"
reversed_string = reverse_string(input_string)
print("Original String:", input_string)
print("Reversed String:", reversed_string)

def reverse_string(s):
    return s[::-1]

# Example usage:
input_string = "Hello, World!"
reversed_string = reverse_string(input_string)
print("Original String:", input_string)
print("Reversed String:", reversed_string)



### 1. Finding the Maximum Number in an Array


def find_max(nums):
    max_num = float('-inf')  # Start with negative infinity to handle negative numbers
    for num in nums:
        if num > max_num:
            max_num = num
    return max_num

# Example usage:
numbers = [3, 7, 2, 9, 4, 1]
print("Maximum number in the array:", find_max(numbers))  # Output: 9


### 2. Checking if a String is an Anagram


from collections import Counter

def is_anagram(s1, s2):
    return Counter(s1) == Counter(s2)

# Example usage:
str1 = "listen"
str2 = "silent"
print("Are '{}' and '{}' anagrams?".format(str1, str2))
print(is_anagram(str1, str2))  # Output: True


### 3. Finding the Factorial of a Number


def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Example usage:
number = 5
print("Factorial of", number, "is", factorial(number))  # Output: 120

### 4. Reversing a Linked List (Recursive Approach)


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    if not head or not head.next:
        return head
    new_head = reverse_linked_list(head.next)
    head.next.next = head
    head.next = None
    return new_head

# Example usage (constructing a linked list and reversing it):
nodes = [ListNode(val) for val in range(1, 6)]
for i in range(len(nodes) - 1):
    nodes[i].next = nodes[i + 1]

head = nodes[0]
reversed_head = reverse_linked_list(head)

# Print reversed linked list values
while reversed_head:
    print(reversed_head.val, end=" ")
    reversed_head = reversed_head.next
# Output: 5 4 3 2 1


### 5. Counting Characters in a String


def count_characters(s):
    char_count = {}
    for char in s:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    return char_count

# Example usage:
string = "hello world"
print("Character counts in '{}':".format(string))
print(count_characters(string))
# Output: {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
