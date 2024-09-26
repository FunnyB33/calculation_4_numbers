# calculation.py

def calculation(a, b, c, d, target):
    import itertools
    result = 0
    expressions = []
    nums = [a, b, c, d]
    ops = ['+', '-', '*', '/']
    structures = [
        '(( {} {} {} ) {} {} ) {} {}',
        '( {} {} ( {} {} {} ) ) {} {}',
        '{} {} ( ( {} {} {} ) {} {} )',
        '{} {} ( {} {} ( {} {} {} ) )',
        '( {} {} {} ) {} ( {} {} {} )'
    ]
    for num_perm in itertools.permutations(nums):
        for op_comb in itertools.product(ops, repeat=3):
            for structure in structures:
                expr = structure.format(
                    num_perm[0], op_comb[0], num_perm[1],
                    op_comb[1], num_perm[2], op_comb[2], num_perm[3]
                )
                try:
                    if abs(eval(expr) - target) < 1e-6:
                        expressions.append(f"{expr} = {target}")
                except ZeroDivisionError:
                    continue
    # 重複する式を削除
    expressions = list(set(expressions))
    expressions.sort()
    result = len(expressions)
    return result, expressions
