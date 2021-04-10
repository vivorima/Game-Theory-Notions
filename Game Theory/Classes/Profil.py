class Profil:

    def __init__(self, list_strats):
        self.strats = list_strats
        self.gains = None

    def __repr__(self):
        if self.gains is not None:
            return str(self.strats) + " : " + str(self.gains)
        else:
            return str(self.strats)

    def ajouter_gain(self, listeGains):
        self.gains = listeGains

    def __eq__(self, other):
        """SI 2 PROFILS ONT LES MM STRATS DONC ILS SONT EGAUX"""
        return self.strats == other.strats and self.gains == self.gains

    def __hash__(self):
        return hash(tuple(self.strats))

    def __gt__(self, other):
        """ SI TOUS LES GAINS SONT > or == """

        for i in range(len(self.gains)):
            if self.gains[i] < other.gains[i]:
                return False
        return True

    def __lt__(self, other):
        """ SI TOUS LES GAINS SONT < ou =="""
        for i in range(len(self.gains)):
            if self.gains[i] > other.gains[i]:
                return False
        return True

    def gainEqual(self, other):
        """ SI TOUS LES GAINS SONT == """

        for i in range(len(self.gains)):
            if self.gains[i] != other.gains[i]:
                return False
        return True