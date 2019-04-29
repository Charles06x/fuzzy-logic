import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#Antecedents and consequents
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
command = ctrl.Consequent(np.arange(15, 26, 1), 'command')

#Memberships (custom)
    #Temperature memberships:
temperature['muy frio'] = fuzz.trapmf(temperature.universe, [0, 4, 6, 8])
temperature['frio'] = fuzz.trapmf(temperature.universe, [6, 10, 12, 16])
temperature['tibio'] = fuzz.trapmf(temperature.universe, [12, 16, 18, 24])
temperature['caliente'] = fuzz.trapmf(temperature.universe, [18, 22, 24, 32])
temperature['muy caliente'] = fuzz.trapmf(temperature.universe, [24, 28, 30, 41])

    #Humidity memberships:
humidity['baja'] = fuzz.gaussmf(humidity.universe, 0, 15)
humidity['optima'] = fuzz.gaussmf(humidity.universe, 50, 15)
humidity['alta'] = fuzz.gaussmf(humidity.universe, 100, 16)

    	#Command memberships:
command['enfriar'] = fuzz.trimf(command.universe, [15, 17, 20])
command['calentar'] = fuzz.trimf(command.universe, [18, 20, 26])

#Rules
rule1 = ctrl.Rule( (temperature['muy frio'] & humidity['baja']) |
                    (temperature['frio'] & humidity['baja']) |
                    (temperature['tibio'] & humidity['baja']) |
                    (temperature['muy frio'] & humidity['optima']) |
                    (temperature['frio'] & humidity['optima']) |
                    (temperature['muy frio'] & humidity['alta']),
                    command['calentar']
)

rule2 = ctrl.Rule( (temperature['muy caliente'] & humidity['baja']) |
                    (temperature['tibio'] & humidity['optima']) |
                    (temperature['caliente'] & humidity['optima']) |
                    (temperature['muy caliente'] & humidity['optima']) |
                    (temperature['tibio'] & humidity['alta']) |
                    (temperature['caliente'] & humidity['alta']) |
                    (temperature['muy caliente'] & humidity['alta']),
                    command['enfriar']
)

rule1.view()
rule2.view()
command_ctrl = ctrl.ControlSystem(rules=[rule1, rule2])

commandAction = ctrl.ControlSystemSimulation(command_ctrl)

commandAction.input['temperature'] = 17
commandAction.input['humidity'] = 10

commandAction.compute()

print(commandAction.output['command'])

command.view(sim=commandAction)

temperature.view()
humidity.view()
command.view()
plt.show()
