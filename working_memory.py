from ca.nengo.model.neuron.impl import ALIFSpikeGenerator
from ca.nengo.model.neuron.impl import ALIFNeuronFactory
from ca.nengo.model.nef.impl import NEFEnsembleFactoryImpl
from ca.nengo.math.impl import IndicatorPDF

# Get access to the Nengo objects using nef_core.py script
import nef

try:
    world.remove(network)
except:
    pass

# Create the network    
net=nef.Network('Working Memory')

# Set up a factory to generate neural populations of aLIF neurons
ef = NEFEnsembleFactoryImpl()
maxRate = IndicatorPDF(20,100)
intercept = IndicatorPDF(-1,1)
incAdapt = IndicatorPDF(.001,.200) #wide variety of adapt
nf = ALIFNeuronFactory(maxRate, intercept, incAdapt, .001, .020, .01) 
ef.setNodeFactory(nf);

#Make neural populations
Freq_pop = ef.make("Frequency", 200, 1)
Time_pop = ef.make("Time", 200, 1)
Mem_pop = ef.make("2D Memory", 100, 2)

net.add(Freq_pop)
net.add(Time_pop)
net.add(Mem_pop)

#Make the input, 500ms step function
input=net.make_input('Input',values=[0])
input.functions = [PiecewiseConstantFunction([.3,.8],[0,4,0])]

#Make the connections
net.connect(input,Freq_pop,weight=.1,pstc=.1)
net.connect(Freq_pop,Freq_pop,weight=1,pstc=.1)
net.connect(Freq_pop,Time_pop,weight=.1,pstc=.1)
net.connect(Time_pop,Time_pop,weight=1,pstc=.1)
net.connect(Freq_pop,Mem_pop,weight=1,index_pre=0,index_post=0,pstc=.1)
net.connect(Time_pop,Mem_pop,weight=1,index_pre=0,index_post=1,pstc=.1)

# render the network
net.add_to(world)

# add any probes
net.network.simulator.addProbe("2D Memory",Mem_pop,"X",True)


