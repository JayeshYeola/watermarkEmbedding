from scipy import linalg
import SendereEnd

SendereEnd.main()
LL=SendereEnd.DWTofImage()
Uc, Sc, Vc = linalg.svd(LL)
#print "Sc :"
#print Sc
Alpha = SendereEnd.alpha
Wt=SendereEnd.GenScrambledWatermark()
Snew=Sc+Alpha*Wt
#print "Snew"
#print Snew
Uw,Sw,Vw = linalg.svd(Snew)

