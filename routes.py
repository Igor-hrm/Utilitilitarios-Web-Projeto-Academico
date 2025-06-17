from main import app
from flask import render_template, request, jsonify

@app.route("/")
def render_index():
    return render_template("index.html")

@app.route("/validadorcpf")
def render_validarcpf():
    return render_template("validadorcpf.html")

@app.route("/geradordecpf")
def render_geradordecpf():
    return render_template("geradordecpf.html")

@app.route("/geradordesenha")
def render_geradordesenha():
    return render_template("geradordesenha.html")

@app.route("/conversordemoedas")
def render_conversordemoedas():
    return render_template("conversordemoedas.html")
''' Abaixo estão as funções responsaveis por gerar algo em um HTML'''


@app.route("/validarcpf", methods=["POST"])
def validarcpf():
    cpf = request.form["validarcpf"]

    if cpf == '':
        return render_template("validadorcpf.html", cpfvalido='')

    cpf = cpf.strip()
    cpf_format = cpf.replace('.','').replace('-','')

    if not cpf_format.isdecimal():
        cpfvalido = f'O CPF é inválido'
        return render_template("validadorcpf.html", cpfvalido=cpfvalido)
    
    if len(cpf_format) != 11:
        cpfvalido = f'O CPF {cpf} é inválido'
        return render_template("validadorcpf.html", cpfvalido=cpfvalido)
    
    cpf9 = cpf_format[:9]
        #calcular primeiro digito
    cpf_soma1 = 0
    for i,n in enumerate(cpf9):
        cpf_soma1 += int(n) * (10-i)
            
    cpf_soma1 *= 10

    resto_cpf1 = cpf_soma1 % 11

    if resto_cpf1 > 9:
        primeiro_digito = 0 
    else:
         primeiro_digito = resto_cpf1

    #calcular o segundo digito

    cpf10 = cpf_format[:9] + str(primeiro_digito)
    cpf_soma2 = 0

    for i,n in enumerate(cpf10):
        cpf_soma2 += int(n) * (11-i)

            
    cpf_soma2 *= 10

    resto_cpf2 = cpf_soma2 % 11

    if resto_cpf2 > 9:
        segundo_digito = 0 
    else:
        segundo_digito = resto_cpf2

    dois_ultimos = str(primeiro_digito) + str(segundo_digito)
            
    if cpf_format[-2:] == dois_ultimos:
        cpfvalido = f'O CPF {cpf} é válido'
        return render_template("validadorcpf.html", cpfvalido=cpfvalido)
         
    cpfvalido = f'O CPF {cpf} é inválido'
    return render_template("validadorcpf.html", cpfvalido=cpfvalido)

@app.route("/gerarsenha", methods=["POST"])
def gerarsenha():
    from random import choice as ch

    tamanho_senha = request.form["slide"]

    tamanho_senha = int(tamanho_senha)
    if 50 <= tamanho_senha <= 1:
        return render_template("geradordesenha.html", senha='')

    selecionados = request.form.getlist('checkbox')

    caracteres = []

    if '1' in selecionados:
        caracteres.append([chr(i) for i in range(ord('A'), ord('Z') + 1)])

    if '2' in selecionados:
        caracteres.append([chr(i) for i in range(ord('a'), ord('z') + 1)])

    if '3' in selecionados:
        caracteres.append([str(i) for i in range(10)])
    
    if '4' in selecionados:
        caracteres.append(list("!@#$%^&*()-_=+[]{}|;:,.<>?/`~"))

    if len(caracteres) == 0:
        return render_template("geradordesenha.html", senha='Selecione pelo menos um tipo de caractere.')

    senha = ''
    for i in range(tamanho_senha):
        senha += ch(ch(caracteres))
    return render_template("geradordesenha.html", senha=senha , selecionados=selecionados,tamanho_senha=tamanho_senha)

@app.route("/gerarcpf", methods=["POST"])
def gerar_cpf():
    def validar_cpf(cpf):

        cpf_format = cpf.replace('.','').replace('-','')

        cpf9 = cpf_format[:9]
        #calcular primeiro digito
        cpf_soma1 = 0
        for i,n in enumerate(cpf9):
            cpf_soma1 += int(n) * (10-i)
                
        cpf_soma1 *= 10

        resto_cpf1 = cpf_soma1 % 11

        if resto_cpf1 > 9:
                primeiro_digito = 0 
        else:
                primeiro_digito = resto_cpf1

        #calcular o segundo digito

        cpf10 = cpf_format[:9] + str(primeiro_digito)
        cpf_soma2 = 0

        for i,n in enumerate(cpf10):
            cpf_soma2 += int(n) * (11-i)

                
        cpf_soma2 *= 10

        resto_cpf2 = cpf_soma2 % 11

        if resto_cpf2 > 9:
            segundo_digito = 0 
        else:
            segundo_digito = resto_cpf2

        dois_ultimos = str(primeiro_digito) + str(segundo_digito)
                
        if cpf_format[-2:] == dois_ultimos:
            return True
        else:
            return False

    from random import randint
    formatado = request.form.get("checkbox")

    cpf_invalido = True

    while cpf_invalido:
        cpf_criado = "".join([str(randint(0, 9)) for i in range(11)])
        cpf_invalido = False if validar_cpf(cpf_criado) else True
            
        
    cpf_str = ""
    
    if formatado == '1':
        cpf_str += f'{cpf_criado[:3]}.{cpf_criado[3:6]}.{cpf_criado[6:9]}-{cpf_criado[9:]}' + "\n"
    else:
        cpf_str += cpf_criado + "\n"
   
    return render_template("geradordecpf.html", cpf_str=cpf_str, formatado=formatado)


@app.route('/converter', methods=['POST'])
def converter_moeda():
    from decimal import Decimal
    import requests

    
    valor = request.form.get('valor', type=float)
    base = request.form.get('conveter')       
    target = request.form.get('convertido')


    if valor is None:
        return render_template("conversordemoedas.html", valor=valor, valor_convertido='', converter=base, convertido=target)

    if base == target:
        return render_template("conversordemoedas.html", valor=valor, valor_convertido=valor, converter=base, convertido=target)

    response = requests.get(f'https://economia.awesomeapi.com.br/last/{base}-{target}')
    dc = response.json()

    valor_target = float(dc[f'{base}{target}']['bid'])

    
    valor_convertido = round(Decimal(valor * valor_target),2)

    return render_template("conversordemoedas.html", valor=valor, valor_convertido=valor_convertido, converter=base, convertido=target)



@app.route('/update_slider', methods=['POST'])
def update_slider():
    data = request.get_json()
    slider_value = data.get('value')
    return jsonify(slider_value)