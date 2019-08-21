#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by Andre Ribas
# 2.0 20/08/2019 - Excluindo discos que nao sao fixos
# 1.3 19/08/2019 - Corrigido perf sem disco
# 1.2 17/06/2019 - Corrigido unidades com erro valor
# 1.1 06/05/2019 - Corrigido perf
# 1.0 25/03/2019 - Correcao status OK e version
# 0.0 28/12/2018
ver=2.0
import datetime
import sys
import json
import os
import subprocess
from optparse import OptionParser

def main():
    parser = OptionParser(usage="usage: %prog [options] filename",
                        version="%prog 1.0")
    parser.add_option("-H", "--srvip", dest="srvip",
                      help="Informar Servidor")
    parser.add_option("-t", "--keyncpa", dest="keyncpa",
                      help="Informar Tipo de Monitoracao")
    parser.add_option("-p", "--port", dest="port",
                      help="Informacoes adicionais")
    parser.add_option("-v", "--versionso", dest="versionso",
                      help="Informacoes SO")
    parser.add_option("-x", "--exclude", dest="exclude",
                      help="Unidades Excluidas")
    parser.add_option("-w", "--warning", dest="warning",
                      help="Informacoes adicionais")
    parser.add_option("-c", "--critical", dest="critical",
                      help="Informacoes adicionais")
    (options, args) = parser.parse_args()

    disk_all( server=options.srvip, chave=options.keyncpa, porta=options.port, sop=options.versionso, exclude=options.exclude, warn=int(options.warning), crit=int(options.critical) )

def convbit(size):
    power = 2**10
    n = 1
    Dic_powerN = {1:'KB', 2:'MB', 3:'GB', 4:'TB'}
    if size <= power**2 :
        size /=  power
        #return size
        res = "%s %s" %(size, Dic_powerN[n])
        return res
        #return size, Dic_powerN[n]
    else:
        while size   >  power :
            n  += 1
            size /=  power**n
            res = "%s %s" %(size, Dic_powerN[n])
            #return size, Dic_powerN[n]
            return res
    
def disk_all( server, chave, porta, sop, exclude, warn, crit ):
	command = "/usr/local/nagios/libexec/check_ncpa.py -H %s -t %s -P %s -M 'disk/logical' -l" %(server, chave, porta)
	valor = subprocess.check_output(command, shell=True)
	item_dict = json.loads(valor)
	saida=0
	unidades = ""
	perf = ""
	uniderr = ""
	chave = []
	status = "OK"
	for x, y in item_dict.iteritems():
		for a, b in y.iteritems():
			if sop == 'windows' :
				unid = a.replace('|','')
			elif sop == 'linux' :
				unid = a.replace('|','/')
			unidtsts = b['used_percent'][0]
			tunid = b['opts']
			try:
				vlrdisk = int(unidtsts)
			except:
				vlrdisk = 0
			unidex = exclude.find(unid)
			if sop == 'windows' and tunid == 'rw,fixed':
				valid=0
			elif sop == 'linux' :
				valid=0
			else:
				valid=1
			if unidex < 0 and unid != 'C:' and unid != '/' and valid == 0:
				if vlrdisk > crit :
					saida=2
					status="CRITICAL"
					uniderr += "%s= %s%%, " %(unid, vlrdisk)
				elif vlrdisk >= warn:
					if saida < crit :
						saida=1
						status="WARNING"
						uniderr += "%s= %s%%, " %(unid, vlrdisk)
					else :
						uniderr += "%s= %s%%, " %(unid, vlrdisk)
				elif saida < 1 : 
					saida=0
					status="OK"
				unidades += "%s %s%%, " %(unid, vlrdisk)
				perf += "%s=%s;%s;%s; " %(unid, vlrdisk, warn, crit)
	if saida > 0 :
		mens2 = uniderr
	else :
		mens2 = unidades
	if len(mens2) < 1 :
		mens2 = "Sem discos adicionais"
		perf = "disk=0;0;0"
	mens = "%s - %s\nversao=%s |%s" %(status, mens2, ver, perf)
	print mens
	sys.exit(saida)
	return;

if __name__ == '__main__':
    main()
