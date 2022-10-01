from neuron.neuron import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    class SelfAddingUnit(Component):
        def __init__(self, living_dictionary: dict, name):
            super(SelfAddingUnit, self).__init__(living_dictionary, name=name)
            self.hidden = 0

        def function(self):
            self.hidden += 1
            self.output = self.hidden
            return self.output


    manager = Manager()
    Ina1 = NaIonComponent(manager, 'Ina1')
    Ikdr1 = NaIonComponent(manager, 'Ikdr1')
    soma1 = PRsomaNeuron(manager, 'soma1', 10.0)
    manager.link_output_input(soma1, Ina1, 'Vs')
    manager.link_output_input(Ina1, soma1, 'Ina')
    manager.link_output_input(soma1, Ikdr1, 'Vs')
    manager.link_output_input(Ikdr1, soma1, 'Ikdr')
    result = manager.start_stimulation(30)
    COMP4_RESULT = []
    COMP5_RESULT = []
    for dictionary in result:
        # COMP4_RESULT.append(dictionary['soma1'])
        COMP4_RESULT.append(dictionary['Ikdr1'])
    figure = plt.figure()
    plt.plot(COMP4_RESULT)
    plt.plot(COMP5_RESULT)
    figure.show()
    plt.show()
    print(result)