import _thread

def split_list_1(lst, n):
    size, rest = divmod(len(lst), n)
    size = size + 1 if rest else size
    for i in range(n):
        yield lst[i*size:(i+1)*size]

def run_function(self, keys):
    for component in keys:
        self.living_dictionary[component].function()
    self.runing_thread_num -= 1


class Manager:
    def __init__(self):
        """
        link_dictionay: key is name of component, value is a list of inputs from different components.
        """
        self.living_dictionary = {}
        self.link_dictionary = {}
        self.record_list = []


    def start_stimulation(self, stimulation_step):
        """
        start stimulation.
        :return:
        """
        for step in range(stimulation_step):
            # if(step%1000==0):
            # print(step)
            # record history
            result_dictonary = {}
            for component in self.living_dictionary:
                result_dictonary[component] = self.living_dictionary[component].record()
            self.record_list.append(result_dictonary)

            # for every link between output and input
            for component in self.link_dictionary:
                input_list = self.link_dictionary[component]
                for inputs in input_list:
                    inputs: list
                    inputs.append(component.output)


            # run fuction
            for component in self.living_dictionary:
                self.living_dictionary[component].function()

        return self.record_list

    def start_stimulation_thread(self, stimulation_step, thread_num=8):
        """
        start stimulation.
        :return:
        """
        for step in range(stimulation_step):
            print(step)
            # record history
            result_dictonary = {}
            for component in self.living_dictionary:
                result_dictonary[component] = self.living_dictionary[component].record()
            self.record_list.append(result_dictonary)

            # for every link between output and input
            for component in self.link_dictionary:
                input_list = self.link_dictionary[component]
                for inputs in input_list:
                    inputs: list
                    inputs.append(component.output)


            # run fuction
            self.runing_thread_num = 0
            keys = self.living_dictionary.keys()
            keys = list(keys)
            for key_list in split_list_1(keys, thread_num):
                self.runing_thread_num += 1
                _thread.start_new_thread(run_function, (self, key_list))
            while self.runing_thread_num>0:
                pass

        return self.record_list

    def link_output_input(self, output_component, inputs_component, tab='add'):
        """
        add a link to manager.
        :param output_component:
        :param inputs_component:
        :return:
        """
        if not output_component in self.link_dictionary:
            self.link_dictionary[output_component] = [inputs_component.inputs]
        else:
            self.link_dictionary[output_component].append(inputs_component.inputs)
        inputs_component.inputs_tab.append(tab)


class Component:
    def __init__(self, manager, name='new component'):
        """
        init a component, and add it into living_dictionary with key of name
        :param living_dictionary: living_dictionary of manager
        """
        self.name = name
        manager.living_dictionary[name] = self # name must be different
        self.inputs = []
        self.inputs_tab = []
        self.output = 0

    def function(self):
        """
        add
        :return:
        """
        # todo clear before tans
        self.output = sum(self.inputs)
        return self.output

    def __forward__(self):
        return self.function()

    def record(self):
        return self.output
