with open("input.txt") as f:
    data = f.read().splitlines()

ans, ans2 = 0, 0
for i, game in enumerate(data):
    sets = game.split(";")
    id = i + 1
    possible = True
    c_blues, c_reds, c_greens = [], [], []
    for s in sets:
        c_blue, c_red, c_green = 0, 0, 0
        cubes = s.split(", ")
        for c in cubes:
            c = c.split(": ")[1] if c.startswith("Game") else c
            if "red" in c:
                c_red += int(c.split()[0])
            elif "green" in c:
                c_green += int(c.split()[0])
            elif "blue" in c:
                c_blue += int(c.split()[0])
            else:
                print("Error")
        c_blues.append(c_blue)
        c_reds.append(c_red)
        c_greens.append(c_green)
        if c_red > 12 or c_green > 13 or c_blue > 14:
            possible = False
    if possible:
        ans += id
    power = max(c_blues) * max(c_reds) * max(c_greens)
    ans2 += power

print(f"Part 1: {ans}")
print(f"Part 2: {ans2}")
