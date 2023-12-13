from main import (
    find_perfect_reflection_h,
    find_perfect_reflection_v,
    find_potential_h_reflection,
    find_potential_v_reflection,
    get_positions,
)


def test_positions():
    pattern = """#..#
#.#.
"""
    assert get_positions(pattern, "rock") == {(0, 0), (0, 1), (3, 0), (2, 1)}


def test_positions_ash():
    pattern = """#..#
#.#.
"""
    assert get_positions(pattern, "ash") == {(1, 0), (2, 0), (1, 1), (3, 1)}


def test_potential_v_reflection():
    pattern = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
"""
    assert find_potential_v_reflection(pattern, get_positions(pattern, "rock")) == [(4, 5)]


def test_potential_h_reflection():
    pattern = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
    assert find_potential_h_reflection(pattern, get_positions(pattern, "rock")) == [(3, 4)]


def test_find_perfect_reflection():
    pattern = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
"""
    p_v_reflection = find_potential_v_reflection(pattern, get_positions(pattern, "rock"))
    assert find_perfect_reflection_v(pattern, get_positions(pattern, "rock"), p_v_reflection[0]) == ((4, 5), "v", 5)


def test_find_perfect_reflection_h():
    pattern = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
    p_h_reflection = find_potential_h_reflection(pattern, get_positions(pattern, "rock"))
    assert find_perfect_reflection_h(pattern, get_positions(pattern, "rock"), p_h_reflection[0]) == ((3, 4), "h", 4)
