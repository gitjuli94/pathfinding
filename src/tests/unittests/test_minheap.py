"""
Unit testing for minheap datastructure.
"""
import unittest
import sys
from pathlib import Path

# get the tested algorithm from a separate parent directory
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_dir))

from algorithms.minheap import MinHeapQueue

class TestMinHeap(unittest.TestCase):
    def setUp(self):
        pass

    def test_enqueue_adds_with_correct_priority(self):
        pq = MinHeapQueue()
        pq.enqueue("first", 1)
        pq.enqueue("second", 4)
        pq.enqueue("third", 3)

        expected = [(1, 'first'), (4, 'second'), (3, 'third')]

        self.assertEqual(pq.elements, expected)

    def test_dequeue_removes_and_returns_the_highest_priority_element(self):
        pq = MinHeapQueue()
        pq.enqueue("task1", 1)
        pq.enqueue("task2", 3)
        pq.enqueue("task3", 2)

        result = pq.dequeue()

        self.assertEqual(result, "task1")
        expected = [(2, "task3"), (3, "task2")]

        self.assertEqual(pq.elements, expected)

    def test_dequeue_returns_none_when_the_queue_is_empty(self):
        pq = MinHeapQueue()
        result = pq.dequeue()
        self.assertIsNone(result)

    def test_is_empty_true(self):
        pq = MinHeapQueue()
        self.assertTrue(pq.is_empty())

    def test_is_empty_false(self):
        pq = MinHeapQueue()
        pq.enqueue("task1", 1)
        self.assertFalse(pq.is_empty())

    def test_contains_true(self):
        pq = MinHeapQueue()
        pq.enqueue("task1", 1)
        self.assertTrue(pq.contains("task1"))

    def test_contains_false(self):
        pq = MinHeapQueue()
        pq.enqueue("task1", 1)
        self.assertFalse(pq.contains("task2"))

    def test_decrease_priority(self):
        pq = MinHeapQueue()
        pq.enqueue("task1", 3)
        pq.enqueue("task2", 1)
        pq.decrease_priority("task1", 0)

        expected = [(0, "task1"), (1, "task2")]

        self.assertEqual(pq.elements, expected)

    def test_decrease_priority_does_nothing_if_new_priority_is_higher(self):
        pq = MinHeapQueue()
        pq.enqueue("task1", 1)
        pq.enqueue("task2", 2)
        pq.decrease_priority("task1", 3)

        expected = [(1, "task1"), (2, "task2")]

        self.assertEqual(pq.elements, expected)

if __name__ == '__main__':
    unittest.main()
