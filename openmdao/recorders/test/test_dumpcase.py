""" Unit test for the DumpCaseRecorder. """

import unittest

from six import StringIO

from openmdao.recorders.dumpcase import DumpCaseRecorder
from openmdao.core.problem import Problem
from openmdao.test.converge_diverge import ConvergeDiverge
from openmdao.test.examplegroups import ExampleGroup


class TestDumpCaseRecorder(unittest.TestCase):

    def test_basic(self):

        top = Problem()
        top.root = ConvergeDiverge()

        sout = StringIO()
        recorder = DumpCaseRecorder(sout)
        top.driver.add_recorder(recorder)
        top.setup()
        top.run()

        expected = \
'''Iteration Coordinate: Driver/1
Params:
  comp1.x1: 2.0
  comp2.x1: 8.0
  comp3.x1: 6.0
  comp4.x1: 4.0
  comp4.x2: 21.0
  comp5.x1: 46.0
  comp6.x1: -93.0
  comp7.x1: 36.8
  comp7.x2: -46.5
Unknowns:
  comp1.y1: 8.0
  comp1.y2: 6.0
  comp2.y1: 4.0
  comp3.y1: 21.0
  comp4.y1: 46.0
  comp4.y2: -93.0
  comp5.y1: 36.8
  comp6.y1: -46.5
  comp7.y1: -102.7
  p.x: 2.0
Resids:
  comp1.y1: 0.0
  comp1.y2: 0.0
  comp2.y1: 0.0
  comp3.y1: 0.0
  comp4.y1: 0.0
  comp4.y2: 0.0
  comp5.y1: 0.0
  comp6.y1: 0.0
  comp7.y1: 0.0
  p.x: 0.0
'''

        self.assertEqual(sout.getvalue(), expected)

    def test_excludes(self):

        top = Problem()
        top.root = ConvergeDiverge()

        sout = StringIO()

        recorder = DumpCaseRecorder(sout)
        recorder.options['excludes'] = ['comp4.y1']
        top.driver.add_recorder(recorder)
        top.setup()
        top.run()

        expected = \
'''Iteration Coordinate: Driver/1
Params:
  comp1.x1: 2.0
  comp2.x1: 8.0
  comp3.x1: 6.0
  comp4.x1: 4.0
  comp4.x2: 21.0
  comp5.x1: 46.0
  comp6.x1: -93.0
  comp7.x1: 36.8
  comp7.x2: -46.5
Unknowns:
  comp1.y1: 8.0
  comp1.y2: 6.0
  comp2.y1: 4.0
  comp3.y1: 21.0
  comp4.y2: -93.0
  comp5.y1: 36.8
  comp6.y1: -46.5
  comp7.y1: -102.7
  p.x: 2.0
Resids:
  comp1.y1: 0.0
  comp1.y2: 0.0
  comp2.y1: 0.0
  comp3.y1: 0.0
  comp4.y2: 0.0
  comp5.y1: 0.0
  comp6.y1: 0.0
  comp7.y1: 0.0
  p.x: 0.0
'''

        self.assertEqual( sout.getvalue(), expected )

    def test_includes(self):

        top = Problem()
        top.root = ConvergeDiverge()

        sout = StringIO()

        recorder = DumpCaseRecorder(sout)
        recorder.options['includes'] = ['comp4.y1']
        top.driver.add_recorder(recorder)
        top.setup()
        top.run()

        expected = \
'''Iteration Coordinate: Driver/1
Params:
Unknowns:
  comp4.y1: 46.0
Resids:
  comp4.y1: 0.0
'''

        self.assertEqual( sout.getvalue(), expected )

    def test_includes_and_excludes(self):

        top = Problem()
        top.root = ConvergeDiverge()

        sout = StringIO()
        recorder = DumpCaseRecorder(sout)
        recorder.options['includes'] = ['comp4.*']
        recorder.options['excludes'] = ['*.y2']
        top.driver.add_recorder(recorder)
        top.setup()
        top.run()

        expected = \
'''Iteration Coordinate: Driver/1
Params:
  comp4.x1: 4.0
  comp4.x2: 21.0
Unknowns:
  comp4.y1: 46.0
Resids:
  comp4.y1: 0.0
'''

        self.assertEqual(sout.getvalue(), expected)

    def test_solver_record(self):

        top = Problem()
        top.root = ConvergeDiverge()
        sout = StringIO()
        recorder = DumpCaseRecorder(sout)
        top.root.nl_solver.add_recorder(recorder)

        top.setup()
        top.run()

        expected = \
'''Iteration Coordinate: Driver/1/root/1
Params:
  comp1.x1: 2.0
  comp2.x1: 8.0
  comp3.x1: 6.0
  comp4.x1: 4.0
  comp4.x2: 21.0
  comp5.x1: 46.0
  comp6.x1: -93.0
  comp7.x1: 36.8
  comp7.x2: -46.5
Unknowns:
  comp1.y1: 8.0
  comp1.y2: 6.0
  comp2.y1: 4.0
  comp3.y1: 21.0
  comp4.y1: 46.0
  comp4.y2: -93.0
  comp5.y1: 36.8
  comp6.y1: -46.5
  comp7.y1: -102.7
  p.x: 2.0
Resids:
  comp1.y1: 0.0
  comp1.y2: 0.0
  comp2.y1: 0.0
  comp3.y1: 0.0
  comp4.y1: 0.0
  comp4.y2: 0.0
  comp5.y1: 0.0
  comp6.y1: 0.0
  comp7.y1: 0.0
  p.x: 0.0
'''
        self.assertEqual(sout.getvalue(), expected)

    def test_sublevel_record(self):

        top = Problem()
        top.root = ExampleGroup()
        sout = StringIO()
        recorder = DumpCaseRecorder(sout)
        top.root.G2.G1.nl_solver.add_recorder(recorder)

        top.setup()
        top.run()

        expected = \
'''Iteration Coordinate: Driver/1/root/1/G2/1/G1/1
Params:
  C2.x: 5.0
Unknowns:
  C2.y: 10.0
Resids:
  C2.y: 0.0
'''
        self.assertEqual(sout.getvalue(), expected)

if __name__ == "__main__":
    unittest.main()
