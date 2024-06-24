from heapq import heappush, heappop

class MinHeapQueue:
    """
    A data structure using binary min heap for queueing elements
    """
    def __init__(self):
        self.elements = []

    def enqueue(self, item, priority):
        # add new element with a priority
        heappush(self.elements, (priority, item))

    def dequeue(self):
        # remove and return the element with the highest priority (root)
        if not self.is_empty():
            return heappop(self.elements)[1]
        else:
            return None

    def is_empty(self):
        return not self.elements

    def contains(self, item):
        return any(element[1] == item for element in self.elements)

    def decrease_priority(self, item, priority):
        for i, (p, element) in enumerate(self.elements):
            if element == item:
                if p > priority:
                    del self.elements[i]
                    heappush(self.elements, (priority, item))
                break

