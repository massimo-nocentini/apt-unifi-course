
class BrokenImplementation(Exception): pass

class TestCase:

    def __init__(self, getter):
        self.getter = getter

    def set_up(self): pass

    def tear_down(self): pass
    
    def run(self):
        result = TestResult()
        result.test_started()
        self.set_up()

        try:
            method = self.getter(self)
            method()
        except BrokenImplementation:
            result.test_failed()

        self.tear_down()

        return result


class WasRun(TestCase):

    def test_method(self):
        self.was_run = True 
        self.log.append('test_method')

    def broken_test_method(self):
        raise BrokenImplementation
    
    def set_up(self):
        self.was_run = False
        self.log = []
        self.log.append('set_up')

    def tear_down(self):
        self.log.append('tear_down')


class TestResult:

    def __init__(self):
        self.run_count = 0
        self.failed_count = 0

    def summary(self):
        return "{} run, {} failed".format(self.run_count, self.failed_count)

    def test_started(self):
        self.run_count += 1

    def test_failed(self):
        self.failed_count += 1


class TestSuite:

    def __init__(self):
        self.tests = []
        
    def append(self, case):
        self.tests.append(case)
    
    def run(self):
#       However, one of the main constraints on Composite interface, in this case about `run` message,
#       is that the aggragate must respond to the same messages as the individual objects. If we add a
#       parameter to test objects in `self.tests`, then we have to add the same parameter to `TestSuite`,
#       objects of this class, too.
        result = TestResult()
        for test in self.tests:
            test.run(result)
        return result
