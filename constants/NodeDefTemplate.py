#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""





class NodeDefTemplate() :

    prifix = '''
<nodeDefs>

'''

    suffix = '''

</nodeDefs>
'''

    nodeDef = '''
  <nodeDef id="irdevice" nls="irdevice">
    <sts>
      <st id="ST" editor="bool" />
	  </sts>
    <cmds>
      <sends />
      <accepts>
        <cmd id="COMMAND">
          <p id="BUTTON" editor="button" />
          <p id="CODE" editor="code" />
          <p id="CONNECTOR" editor="connector" />
          <p id="REPETE" editor="repete" />
        </cmd>
        <cmd id="STOP">
          <p id="CONNECTOR" editor="connector" />
        </cmd>
      </accepts>
    </cmds>
  </nodeDef>
    
'''

    # def __init__(self):
    #     print("init")

    def getNodeDef(self,  address: str, number: int) -> str:
        nls = self.nodeDef
        #button editor
        editor = "_25_0_R_0_" + str(number) + "_N_" + address
        replacment = '<p id="BUTTON" editor="' + editor + '" />'
        nls = nls.replace('<p id="BUTTON" editor="button" />', replacment)
        #nodeDef
        ndReplacment = '<nodeDef id="' + address +'" nls="irdevice">'
        nls = nls.replace('<nodeDef id="irdevice" nls="irdevice">', ndReplacment)
        return nls