import aiohttp
from xoxxox.shared import Custom, LibLog

#---------------------------------------------------------------------------

class TttPrc:
  def __init__(self, config="xoxxox/config_tttlsv_cmm001", **dicprm):
    diccnf = Custom.update(config, dicprm)
    self.conlog = {}

  def status(self, config="xoxxox/config_tttlsv_cmm001", **dicprm):
    diccnf = Custom.update(config, dicprm)
    self.expert = diccnf["expert"]
    self.adrsrv = diccnf["adrsrv"]
    if not (self.expert in self.conlog):
      self.conlog[self.expert] = LibLog.getlog(diccnf["conlog"]) # LOG
      self.conlog[self.expert].catsys(diccnf) # LOG

  async def infere(self, txtreq):
    prompt = self.conlog[self.expert].catreq(txtreq) # LOG
    print("prompt[", prompt, "]", sep="", flush=True) # DBG
    dicreq = {
      "model": "local",
      "messages": prompt,
    }
    async with aiohttp.ClientSession() as s:
      async with s.post(
        self.adrsrv,
        json=dicreq,
        headers={"Content-Type": "application/json"},
      ) as r:
        r.raise_for_status()
        rawifr = await r.json()
    print("rawifr[", rawifr, "]", sep="", flush=True) # DBG
    txtifr = rawifr["choices"][0]["message"]["content"]
    print("txtifr[" + txtifr + "]", flush=True) # DBG
    txtres, txtopt = self.conlog[self.expert].arrres(txtifr) # LOG
    print("txtres[" + txtres + "]", flush=True) # DBG
    print("txtopt[" + txtopt + "]", flush=True) # DBG
    self.conlog[self.expert].catres(txtres) # LOG
    return (txtres, txtopt)
