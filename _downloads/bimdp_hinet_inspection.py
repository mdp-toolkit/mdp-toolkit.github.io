"""
Test the inspection of a normal (non-bi) Flow with the BiMDP inspection.

Since this requires the creation of files and opens them in a browser this
should not be included in the unittests.
"""

import numpy

import mdp
import bimdp

## Create the flow.
noisenode = mdp.nodes.NormalNoiseNode(input_dim=20*20,
                                      noise_args=(0, 0.0001))
sfa_node = mdp.nodes.SFANode(input_dim=20*20, output_dim=20, dtype='f')
sfa2_node = mdp.nodes.SFA2Node(input_dim=20, output_dim=10)
switchboard = mdp.hinet.Rectangular2dSwitchboard(
                                          in_channels_xy=100,
                                          field_channels_xy=20,
                                          field_spacing_xy=10)
flownode = mdp.hinet.FlowNode(noisenode + sfa_node + sfa2_node)
sfa_layer = mdp.hinet.CloneLayer(flownode, switchboard.output_channels)
flow = switchboard + sfa_layer

train_data = [numpy.cast['f'](numpy.random.random((10, 100*100)))
              for _ in range(5)]

## Do the inspections and open in browser.
# The debug=True is not needed here, unless one starts experimenting.
bimdp.show_training(flow=flow, data_iterables=[None, train_data],
                    debug=True)
filename, out = bimdp.show_execution(flow, x=train_data[0], debug=True)

print "done."
