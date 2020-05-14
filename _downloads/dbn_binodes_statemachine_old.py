"""
This is the binet version of the DBN,
based on Pietros non-binet DBN node implementation.
"""

import mdp
import bimdp
from dbn_nodes import DBNLayerNode


class DBNLayerBiNode(bimdp.BiNode, DBNLayerNode):
    """Adapter to turn the DBNLayerNode into a BiNode."""

    def __init__(self, node_id, hidden_dim, visible_dim=None, dtype=None):
        super(DBNLayerBiNode, self).__init__(node_id=node_id,
                                             hidden_dim=hidden_dim,
                                             visible_dim=visible_dim,
                                             dtype = dtype)
    
    def _is_bi_learning(self):
        return self._updown_initialized

    # v as the first argument is filled with the x value
    def _up_pass(self, v, epsilon=0.1, decay=0.0, momentum=0.0):
        v, pv, deltav = super(DBNLayerBiNode, self)._up_pass(
                                                v, epsilon, decay, momentum)
        # pv and deltav are currently not used,
        # but could be passed in the message
        return v
    
    # h has a different dimension than x, so have to transport it in message,
    # x is None, but is always given as the first argument
    def _down_pass(self, x, h, top_updates=0, epsilon=0.1, decay=0.0,
                   momentum=0.0):
        v, pv, deltav = super(DBNLayerBiNode, self)._down_pass(
                                    h, top_updates, epsilon, decay, momentum)
        # pv and deltav are currently not used
        return None, {"h": h}
        

class DBNMasterBiNode(bimdp.BiNode):
    """Node sits atop the DBN and manages the updown training phase."""
    
    def __init__(self, dbn_ids, sender_id, node_id="dbn_master",
                 input_dim=None, output_dim=None, dtype=None):
        """
        sender_id -- id of the sender node at the flow bottom.
        dbn_ids -- List with the ids of all the DBN node in the correct order.
        """
        self.dbn_ids = dbn_ids
        self.sender_id = sender_id
        super(DBNMasterBiNode, self).__init__(node_id=node_id,
                                              input_dim=input_dim,
                                              output_dim=input_dim,
                                              dtype=dtype)
        self.error = 0
        self._data_len = 0
        self._orig_x = None  # temporary storage for the error calculation
        self._status = "waiting"   # flag used for the phases during training
        self._iter_counter = 0
        
    def _bi_reset(self):
        self._orig_x = None
        self._status = "waiting"
        self._iter_counter = 0
        
    def _train(self, x, max_iter, min_error, msg, msg_x=None):
        """Manage the DBN learning loop."""
        if self._orig_x is None:
            # first time we reach this node for this data chunk
            self._orig_x = msg_x
            # start the up phase
            self._status = "up"
            for dbn_id in self.dbn_ids:
                msg[dbn_id + "->method"] = "up_pass"
            return self._orig_x, msg, self.sender_id
        elif self._status == "up":
            # start down phase
            self._status = "down"
            for dbn_id in self.dbn_ids:
                msg[dbn_id + "->target"] = -1
                msg[dbn_id + "->method"] = "down_pass"
            msg[self.sender_id + "->target"] = self.node_id
            msg[self.sender_id + "->no_x"] = True  # avoid x dimension error
            msg["h"] = x
            return None, msg, -1
        elif self._status == "down":
            del msg["h"]
            # do one normal execution for the error calculation
            self._status = "execute"
            return self._orig_x, msg, self.sender_id
        elif self._status == "execute":
            # get inverse for the error calculation
            self._status = "inverse"
            for dbn_id in self.dbn_ids:
                msg[dbn_id + "->method"] = "inverse"
            msg[self.sender_id + "->target"] = self.node_id
            msg[self.sender_id + "->no_x"] = True
            return x, msg, -1
        elif self._status == "inverse":
            # update error
            # TODO: this seems a little strange, use self._data_len?
            self.error = float(mdp.numx.absolute(self._orig_x - msg_x).sum())
            self._data_len += len(self._orig_x)
            self._iter_counter += 1
            if (self._iter_counter >= max_iter) or (self.error < min_error):
                # end iterations
                return
            else:
                # start next iteration with new up phase
                self._status = "up"
                for dbn_id in self.dbn_ids:
                    msg[dbn_id + "->method"] = "up_pass"
                return self._orig_x, msg, self.sender_id

            
@mdp.extension_method("html", DBNMasterBiNode, "_html_representation")
def master_html_representation(self):
    return (['phase: %s' % self._status,
             'iter counter: %d' % self._iter_counter,
             'error: %.5f' % self.error])


def get_DBN_flow(n_layers, hidden_dims):
    """Factory function for DBNs."""
    dbn_ids = []
    nodes = [bimdp.nodes.SenderBiNode(node_id="sender")]
    for i_layer in range(n_layers):
        dbn_ids.append("dbn_%d" % (i_layer+1))
        nodes.append(DBNLayerBiNode(node_id=dbn_ids[i_layer],
                                    hidden_dim=hidden_dims[i_layer]))
    nodes.append(DBNMasterBiNode(dbn_ids=dbn_ids,
                                 sender_id="sender",
                                 node_id="dbn_master"))
    return bimdp.BiFlow(nodes)   
