# -*- coding: utf-8 -*-
# Generated by codesnippet sphinx extension on 2020-05-14

import mdp
import numpy as np
np.random.seed(0)
import bimdp
class NewtonNode(bimdp.nodes.IdentityBiNode):
    """Node to implement gradient descent with the Newton method.

    :param sender_id: id of the SenderBiNode that is at the front of
      the flow, or at the point where the x value should be optimized.
    """
    def __init__(self, sender_id, **kwargs):
        self.sender_id = sender_id
        super(NewtonNode, self).__init__(**kwargs)

    @bimdp.binode_coroutine(["grad", "msg_x", "msg"])
    def _newton(self, y_goal, n_iterations, x_start, msg):
        """Try to reach the given y value with gradient descent.

        The Newton method is used to calculate the next point.
        """
        # can't use function decorator, since this is a coroutine
        with mdp.extension("gradient"):
            # get the y value for the output
            msg = {self.node_id + "->method": "newton", "method": "gradient"}
            y, grad, x, _ = yield x_start, msg.copy(), self.sender_id
            for _ in xrange(n_iterations):
                # use Newton's method to get the new data point
                error = np.sum((y - y_goal) ** 2, axis=1)
                error_grad = np.sum(2 * (y - y_goal)[:,:,np.newaxis] * grad,
                                    axis=1)
                err_grad_norm = np.sqrt(np.sum(error_grad**2, axis=1))
                unit_error_grad = error_grad / err_grad_norm[:,np.newaxis]
                # x_{n+1} = x_n - f(x_n) / f'(x_n)
                x = x - (error / err_grad_norm)[:,np.newaxis] * unit_error_grad
                y, grad, x, _ = yield x, msg.copy(), self.sender_id
            raise StopIteration(x, None, "exit")

n_iterations = 3
show_inspection = True

sfa_node = bimdp.nodes.SFA2BiNode(input_dim=4*4, output_dim=5)
switchboard = bimdp.hinet.Rectangular2dBiSwitchboard(
                                in_channels_xy=8,
                                field_channels_xy=4,
                                field_spacing_xy=2)
flownode = bimdp.hinet.BiFlowNode(bimdp.BiFlow([sfa_node]))
sfa_layer = bimdp.hinet.CloneBiLayer(flownode,
                                     switchboard.output_channels)
flow = bimdp.BiFlow([switchboard, sfa_layer])
train_data = [np.random.random((10, switchboard.input_dim))
              for _ in range(3)]
flow.train([None, train_data])

sender_node = bimdp.nodes.SenderBiNode(node_id="sender", recipient_id="newton")
newton_node = NewtonNode(sender_id="sender", input_dim=sfa_layer.output_dim,
                         node_id="newton")
flow = sender_node + flow + newton_node

x_goal = np.random.random((2, switchboard.input_dim))
goal_y, msg = flow.execute(x_goal)

x_start = np.random.random((2, switchboard.input_dim))
y_start, _ = flow.execute(x_start)

msg = {"method": "newton", "n_iterations": n_iterations, "x_start": x_start}
if show_inspection:
    _, (x, msg) = bimdp.show_execution(flow, x=goal_y, msg=msg, target="newton")
else:
    x, msg = flow.execute(goal_y, msg, "newton")

y, _ = flow.execute(x)
print ("errors before optimization: %s" %
       np.sum((y_start - goal_y)**2, axis=1))
# Expected:
## errors before optimization: [ 196.49202899  241.31524993]
print ("errors after optimization  : %s" %
       np.sum((y - goal_y)**2, axis=1))
# Expected:
## errors after optimization  : [ 39.01372025  34.84160123]
