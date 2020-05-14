import unittest
import mdp
import bimdp
import mdp.nodes as mn

from dbn_nodes import DBNLayerNode
import dbn_binodes

from mdp.test import testing_tools
from mdp.test.testing_tools import assert_array_almost_equal, assert_array_equal, \
     assert_almost_equal, assert_equal, assert_array_almost_equal_diff, \
     assert_type_equal

class DBNLayerTestCase(unittest.TestCase):
    def _test_updown_stability(self):
        """Test that the updown phase does not change optimal greedy weights.
        """

        # number of visible and hidden units
        I, J = 8, 2

        # create DBNLayer node
        node = DBNLayerNode(J, I)
        node._rbm._init_weights()
        # init to random model
        node._rbm.w = mdp.utils.random_rot(max(I,J), dtype='d')[:I, :J]
        node._rbm.bv = mdp.numx_rand.randn(I)
        node._rbm.bh = mdp.numx_rand.randn(J)

        # Gibbs sample to reach the equilibrium distribution
        N = 1e4
        v = mdp.numx_rand.randint(0,2,(N,I)).astype('d')
        for k in range(100):
            #if k%5==0: spinner()
            p, h = node._rbm._sample_h(v)
            p, v = node._rbm._sample_v(h)

        # greedy learning phase (it shouldn't change the weights by much,
        # since the input is already taken from the equilibrium distr)
        for k in range(100):
            #if k%5==0: spinner()
            node.train(v)
        node.stop_training()
        
        # save original weights
        real_w = node._rbm.w.copy()
        real_bv = node._rbm.bv.copy()
        real_bh = node._rbm.bh.copy()

        # up-down training
        node._init_updown()
        for k in range(100):
            h, ph, deltah = node._up_pass(v)
            _, _, deltav = node._down_pass(h)
            #print k, deltah, deltav

        assert_array_almost_equal(real_w, node.w_rec, 2)
        assert_array_almost_equal(real_w, node.w_gen, 2)
        assert_array_almost_equal(real_bv, node.bv, 2)
        assert_array_almost_equal(real_bh, node.bh, 2)

    def _test_updown_learning(self):
        """Test that DBNLayer is able to learn by up-down passes alone."""
        
        # number of visible and hidden units
        I, J = 4, 2
        
        node = DBNLayerNode(J, I)

        # the observations consist of two disjunct patterns that
        # never appear together
        N = 10000
        v = mdp.numx.zeros((N,I))
        for n in range(N):
            r = mdp.numx_rand.random()
            if r>0.666: v[n,:] = [0,1,0,1]
            elif r>0.333: v[n,:] = [1,0,1,0]

        # fake to train the node with a very short greedy phase
        node.train(v[:1,:])
        node.stop_training()
        # start up-down phase
        node._init_updown()

        for k in range(1500):
            #if k%5==0: spinner()
            if k>5:
                mom = 0.9
                eps = 0.2
            else:
                mom = 0.5
                eps = 0.5
            h, ph, deltah = node._up_pass(v, epsilon=eps, momentum=mom)
            rec_v, rec_pv, deltav = node._down_pass(h, epsilon=eps, momentum=mom)
            train_err = float(((v-rec_v)**2.).sum())
            #print k, train_err, train_err/N, deltah, deltav
            if train_err/N<0.1: break

        assert train_err/N<0.1

class DBNTestCase(unittest.TestCase):
    # TODO: what to do with this test?
#     def test_all_dbnlayer(self):
#         """Test that all nodes are DBNLayers"""
#         flow = [DBNLayerNode(10),
#                 mn.PCANode(input_dim=10, output_dim=20),
#                 DBNLayerNode(30)]
#         # this works
#         mdp.Flow(flow)
#         # this doesn't
#         self.assertRaises(DBNFlowException, DBNFlow, flow)

    # TODO: test updown phase where the iterable runs out

    # TODO: test updown phase for stop criterions becoming true

    # TODO: test convergence of epsilon, decay, momentum

    # TODO: test learning with multiple layers

    def test_factory_arguments(self):
        self.assertRaises(dbn_binodes.DBNException,
                          dbn_binodes.get_DBN_flow, 3, [1,2])
        self.assertRaises(dbn_binodes.DBNException,
                          dbn_binodes.get_DBN_flow, 3, [1,2,3,4])
        self.assertRaises(dbn_binodes.DBNException,
                          dbn_binodes.get_DBN_flow, 1, 2)

    def test_one_node_updown(self):
        """Test flow updown phase with just one node."""
        flow = dbn_binodes.get_DBN_flow(1, hidden_dims=[2])
        N = 10000
        x = mdp.numx.zeros((N, 4))
        for i in range(N):
            r = mdp.numx.rand()
            if r>0.666:
                x[i,:] = [0.,1.,0.,1.]
            elif r>0.333:
                x[i,:] = [1.,0.,1.,0.]

        def data_gen():
            for _ in range(100):
                # (data, learning rate, decay, momentum)
                yield (x, 0.5, 0., 0.5)

        flow.train([data_gen()])
        print flow[0].w_gen

        flow.updown_phase([x], epsilon=0.5,
                          decay=0., momentum=0.5, n_updates=3,
                          max_iter=300, min_error=1e-2)
        print flow[0].w_gen
        
        error = flow.updown_phase([x], epsilon=0.1,
                                  decay=0., momentum=0.9, n_updates=3,
                                  max_iter=1000, min_error=0.05)

        assert error < 0.05

    def test_training_finished_before_updown(self):
        flow = DBNFlow([DBNLayerNode(5), DBNLayerNode(2)])
        self.assertRaises(DBNFlowException, flow.updown_phase, None)        

    def test_updown_phase_functionality(self):
        N, I, J = 100, 5, 2
        flow = DBNFlow([DBNLayerNode(I), DBNLayerNode(J)])
        
        v = mdp.numx_rand.randint(0,2,size=(N,I)).astype('d')
        flow.train(v)
        flow.updown_phase(v, max_iter=10)
        h = flow.execute(v)
        v = flow.inverse(h)

if __name__ == "__main__":
    unittest.main()

