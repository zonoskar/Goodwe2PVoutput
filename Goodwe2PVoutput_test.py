import processData
import goodweData
import copy
import processData2
import numpy as np
import matplotlib.pyplot as pl

class test:
   
   def do_tests( self):
      print "test_1"
      self.test_1()
      print "test_2"
      self.test_2()
      print "test_3"
      self.test_3()
      print "test_4"
      self.test_4()
      print "test_5"
      self.test_5()
      
   def test_1( self):
      gw1 = goodweData.goodweData('id="tab_big"><tr></tr><tr class=\"DG_Item\"><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0/1.0<c/td><td>1.0/1.0</td><td>1.0/1.0</td><td>1.0/1.0/1.0</td><td>1.0/1.0/1.0</td><td>1.0/1.0/1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0/1.0/1.0</td><td>1.0</td><td>1.0</td></tr>')

      gw1.m_inverter_sn = 1
      gw1.m_vpv[0] = 1.0
      gw1.m_vpv[1] = 1.0
      gw1.m_ipv[0] = 1.0
      gw1.m_ipv[1] = 1.0
      gw1.m_vac[0] = 1.0
      gw1.m_vac[1] = 1.0
      gw1.m_vac[2] = 1.0
      gw1.m_iac[0] = 1.0
      gw1.m_iac[1] = 1.0
      gw1.m_iac[2] = 1.0
      gw1.m_fac[0] = 1.0
      gw1.m_fac[1] = 1.0
      gw1.m_fac[2] = 1.0
      gw1.m_pgrid= 1.0
      gw1.m_eday = 1.0
      gw1.m_etotal= 1.0
      gw1.m_htotal= 1.0
      gw1.m_temperature= 1.0

      gw2 = copy.deepcopy(gw1)
      gw2.m_inverter_sn = 2
      gw3 = copy.deepcopy(gw1)
      gw3.m_inverter_sn = 3
      gw4 = copy.deepcopy(gw1)
      gw4.m_inverter_sn = 4
      gw5 = copy.deepcopy(gw1)
      gw5.m_inverter_sn = 5
      gw6 = copy.deepcopy(gw1)
      gw6.m_inverter_sn = 6
      gw10 = copy.deepcopy(gw1)

      gw10.m_inverter_sn = 10
      gw10.m_vpv[0] = 10.0
      gw10.m_vpv[1] = 10.0
      gw10.m_ipv[0] = 10.0
      gw10.m_ipv[1] = 10.0
      gw10.m_vac[0] = 10.0
      gw10.m_vac[1] = 10.0
      gw10.m_vac[2] = 10.0
      gw10.m_iac[0] = 10.0
      gw10.m_iac[1] = 10.0
      gw10.m_iac[2] = 10.0
      gw10.m_fac[0] = 10.0
      gw10.m_fac[1] = 10.0
      gw10.m_fac[2] = 10.0
      gw10.m_pgrid= 10.0
      gw10.m_eday = 10.0
      gw10.m_etotal= 10.0
      gw10.m_htotal= 10.0
      gw10.m_temperature= 10.0

      gw11 = copy.deepcopy(gw10)
      gw11.m_inverter_sn = 11

      gw12 = copy.deepcopy(gw10)
      gw12.m_inverter_sn = 12
      
      process = processData.processData(None)
      process.reset()
      print "State:" + process.state_to_string()
      process.processSample( gw1)
      print "State:" + process.state_to_string()
      process.processSample( gw2)
      print "State:" + process.state_to_string()
      process.processSample( gw3)
      print "State:" + process.state_to_string()
      process.processSample( gw4)
      print "State:" + process.state_to_string()
      process.processSample( gw10)
      print "State:" + process.state_to_string()
      process.processSample( gw11)
      print "State:" + process.state_to_string()
      process.processSample( gw5)
      print "State:" + process.state_to_string()
      process.processSample( gw6)
      print "State:" + process.state_to_string()
      process.processSample( gw12)
      print "State:" + process.state_to_string()
      process.reset()
      print "State:" + process.state_to_string()


   def test_2( self):
      with open('OfflineResponse.html', 'r') as f:
         response = f.read()
      
      gw1 = goodweData.goodweData(response)


   def test_3( self):
      with open('OnlineResponse.html', 'r') as f:
         response = f.read()
      
      gw1 = goodweData.goodweData(response)


   def test_4( self):
      proc = processData2.processData2(None)

      gw1 = goodweData.goodweData('id="tab_big"><tr></tr><tr class=\"DG_Item\"><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0/1.0<c/td><td>1.0/1.0</td><td>1.0/1.0</td><td>1.0/1.0/1.0</td><td>1.0/1.0/1.0</td><td>1.0/1.0/1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0/1.0/1.0</td><td>1.0</td><td>1.0</td></tr>')
      gw2 = copy.deepcopy(gw1)
      gw3 = copy.deepcopy(gw1)
      gw4 = copy.deepcopy(gw1)
      gw5 = copy.deepcopy(gw1)
      gw6 = copy.deepcopy(gw1)
      gw7 = copy.deepcopy(gw1)
      gw8 = copy.deepcopy(gw1)
      gw9 = copy.deepcopy(gw1)
      gw10 = copy.deepcopy(gw1)

      gw1.m_pgrid= 1.0
      gw2.m_pgrid= 2.0
      gw3.m_pgrid= 3.0
      gw4.m_pgrid= 4.0
      gw5.m_pgrid= 5.0
      gw6.m_pgrid= 6.0
      gw7.m_pgrid= 7.0
      gw8.m_pgrid= 8.0
      gw9.m_pgrid= 9.0
      gw10.m_pgrid= 10.0
      xx = []
      x = np.array([ 0,0,0,0,0,1.0,1.0,1.0,1.0,2.0,3.0,4.0,4.0,5.0,6.0,6.0,7.0,8.0,9.0,9.0,10.0,10.0,10.0,10.0,10.0,10.0,10.0,9.0,8.0,7.0,7.0,6.0,5.0,5.0,4.0,3.0,3.0,2.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])
      y = np.array([ 1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15, 16,  17,  18,  19,  20,  21,  22,  23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45])
      proc.processSample(gw1)
      xx.append(0)
      proc.processSample(gw1)
      xx.append(0)
      proc.processSample(gw1)
      xx.append(0)
      proc.processSample(gw1)
      xx.append(0)
      proc.processSample(gw2)
      xx.append(0)
      proc.processSample(gw3)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw4)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw4)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw5)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw6)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw6)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw7)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw8)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw9)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw9)
      xx.append(proc.getSample('pgrid'))

      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))

      proc.processSample(gw9)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw8)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw7)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw7)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw6)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw5)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw5)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw4)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw3)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw3)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw2)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      xx.append(1.0)
      xx.append(1.0)
      xx.append(1.0)
      xx.append(1.0)
      xx.append(1.0)
      xxx = np.array(xx)
      
      pl.figure()
      pl.plot(y,x)
      pl.plot(y,xxx)
      pl.show()


   def test_5( self):
      proc = processData2.processData2(None)

      gw1 = goodweData.goodweData('id="tab_big"><tr></tr><tr class=\"DG_Item\"><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0/1.0<c/td><td>1.0/1.0</td><td>1.0/1.0</td><td>1.0/1.0/1.0</td><td>1.0/1.0/1.0</td><td>1.0/1.0/1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0</td><td>1.0/1.0/1.0</td><td>1.0</td><td>1.0</td></tr>')
      gw2 = copy.deepcopy(gw1)
      gw3 = copy.deepcopy(gw1)
      gw4 = copy.deepcopy(gw1)
      gw5 = copy.deepcopy(gw1)
      gw6 = copy.deepcopy(gw1)
      gw7 = copy.deepcopy(gw1)
      gw8 = copy.deepcopy(gw1)
      gw9 = copy.deepcopy(gw1)
      gw10 = copy.deepcopy(gw1)

      gw1.m_pgrid= 15.0
      gw2.m_pgrid= 120.0
      gw3.m_pgrid= 300.0
      gw4.m_pgrid= 49.0
      gw5.m_pgrid= 500.0
      gw6.m_pgrid= 600.0
      gw7.m_pgrid= 70.0
      gw8.m_pgrid= 1800.0
      gw9.m_pgrid= 1900.0
      gw10.m_pgrid= 1054.0
      xx = []
      x = np.array([ 0,0,0,0,0,15.0,15.0,15.0,15.0,120.0,300.0,49.0,49.0,500.0,600.0,600.0,70.0,1800.0,1900.0,1900.0,1054.0,1054.0,1054.0,1054.0,1054.0,1054.0,1054.0,1900.0,1800.0,70.0,70.0,600.0,500.0,500.0,49.0,300.0,300.0,120.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0])
      y = np.array([ 1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15, 16,  17,  18,  19,  20,  21,  22,  23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45])
      proc.processSample(gw1)
      xx.append(0)
      proc.processSample(gw1)
      xx.append(0)
      proc.processSample(gw1)
      xx.append(0)
      proc.processSample(gw1)
      xx.append(0)
      proc.processSample(gw2)
      xx.append(0)
      proc.processSample(gw3)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw4)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw4)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw5)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw6)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw6)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw7)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw8)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw9)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw9)
      xx.append(proc.getSample('pgrid'))

      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw10)
      xx.append(proc.getSample('pgrid'))

      proc.processSample(gw9)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw8)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw7)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw7)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw6)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw5)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw5)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw4)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw3)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw3)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw2)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      proc.processSample(gw1)
      xx.append(proc.getSample('pgrid'))
      xx.append(1.0)
      xx.append(1.0)
      xx.append(1.0)
      xx.append(1.0)
      xx.append(1.0)
      xxx = np.array(xx)
      print x
      print xxx
      
      pl.figure()
      pl.plot(y,x)
      pl.plot(y,xxx)
      pl.show()

if __name__ == "__main__":
   t = test()
   t.do_tests()
