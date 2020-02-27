import hrm

if __name__ == "__main__":
    from hrm.tests import TestHRM
    import unittest

    unittest.main()

    program = """
    loop:
        INBOX
        COPYTO 0
        INBOX
        ADD 0
        OUTBOX
        JUMP loop
    """

    hrm_program = hrm.HRM(program, 1)
    print(hrm_program([1, 2]))
    print(hrm_program(["A", "B"]))
