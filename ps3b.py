# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab

''' 
Begin helper code
'''
class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """
'''
End helper code
'''


# PROBLEM 1
class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """

    def __init__(self, max_birth_prob, clear_prob):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        max_birth_prob: Maximum reproduction probability (a float between 0-1)        
        clear_prob: Maximum clearance probability (a float between 0-1).
        """
        self.max_birth_prob = max_birth_prob
        self.clear_prob = clear_prob

    def getmaxbirthprob(self):
        """
        Returns the max birth probability.
        """
        return self.max_birth_prob

    def getclearprob(self):
        """
        Returns the clear probability.
        """
        return self.clear_prob

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.getclearprob and otherwise returns
        False.
        """
        if self.getclearprob() >= random.random():
            return True
        else:
            return False

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        if self.getmaxbirthprob() * (1 - pop_density) >= random.random():
            return SimpleVirus(self.getmaxbirthprob(), self.getclearprob())
        else:
            raise NoChildException()


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, max_pop):
        """
        Initialization function, saves the viruses and max_pop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        max_pop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.max_pop = max_pop

    def getviruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getmaxpop(self):
        """
        Returns the max population.
        """
        return self.max_pop

    def gettotalpop(self):
        """
        Gets the size of the current total virus population.
        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update()

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """

        for i in self.viruses:
            if i.doesClear():
                self.viruses.remove(i)

        pop_density = float(len(self.viruses) / self.max_pop)

        for i in self.viruses:
            try:
                # self.viruses.append(i.reproduce(pop_desity))
                self.viruses.append(i.reproduce(pop_density))
            except NoChildException:
                pass

        return self.gettotalpop()


# PROBLEM 2
def simulationwithoutdrug(num_viruses, max_pop, max_birth_prob, clear_prob, num_trials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    num_viruses: number of SimpleVirus to create for patient (an integer)
    max_pop: maximum virus population for patient (an integer)
    max_birth_prob: Maximum reproduction probability (a float between 0-1)        
    clear_prob: Maximum clearance probability (a float between 0-1)
    num_trials: number of simulation runs to execute (an integer)
    """
    viruses = []
    results = []

    # Run simulation
    for viruses_created in range(num_viruses):
        viruses.append(SimpleVirus(max_birth_prob, clear_prob))
    for trials in range(num_trials):
        current_patient = Patient(viruses, max_pop)
        for i in range(300):
            try:
                results[i] += current_patient.update()
            except:
                results.append(current_patient.update())

    # Plot graph of Number of Viruses vs Time Steps
    pylab.figure('Without Drugs')
    pylab.plot(range(300), [x / num_trials for x in results])
    pylab.title('Viruses vs Time')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Number of Viruses')
    pylab.legend()
    pylab.show()


# PROBLEM 3
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, max_birth_prob, clear_prob, resistances, mut_prob):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        max_birth_prob: Maximum reproduction probability (a float between 0-1)

        clear_prob: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mut_prob: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self, max_birth_prob, clear_prob)
        self.resistances = resistances
        self.mut_prob = mut_prob

    def getresistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getmutprob(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mut_prob

    def isresistantto(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getresistpop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        if drug in self.resistances:
            return self.resistances.get(drug)
        else:
            return False

    def reproduce(self, pop_density, active_drugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in active_drugs, then the virus reproduces with probability:

        self.max_birth_prob * (1 - pop_density).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        pop_density: the population density (a float), defined as the current
        virus population divided by the maximum population

        active_drugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        max_birth_prob and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        for drug in active_drugs:
            if not self.isresistantto(drug):
                raise NoChildException

        if self.getmaxbirthprob() * (1 - pop_density) >= random.random():
            resistances_copy = dict.copy(self.getresistances())

            for types in resistances_copy:
                if self.getmutprob() <= random.random():
                    resistances_copy[types] = False
                else:
                    resistances_copy[types] = True

            return ResistantVirus(self.getmaxbirthprob(), self.getclearprob(), resistances_copy, self.getmutprob())
        else:
            raise NoChildException()


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, max_pop):
        """
        Initialization function, saves the viruses and max_pop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: The list representing the virus population (a list of
        virus instances)

        max_pop: The  maximum virus population for this patient (an integer)
        """

        super().__init__(viruses, max_pop)
        self.Presciptions = []

    def addprescription(self, new_drug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        new_drug is already prescribed to this patient, the method has no effect.

        new_drug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        if new_drug not in self.Presciptions:
            self.Presciptions.append(new_drug)

    def getprescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.Presciptions

    def getresistpop(self, drug_resist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drug_resist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        pop_of_viruses_with_resistances = 0

        if not drug_resist:
            return pop_of_viruses_with_resistances

        for virus in self.viruses:
            len_of_drug_resist = len(drug_resist)
            for drug in drug_resist:
                if virus.isresistantto(drug):
                    len_of_drug_resist -= 1
                else:
                    break
            if len_of_drug_resist == 0:
                pop_of_viruses_with_resistances += 1

        return pop_of_viruses_with_resistances

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        for i in self.viruses:
            if i.doesClear():
                self.viruses.remove(i)

        pop_desity = float(len(self.viruses) / self.max_pop)

        for i in self.viruses:
            try:
                self.viruses.append(i.reproduce(pop_desity, self.getprescriptions()))
            except NoChildException:
                pass

        return self.gettotalpop() + self.getresistpop(self.getprescriptions())


# PROBLEM 4
def simulationwithdrug(num_viruses, max_pop, max_birth_prob, clear_prob, resistances,
                       mut_prob, num_trials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    num_viruses: number of ResistantVirus to create for patient (an integer)
    max_pop: maximum virus population for patient (an integer)
    max_birth_prob: Maximum reproduction probability (a float between 0-1)
    clear_prob: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mut_prob: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    num_trials: number of simulation runs to execute (an integer)

    """

    viruses = []
    results = []
    results2 = []

    for viruses_created in range(num_viruses):
        viruses.append(ResistantVirus(max_birth_prob, clear_prob, resistances, mut_prob))
    for trials in range(num_trials):
        current_patient = TreatedPatient(viruses, max_pop)
        for i in range(300):
            if i == 150:
                current_patient.addprescription('guttagonol')
            try:
                results[i] += current_patient.update()
                results2[i] += float(current_patient.getresistpop(['guttagonol']))
            except:
                results.append(current_patient.update())
                results2.append(float(current_patient.getresistpop(['guttagonol'])))

    pylab.figure('Without Drugs')
    pylab.plot(range(300), [x / num_trials for x in results])
    pylab.plot(range(300), [y / num_trials for y in results2])
    pylab.title('Viruses vs Time')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Number of Viruses')
    pylab.legend()
    pylab.show()

# Example of Simulation
simulationwithdrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 10)