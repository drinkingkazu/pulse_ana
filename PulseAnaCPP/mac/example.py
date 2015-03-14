import sys
from ROOT import gSystem
gSystem.Load("libpulse_ana_PulseAnaCPP")
from ROOT import sample

try:

    print "PyROOT recognized your class %s" % str(sample)

except NameError:

    print "Failed importing PulseAnaCPP..."

sys.exit(0)

