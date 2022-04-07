class Partition:
    """
    This class pairs each potential solution with
    its score, which can be updated automatically with
    each call to add_element.
    """
    def __init__(self, partition = [[1,2], [3]] ) -> None:
        self.partition = deepcopy(partition)
        self.score = fitness(self.partition)

    def single_add(self, elem : int, color : int) -> bool:
        """Adds an element and automatically dynamically updates
        the fitness score of the partition.

        Args:
            elem (int): new number to add
            color (int): which partition to add it to

        Returns:
            bool: True if adding and updating score have
                  succeeded, False if we're adding to a
                  partition that doesn't exist.
        """
        # If the partition specified is outside the number
        # of partitions that we have, return False and
        # add nothing.
        if color > len(self.partition):
            print(f"Cannot add {elem} to subset {color}")
            return False

        # Otherwise, add it and update self._score
        # self.partition[color].append(elem)
        # Optimisation: sorted insert each time
        bisect.insort(self.partition[color], elem); 

        # We only need to verify the pairs that are
        # created by the addition of `elem`. All prior
        # information has already been stored in
        # self._score.

        # First for pairs of the type a + elem = b \in partition_i
        # then for pairs of the type a + b = elem \in partition_i
        # Note: We need to count each such pair only once! 
        #       So we use the or to do that job.  
        required = {}
        count = 0
        for idx in range(len(self.partition[color])): 
            if abs(elem - self.partition[color][idx]) in required: 
                count += 1
            else :
                required[self.partition[color][idx]] = idx
        self._score += count

        return True


#  @property
#     def partition(self):
#         """Getter method for the partition.
#         Prevents accidental modification.

#         Returns:
#             list: the partition
#         """
#         return self.partition

#     @property
#     def score(self):
#         """Getter method for the score of the partition.
#         Prevents accidental modification.

#         Returns:
#             int: the score of the partition
#         """
#         return self._score

#     @score.setter
#     def score(self, new_score: int) -> None:
#         """Setter method for the score of the partition.
#         Prevents accidental modification.

#         Returns:
#             int: the new score of the partition
#         """
#         self._score = new_score


# @dataclass
# class Partition: 
#     """
#     This class pairs each potential solution with
#     its score, which can be updated automatically with
#     each call to add_element.
#     """
#     partition: list[list[int]]
#     score : int = 0