import uncertainpy as un
import chaospy as cp

from mitchell import mitchell

# Initialize the model
model = un.Model(run=mitchell,
                 labels=["Time (ms)", "Membrane potential (mV)"])

# Define a parameter dictionary
# parameters = {"alpha":0.1,
#               "K":8
#              }
parameters = {"IstimEnd":50000,
            #"IstimAmplitude":0.05,
            "IstimPeriod":500,
            "IstimPulseDuration":1,
            "tau_in":0.3,
            "tau_open":120.0, #75
            "tau_close": 150.0, #80
            "V_gate":0.13,
            "tau_out": 6.0}

# Create the parameters
parameters = un.Parameters(parameters)

# Set all parameters to have a uniform distribution
# within a 20% interval around their fixed value
parameters.set_all_distributions(un.uniform(0.2))

# Perform the uncertainty quantification
UQ = un.UncertaintyQuantification(model,
                                  parameters=parameters)
# We set the seed to easier be able to reproduce the result
data = UQ.quantify(seed=10, method="mc")
