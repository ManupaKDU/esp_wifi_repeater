with open('user/user_main.c', 'r') as f:
    lines = f.readlines()

count = 0
for l, line in enumerate(lines):
    # Ignoring comments
    if '//' in line:
        line = line[:line.find('//')]
    # This is a very naive brace checker, assuming no weird string literals
    for char in line:
        if char == '{':
            count += 1
        elif char == '}':
            count -= 1
            if count < 0:
                print(f"Extra '}}' found at line {l+1}")
                count = 0 # reset to not cascade
print(f"Final brace count: {count}")
