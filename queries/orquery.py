from .querycomponent import QueryComponent
from indexing import Index, Posting

from queries import querycomponent 

class OrQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    def get_postings(self, index : Index, tp) -> list[Posting]:
        result = self.components[0].get_postings(index, tp)
        # result = self.components[0].get_postings_without_positions(index)


        # TODO: program the merge for an OrQuery, by gathering the postings of the composed QueryComponents and
		# merging the resulting postings.
        # for c in self.components:
            
        doclists = []
        for comp in self.components[1:]:
            doclist = []
            posting = comp.get_postings(index, tp)

            temp = self._OrMerge(result, posting)
            result = temp
        # print('or merge ', result)
        return result


    def get_author_postings(self, soundex : Index) -> list[Posting]:
        result = self.components[0].get_author_postings(soundex)


        # TODO: program the merge for an OrQuery, by gathering the postings of the composed QueryComponents and
		# merging the resulting postings.
        # for c in self.components:
            
        doclists = []
        for comp in self.components[1:]:
            doclist = []
            posting = comp.get_author_postings(soundex)

            temp = self._OrMerge(result, posting)
            result = temp
        # print('or merge ', result)
        return result


    def _OrMerge(self, posting1, posting2):
        pos1 = pos2 = 0
        merged_result = []

        while pos1 < len(posting1) and pos2 < len(posting2):
            if posting1[pos1][0] == posting2[pos2][0]:
                pos1 += 1
                pos2 += 1
            elif posting1[pos1][0] < posting2[pos2][0]:
                    merged_result.append(posting1[pos1])
                    pos1 += 1
            else:
                merged_result.append(posting2[pos2])
                pos2 += 1
        
        while pos1 < len(posting1):
            merged_result.append(posting1[pos1])
            pos1+=1
        
        while pos2 < len(posting2):
            merged_result.append(posting2[pos2])
            pos2+=1
            
        return merged_result


    def __str__(self):
        return "(" + " OR ".join(map(str, self.components)) + ")"