#encoding: utf-8

def valid_tema(termo, curr_year):
	return not termo.isnumeric() and "código" not in termo.lower() and "número" not in termo.lower() and curr_year == 1999 and termo != ''

def valid_year(ano):
	try:
		return int(ano) in range(1999, 2020)
	except:
		return False
def load_file(): 
	lines = []
	ipcs = set()
	curr_year = 2019

	with open("metrica.csv") as metrica:
		linhas = metrica.readlines()
		curr_tema = linhas[0].split(",")[0]
		for linha in range(len(linhas)):
			curr_line = linhas[linha].split(",")
			curr_tema = curr_line[0] if valid_tema(curr_line[0], curr_year) else curr_tema
			curr_year = int(curr_line[0]) if valid_year(curr_line[0])  else curr_year

			if("código" in curr_line[0].lower()):
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
					tema[curr_year][curr_line[i]] = values[i]	
	
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
	temas = load_file()[0]
	print_csv(temas)


def print_csv(collection):

	with open("result.csv", "w") as f:
		f.write("ano/tema"+",".join(list(collection[0][2019].keys())))
		for tema in collection:
				for ano in filter(lambda x: str(x).isnumeric(), tema.keys()):
					writeable = tema["tema"]+"_"+str(ano) +","
					writeable = writeable + ",".join(map(str,tema[ano].values()))
					f.write(writeable)
			
		

main()
