from weak_schur import fitness


class Partition: 
    def __init__(self, partition = [[1,2], [3]]) -> None:
        self.partition = partition
        self._score = fitness(self.partition)

    @property
    def score(self):
        return self._score

    def add_element(self, elem : int, color : int) -> bool: 
        # If the partition specified is outside the number 
        # of partitions that we have, return False and 
        # add nothing.
        if color > len(self.partition): 
            print(f"Cannot add {elem} to subset {color}")
            return False

        # Otherwise, add it and update self._score 
        self.partition[color].append(elem); 
        self._score = fitness(self.partition)

        return True 

if __name__ == "__main__": 
    solution = Partition()
    print(solution.score)