import uncertainpy as un
import chaospy as cp

from hodgkin_huxley import HodgkinHuxley

# Define a parameter list
parameter_list = [["V_rest", -65, None],
                  ["Cm", 1, cp.Uniform(0.8, 1.5)],
                  ["gbar_Na", 120, cp.Uniform(80, 160)],
                  ["gbar_K", 36, cp.Uniform(26, 49)],
                  ["gbar_L", 0.3, cp.Uniform(0.13, 0.5)],
                  ["E_Na", 50, cp.Uniform(30, 54)],
                  ["E_K", -77, cp.Uniform(-74, -79)],
                  ["E_l", -50.613, cp.Uniform(-61, -43)],
                  ["m0", 0.0011, cp.Uniform(0.0005, 0.0016)],
                  ["n0", 0.0003, cp.Uniform(0.0001, 0.0005)],
                  ["h0", 0.9998, cp.Uniform(0.997, 0.9999)]]




# Create the parameters using that parameter list
parameters = un.Parameters(parameter_list)

# Set all parameters to have a uniform distribution
# within a 50% interval around their fixed value
parameters.set_all_distributions(un.uniform(0.2))

# Initialize the model
model = HodgkinHuxley()

# Initialize features
features = un.SpikingFeatures()

# Perform the uncertainty quantification
UQ = un.UncertaintyQuantification(model=model,
                                  parameters=parameters,
                                  features=features)
data = UQ.quantify()