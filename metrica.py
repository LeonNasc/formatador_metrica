#encoding: utf-8

def valid_tema(termo, curr_year):
	return not termo.isnumeric() and "codigo" not in termo.lower() and "número" not in termo.lower() and curr_year == 1999 and termo != ''

def valid_year(ano):
	try:
		return int(ano) in range(1999, 2020)
	except:
		return False
    
def load_file(file): 
	lines = []
	ipcs = set()
	curr_year = 2019

	with open(file) as metrica:
		linhas = metrica.readlines()
		curr_tema = linhas[0].split(";")[0]
		for linha in range(len(linhas)):
            print("a")
			curr_line = linhas[linha].split(";")
			curr_tema = curr_line[0] if valid_tema(curr_line[0], curr_year) else curr_tema
			curr_year = int(curr_line[0]) if valid_year(curr_line[0])  else curr_year

			if("codigo" in curr_line[0].lower()):
				ipcs.update(map(lambda x:x.strip(),curr_line[1:])) # atualiza o conjunto dos IPCS

				tema = {}
				tema["tema"] = curr_tema
				
				for tema_guardado in lines: 
					if tema_guardado["tema"] == curr_tema:
						tema = tema_guardado	
						lines.remove(tema_guardado)

				tema[curr_year] = {}
				values = linhas[linha+1].split(",")

				for i in range(1,len(curr_line[1:])):
					tema[curr_year][curr_line[i]] = values[i] if i<len(values) else 0
	
				lines.append(tema)

	lines = fill_ipcs(lines, ipcs)

	return (lines, ipcs)


def fill_ipcs(lista, ipcs):
	for i in range(0,len(lista)):
		for ano in range(1999, 2020):
			for codigo in ipcs:
				if codigo not in lista[i][ano]:
					try:
						lista[i][ano][codigo] = 0
					except:
						pass

	return lista


def main():
    temas1, ipcs1 = load_file("ipcs_industrial.csv")
    temas2, ipcs2 = load_file("ipcs_academicos.csv")
    
    ipcs = ipcs1 | ipcs2
    print_csv(temas2, ipcs)
    print_csv(temas1, ipcs)


def print_csv(collection, temas):

	with open("result_1.csv", "a") as f:
		primeira_linha = sorted(list(temas))
		f.write("ano/tema,"+",".join(primeira_linha) + "\r\n")
		for tema in collection:
				for ano in filter(lambda x: str(x).isnumeric(), tema.keys()):
					atual = dict(sorted(tema[ano].items()))
					writeable = tema["tema"]+"_"+str(ano) +","
					writeable = writeable + ",".join(map(str,atual.values()))
					f.write(writeable + "\r\n")
			
		

main()
