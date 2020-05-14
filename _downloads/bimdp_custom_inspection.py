"""
Test the inspection of a normal (non-bi) Flow with a customized visualization.

This demonstrates how one can write custom TraceHTMLTranslator classes to
conveniently create rich visualizations with the BiMDP trace inspection.
"""

import numpy
import os
import matplotlib.pyplot as plt

import mdp
import bimdp


class CustomTraceHTMLConverter(bimdp.TraceHTMLConverter):
    """Custom TraceHTMLTranslator to visualize the SFA node output.

    This class also demonstrates how to use custom section_id values, and how
    to correctly reset internal variables via the reset method.
    """

    def __init__(self, flow_html_converter=None):
        super(CustomTraceHTMLConverter, self).__init__(
                                    flow_html_converter=flow_html_converter)
        self._sect_counter = None

    def reset(self):
        """Reset the section counter."""
        super(CustomTraceHTMLConverter, self).reset()
        self._sect_counter = 0

    def _write_data_html(self, path, html_file, flow, node, method_name,
                         method_result, method_args, method_kwargs):
        """Write the result part of the translation."""
        # check if we have reached the right node
        if isinstance(node, bimdp.BiNode) and (node.node_id == "sfa"):
            self._sect_counter += 1
            html_file.write("<h3>visualization (in section %d)<h3>" %
                            self._sect_counter)
            slide_name = os.path.split(html_file.name)[-1][:-5]
            image_filename = slide_name + "_%d.png" % self._sect_counter
            # plot the y result values
            plt.figure(figsize=(6, 4))
            ys = method_result
            for y in ys:
                plt.plot(y)
            plt.legend(["y sample %d" % (i+1) for i in range(len(ys))])
            plt.title("SFA node output")
            plt.xlabel("coordinate")
            plt.ylabel("y value")
            plt.savefig(os.path.join(path, image_filename), dpi=75)
            html_file.write('<img src="%s">' % image_filename)
        section_id = "%d" % self._sect_counter
        # now add the standard stuff
        super(CustomTraceHTMLConverter, self)._write_data_html(
                               path=path, html_file=html_file, flow=flow,
                               node=node, method_name=method_name,
                               method_result=method_result,
                               method_args=method_args,
                               method_kwargs=method_kwargs)
        return section_id


## Create the flow.
noisenode = mdp.nodes.NormalNoiseNode(input_dim=20*20,
                                      noise_args=(0, 0.0001))
sfa_node = bimdp.nodes.SFABiNode(input_dim=20*20, output_dim=10, dtype='f',
                                 node_id="sfa")
switchboard = mdp.hinet.Rectangular2dSwitchboard(
                                          in_channels_xy=100,
                                          field_channels_xy=20,
                                          field_spacing_xy=10)
flownode = mdp.hinet.FlowNode(mdp.Flow([noisenode, sfa_node]))
sfa_layer = mdp.hinet.CloneLayer(flownode, switchboard.output_channels)
flow = mdp.Flow([switchboard, sfa_layer])
train_data = [numpy.cast['f'](numpy.random.random((3, 100*100)))
              for _ in range(5)]
flow.train(data_iterables=[None, train_data])

## This is where the inspection happens.
html_converter = CustomTraceHTMLConverter()
# note that we could also specify a custom CSS file, via css_filename
tracer = bimdp.InspectionHTMLTracer(html_converter=html_converter)
filename, out = bimdp.show_execution(flow, x=train_data[0],
                                     tracer=tracer)

print "done."
