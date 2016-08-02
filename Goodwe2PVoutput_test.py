import processData
import goodweData
import copy

class test:
   
   def do_tests( self):
      print "test_1"
      self.test_1()
      print "test_2"
      self.test_2()
      print "test_3"
      self.test_3()
      
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


if __name__ == "__main__":
   t = test()
   t.do_tests()
